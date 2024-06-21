import shutil
import unittest
from pathlib import Path

from tqdm import tqdm

from sortasaurus_rex.utilities.classifier import classify_file, classify_files_in_directory


class TestFileClassification(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = Path('test_directory')
        self.test_dir.mkdir(exist_ok=True)

        # Create test files
        (self.test_dir / 'test1.jpg').touch()
        (self.test_dir / 'test2.png').touch()
        (self.test_dir / 'document1.pdf').touch()
        (self.test_dir / 'audio1.mp3').touch()
        (self.test_dir / 'video1.mp4').touch()
        (self.test_dir / 'unknownfile.xyz').touch()

        # Create subdirectories for categorized files
        (self.test_dir / 'Images').mkdir(exist_ok=True)
        (self.test_dir / 'Documents').mkdir(exist_ok=True)
        (self.test_dir / 'Audio').mkdir(exist_ok=True)
        (self.test_dir / 'Videos').mkdir(exist_ok=True)
        (self.test_dir / 'Others').mkdir(exist_ok=True)

    def tearDown(self):
        # Remove the temporary directory after tests
        shutil.rmtree(self.test_dir)

    def test_classify_file(self):
        categories = {
            '.jpg': 'Images',
            '.png': 'Images',
            '.pdf': 'Documents',
            '.mp3': 'Audio',
            '.mp4': 'Videos',
        }
        for file in self.test_dir.iterdir():
            if file.is_file():
                file_name, category = classify_file(file, self.test_dir, categories)
                expected_dir = self.test_dir / categories.get(file.suffix.lower(), 'Others')
                expected_path = expected_dir / file.name
                self.assertTrue(expected_path.exists())
                self.assertEqual(category, categories.get(file.suffix.lower(), 'Others'))

    def test_classify_files_in_directory(self):
        categories = {
            '.jpg': 'Images',
            '.png': 'Images',
            '.pdf': 'Documents',
            '.mp3': 'Audio',
            '.mp4': 'Videos',
        }
        with tqdm(total=6, desc="Classifying files", unit="file") as pbar:
            classify_files_in_directory(self.test_dir, categories, pbar)

        for ext, category in categories.items():
            category_dir = self.test_dir / category
            self.assertTrue(any(category_dir.iterdir()))

        others_dir = self.test_dir / 'Others'
        self.assertTrue(any(others_dir.iterdir()))


if __name__ == '__main__':
    unittest.main()
