import unittest
from unittest.mock import patch, MagicMock
import srex


class TestFileClassification(unittest.TestCase):

    @patch('srex.Path')
    @patch('srex.get_directory')
    def test_directory_creation(self, mock_get_directory, mock_path):
        mock_get_directory.return_value = '/mock/directory'
        mock_directory = MagicMock()
        mock_path.return_value = mock_directory
        mock_directory.is_dir.return_value = True
        mock_directory.iterdir.return_value = []

        # Mock the mkdir method
        mock_category_path = MagicMock()
        mock_directory.__truediv__.return_value = mock_category_path

        # Run the script
        with self.assertRaises(srex.EmptyDirectoryError):
            srex.main()

        # Check if the mkdir method was called for each category
        self.assertTrue(mock_category_path.mkdir.called)

    @patch('srex.Path')
    @patch('srex.get_directory')
    def test_file_classification(self, mock_get_directory, mock_path):
        mock_get_directory.return_value = '/mock/directory'
        mock_directory = MagicMock()
        mock_path.return_value = mock_directory
        mock_directory.is_dir.return_value = True

        # Mock files with different extensions
        mock_files = [
            MagicMock(suffix='.jpg', name='image.jpg'),
            MagicMock(suffix='.pdf', name='document.pdf'),
            MagicMock(suffix='.csv', name='data.csv'),
            MagicMock(suffix='.mp4', name='video.mp4'),
            MagicMock(suffix='.unknown', name='unknown.xyz')
        ]
        mock_directory.iterdir.return_value = mock_files

        # Mock the destination paths
        mock_dest_path = MagicMock()
        mock_directory.__truediv__.return_value = mock_dest_path

        # Run the script
        srex.main()

        # Check if the rename method was called for each file
        for file in mock_files:
            self.assertTrue(file.rename.called)

    @patch('srex.Path')
    @patch('srex.get_directory')
    def test_classify_file_permission_error(self, mock_get_directory, mock_path):
        mock_get_directory.return_value = '/mock/directory'
        mock_directory = MagicMock()
        mock_path.return_value = mock_directory
        mock_directory.is_dir.return_value = True

        # Mock a file with a permission error
        mock_file = MagicMock(suffix='.jpg', name='image.jpg')
        mock_file.rename.side_effect = PermissionError

        categories = {
            'Images': ['jpeg', 'jpg', 'png'],
            'PDFs': ['pdf'],
            'Datasets': ['csv', 'xlsx', 'json'],
            'Videos&ShortVids': ['mp4', 'gif'],
            'Other': []
        }

        with self.assertRaises(srex.PermissionDeniedError):
            srex.classify_file(mock_file, mock_directory, categories)


if __name__ == '__main__':
    unittest.main()
