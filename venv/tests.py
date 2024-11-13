import unittest
import os
from io import StringIO
from unittest.mock import patch
import datetime
from hw1 import main  # Импортируем main из hw1.py


class TestTarShell(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Устанавливаем текущую директорию в директорию файла tests.py (где находится arch.tar)
        cls.original_directory = os.getcwd()
        os.chdir(os.path.dirname(__file__))

    @classmethod
    def tearDownClass(cls):
        # Возвращаемся в исходную директорию после завершения всех тестов
        os.chdir(cls.original_directory)

    @patch('builtins.input', side_effect=['ls', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_ls_command(self, mock_stdout, mock_input):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("arch", output)

    @patch('builtins.input', side_effect=['cd arch', 'cat doc1.txt', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_cat_command(self, mock_stdout, mock_input):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Hello world!", output)  # Ожидаемый контент файла doc1.txt в arch.tar

    @patch('builtins.input', side_effect=['cd arch', 'cd dir1', 'ls', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_cd_ls_command(self, mock_stdout, mock_input):
        main()
        output = mock_stdout.getvalue()
        # Проверка наличия файлов something_interesting1.txt и something_interesting2.txt внутри dir1
        self.assertIn("something_interesting.txt", output)
        self.assertIn("something_interesting2.txt", output)

    @patch('builtins.input', side_effect=['date', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_date_command(self, mock_stdout, mock_input):
        main()
        output = mock_stdout.getvalue()
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.assertIn(current_date, output)

    @patch('builtins.input', side_effect=['who', 'exit'])
    @patch('getpass.getuser', return_value="testuser")
    @patch('sys.stdout', new_callable=StringIO)
    def test_who_command(self, mock_stdout, mock_getuser, mock_input):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("juliavediukova", output)

    @patch('builtins.input', side_effect=['history', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_history_command(self, mock_stdout, mock_input):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("1 history", output)


if __name__ == '__main__':
    unittest.main()