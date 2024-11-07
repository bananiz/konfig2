import unittest
from unittest.mock import patch
import yaml
from visualizer import get_commits_with_file, build_dependency_graph


class TestVisualizer(unittest.TestCase):
    def setUp(self):
        """Загружаем конфигурацию из файла и определяем необходимые переменные."""
        self.config_path = '/config.yaml'
        self.config = self.load_config(self.config_path)

        # Параметры из конфигурации
        self.repository_path = self.config.get('repository_path', '/path/to/repository')
        self.file_path = self.config.get('file_path', 'README.md')
        self.file_hash = self.config.get('file_hash', '7c8dc7ee0bdf8dfbe0c189b46d7ff800b80a7c29')
        self.output_path = self.config.get('output_path', '/Users/banani/output/commit_graph.md')

    def load_config(self, file_path):
        """Загрузка конфигурации из yaml файла."""
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)
        return config

    def test_load_config(self):
        """Проверка загрузки конфигурации."""
        self.assertIsNotNone(self.config)
        self.assertIn('repository_path', self.config)
        self.assertIn('file_hash', self.config)
        self.assertIn('output_path', self.config)

    @patch('visualizer.subprocess.check_output')
    def test_get_commits_with_file(self, mock_check_output):
        """Тестируем функцию получения коммитов для конкретного файла."""

        # Мокаем команду git log для тестирования
        mock_check_output.return_value = """
        191c63aa1550750fd067cbc3cdf2290ca5952d5b|Елисеев Роман Андреевич|2023-03-03 16:52:20 +0000
        a96ec0c1a2fbb0b7a6475be8887df73f0ffab52c|Елисеев Роман Андреевич|2023-02-28 15:51:50 +0000
        3c1041e30d08ef668d64005aa9ce37744a643b7c|Елисеев Роман Андреевич|2023-02-28 15:51:00 +0000
        """

        # Передаем правильные аргументы
        commits = get_commits_with_file(self.repository_path, self.file_path)

        # Проверка, что хеш коммита найден
        commit_hashes = [commit[0] for commit in commits]  # Извлекаем хеши из каждого коммита
        self.assertIn('191c63aa1550750fd067cbc3cdf2290ca5952d5b', commit_hashes)
        self.assertIn('a96ec0c1a2fbb0b7a6475be8887df73f0ffab52c', commit_hashes)
        self.assertIn('3c1041e30d08ef668d64005aa9ce37744a643b7c', commit_hashes)

    def test_build_dependency_graph(self):
        """Тестируем построение графа зависимости между коммитами."""

        commits = [
            ('191c63aa1550750fd067cbc3cdf2290ca5952d5b', 'Елисеев Роман Андреевич', '2023-03-03 16:52:20 +0000'),
            ('a96ec0c1a2fbb0b7a6475be8887df73f0ffab52c', 'Елисеев Роман Андреевич', '2023-02-28 15:51:50 +0000'),
            ('3c1041e30d08ef668d64005aa9ce37744a643b7c', 'Елисеев Роман Андреевич', '2023-02-28 15:51:00 +0000')
        ]

        # Строим граф зависимости
        graph = build_dependency_graph(commits)

        # Проверяем, что коммиты присутствуют в графе (сокращенные хеши)
        self.assertIn('191c63a', graph)
        self.assertIn('a96ec0c', graph)
        self.assertIn('3c1041e', graph)

@patch('visualizer.save_output')
def test_save_output(self, mock_save_output):
    """Тестируем сохранение графа в файл."""
    graph = "graph TD\n 191c63a[\"commit 1\"]\n a96ec0c[\"commit 2\"]\n 191c63a --> a96ec0c\n"
    print("Graph to be saved:", graph)

    # Строим граф зависимости
    build_dependency_graph([
        ('191c63aa1550750fd067cbc3cdf2290ca5952d5b', 'Елисеев Роман Андреевич', '2023-03-03 16:52:20 +0000'),
        ('a96ec0c1a2fbb0b7a6475be8887df73f0ffab52c', 'Елисеев Роман Андреевич', '2023-02-28 15:51:50 +0000'),
        ('3c1041e30d08ef668d64005aa9ce37744a643b7c', 'Елисеев Роман Андреевич', '2023-02-28 15:51:00 +0000')
    ])

    print("Mock call count:", mock_save_output.call_count)
    print("Mock call args:", mock_save_output.call_args_list)

    # Проверяем, что функция save_output была вызвана с правильными аргументами
    mock_save_output.assert_called_once_with(self.output_path, graph)


if __name__ == '__main__':
    unittest.main()
