import subprocess
import yaml
import os


def load_config(config_path):
    """Загружает конфигурацию из YAML файла."""
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        print("Loaded config:")
        print(config)
        return config


def get_commits_with_file(repository_path, file_hash_or_path):
    """Получает коммиты, связанные с файлом, по его хешу или пути."""
    print(f"Repository Path: {repository_path}")
    print(f"File Hash/Path: {file_hash_or_path}")

    # Формируем команду для git log
    command = [
        'git', '-C', repository_path, 'log', '--pretty=format:%H|%an|%ad', '--date=iso', '--', file_hash_or_path
    ]

    # Печатаем команду для дебага
    print(f"Running command: {' '.join(command)}")

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.stderr:
        print(f"Error: {result.stderr}")

    print(f"Git log output:\n{result.stdout}")

    if not result.stdout.strip():
        print("Git log returned no output. Please check the file path and hash.")

    commits = result.stdout.strip().split('\n')
    print(f"Total commits found: {len(commits)}")

    valid_commits = [line.split('|') for line in commits if len(line.split('|')) == 3]

    if not valid_commits:
        print("No valid commits found for the specified file.")
        return []

    return valid_commits


def save_output(output_path, graph_code):
    """Сохраняет граф в файл."""
    # Создание директории, если она не существует
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as file:
        file.write(graph_code)
    print(f"Graph saved to {output_path}")


def build_dependency_graph(commits):
    """Строит граф зависимостей для полученных коммитов."""
    graph = "graph TD\n"

    for i, (commit_hash, author, date) in enumerate(commits):
        graph += f"  {commit_hash[:7]}[\"{commit_hash[:7]}\n{author}\n{date}\"]\n"
        if i > 0:
            graph += f"  {commits[i - 1][0][:7]} --> {commit_hash[:7]}\n"

    return graph


def main():
    # Загрузим конфигурацию
    config = load_config('config.yaml')

    repository_path = config['repository_path']
    file_hash_or_path = config['file_hash']  # Это может быть как хеш, так и путь к файлу
    output_path = config['output_path']

    if not os.path.isdir(repository_path):
        print(f"Error: The repository path {repository_path} is not valid.")
        return

    # Получаем коммиты для файла (по хешу или пути)
    commits = get_commits_with_file(repository_path, file_hash_or_path)

    if commits:
        # Строим граф зависимости для найденных коммитов
        graph = build_dependency_graph(commits)

        # Сохраняем граф в файл
        save_output(output_path, graph)
    else:
        print("No commits found for the specified file.")


if __name__ == '__main__':
    main()
