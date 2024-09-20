import datetime
from tarfile import *
from getpass import *


with TarFile('files.tar', 'a') as tar:
    while True:
        command = input('$ ')
        if command == 'ls':
            for name in tar.namelist():
                print(name)
        elif command == "exit":
            break
        elif command.startswith('cat '):
            path = command.split()[1]
            content = tar.read(path).decode()
            print(content)
        elif command == "date":
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(current_date)
        elif command == "who":
            user = getuser()
            print(user)
        