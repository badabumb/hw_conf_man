import tarfile  # Импорт модуля для работы с tar-архивами
import datetime
import os
from getpass import getuser


def main():
    # Переменная для хранения истории команд
    history = []
    current_directory = '/'

    # Открываем tar архив для чтения
    with tarfile.open('arch.tar', 'r:*') as tar:
        members = tar.getmembers()  # Получаем список всех файлов и директорий
        while True:
            command = input(f"{current_directory}$ ")

            # Добавляем команду в историю
            history.append(command)

            if command.startswith('ls'):
                # Извлекаем путь после команды 'ls', если он указан
                args = command.split()
                if len(args) > 1:
                    # Если путь указан, используем его
                    path = args[1].rstrip('/')  # Убираем возможный завершающий слеш
                else:
                    # Если путь не указан, используем текущую директорию
                    path = current_directory.rstrip('/')

                # Убираем ведущий слеш для соответствия пути в tar
                directory = path.lstrip('/')

                for member in members:
                    # Показываем только файлы и папки, которые находятся в указанной директории
                    if member.name.startswith(directory) and member.name != directory:
                        relative_path = member.name[len(directory):].lstrip('/')
                        if '/' not in relative_path:  # Показываем только файлы и папки первого уровня
                            print(relative_path)


            elif command == "exit":
                # Команда exit: завершение работы
                break

            elif command.startswith('cat '):
                # Команда cat: чтение содержимого файла
                path = command.split()[1]
                full_path = os.path.normpath(os.path.join(current_directory.lstrip('/'), path))
                try:
                    file = tar.extractfile(full_path)
                    if file:
                        content = file.read().decode()
                        print(content)
                    else:
                        print(f"cat: {path}: No such file")
                except KeyError:
                    print(f"cat: {path}: No such file")

            elif command == "date":
                # Команда date: вывод текущей даты и времени
                current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(current_date)

            elif command == "who":
                # Команда who: вывод имени текущего пользователя
                user = getuser()
                print(user)

            elif command.startswith('cd '):
                # Команда cd: смена директории
                new_dir = command.split()[1]
                if new_dir == "..":
                    if current_directory != '/':
                        current_directory = os.path.dirname(current_directory.rstrip('/'))
                        if current_directory == '':
                            current_directory = '/'
                else:
                    potential_dir = os.path.normpath(os.path.join(current_directory, new_dir)).lstrip('/')
                    if any(member.isdir() and member.name.rstrip('/') == potential_dir for member in members):
                        current_directory = '/' + potential_dir
                    else:
                        print(f"cd: {new_dir}: No such directory")

            elif command == "history":
                # Команда history: вывод истории команд
                for idx, cmd in enumerate(history, start=1):
                    print(f"{idx} {cmd}")

            else:
                print(f"{command}: command not found")

main()