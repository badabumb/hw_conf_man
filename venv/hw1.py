import tarfile
import datetime
import os
import sys
import json
from getpass import getuser

def main():
    # Проверка аргументов командной строки
    if len(sys.argv) < 4:
        print("Использование: python hw1.py <имя_компьютера> <путь_к_архиву> <путь_к_лог_файлу>")
        sys.exit(1)

    # Аргументы командной строки
    computer_name = sys.argv[1]
    archive_path = sys.argv[2]
    log_file_path = sys.argv[3]

    # Переменные для хранения истории и текущей директории
    history = []
    current_directory = '/'
    log_data = []

    # Функция для записи действий в лог-файл
    def log_action(command, output):
        log_data.append({
            "command": command,
            "output": output,
            "timestamp": datetime.datetime.now().isoformat()
        })

    # Открываем tar архив для чтения
    with tarfile.open(archive_path, 'r:*') as tar:
        members = tar.getmembers()  # Получаем список всех файлов и директорий
        while True:
            command = input(f"{computer_name}:{current_directory}$ ")

            # Добавляем команду в историю
            history.append(command)
            log_action(command, "")

            if command.startswith('ls'):
                args = command.split()
                path = args[1].rstrip('/') if len(args) > 1 else current_directory.rstrip('/')
                directory = path.lstrip('/')
                output = []

                for member in members:
                    if member.name.startswith(directory) and member.name != directory:
                        relative_path = member.name[len(directory):].lstrip('/')
                        if '/' not in relative_path:
                            output.append(relative_path)

                result = "\n".join(output)
                print(result)
                log_action(command, result)

            elif command == "exit":
                log_action(command, "Exiting shell.")
                break

            elif command.startswith('cat '):
                path = command.split()[1]
                full_path = os.path.normpath(os.path.join(current_directory.lstrip('/'), path))
                try:
                    file = tar.extractfile(full_path)
                    if file:
                        content = file.read().decode()
                        print(content)
                        log_action(command, content)
                    else:
                        error_message = f"cat: {path}: No such file"
                        print(error_message)
                        log_action(command, error_message)
                except KeyError:
                    error_message = f"cat: {path}: No such file"
                    print(error_message)
                    log_action(command, error_message)

            elif command == "date":
                current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(current_date)
                log_action(command, current_date)

            elif command == "who":
                user = getuser()
                print(user)
                log_action(command, user)

            elif command.startswith('cd '):
                new_dir = command.split()[1]
                if new_dir == "..":
                    if current_directory != '/':
                        current_directory = os.path.dirname(current_directory.rstrip('/'))
                        if current_directory == '':
                            current_directory = '/'
                    log_action(command, f"Changed directory to {current_directory}")
                else:
                    potential_dir = os.path.normpath(os.path.join(current_directory, new_dir)).lstrip('/')
                    if any(member.isdir() and member.name.rstrip('/') == potential_dir for member in members):
                        current_directory = '/' + potential_dir
                        log_action(command, f"Changed directory to {current_directory}")
                    else:
                        error_message = f"cd: {new_dir}: No such directory"
                        print(error_message)
                        log_action(command, error_message)

            elif command == "history":
                output = "\n".join(f"{idx} {cmd}" for idx, cmd in enumerate(history, start=1))
                print(output)
                log_action(command, output)

            else:
                error_message = f"{command}: command not found"
                print(error_message)
                log_action(command, error_message)

    # Сохраняем лог-файл в формате JSON
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        json.dump(log_data, log_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()