import os
import socket
import select
import threading
import shutil

# Функция по окраске текста
def colorize(text, color_code):
    if color_code == 'red':  # Покраска текста в красный (ошибка)
        return f'\033[91m{text}\033[0m'
    elif color_code == 'yellow':  # Покраска текста в желтый (предупреждение)
        return f'\033[93m{text}\033[0m'
    elif color_code == 'green':  # Покраска текста в зеленый (успешно)
        return f'\033[92m{text}\033[0m'
    elif color_code == 'purple':  # Покраска текста в фиолетовый (команды)
        return f'\033[95m{text}\033[0m'
    else:
        return f'{text}'


# Создание сокета клиента
HOST_SERVER, PORT_SERVER = '192.168.0.103', 12345
sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключение клиента к серверу
sock_client.connect((HOST_SERVER, PORT_SERVER))
print(colorize(f'Клиент был подключен к серверу: HOST - [*{HOST_SERVER}*],  PORT - [*{PORT_SERVER}*]', 'green'), '')
print(f'Чтобы открыть справку по командам, введите - {colorize("document", "purple")}\n\n')






# поиск файла и копирование
def find_copy_file(file_name, destin_path):
    # проверка файла, на то, что есть ли он в текущей дирректории
    destin_file_now = os.path.join("C:/PYTHON_/_PROJECT_PYTHON/Python_Project_Other/clitent_sock", file_name)
    if os.path.exists(destin_file_now):
        print(f'{colorize("Файл уже существует в целевой директории: ", "green")}{colorize(destin_path, "red")}\n')
        return upload_file(file_name, file_flag=False)

    # поиск файла на пк
    for root, dirs, files in os.walk('/'):
        if file_name in files:
            file_path = os.path.join(root, file_name)

            # копирование файла в дирректорию сервака
            shutil.copy2(file_path, destin_path)
            print(f'{colorize("Файл скопирован в дирректорию: ", "green")}{colorize(destin_path, "red")}\n')
            return True

    print(f'{colorize("Файл был не найден на данном устройстве!", "red")}')
    return False

# Функция загрузки файла с сервера
def download_file(file_name):
    # Отправка команды на сервер для загрузки файла
    sock_client.sendall(f'download {file_name}'.encode('utf-8'))

    # Прием файла от сервера
    with open(file_name, 'wb') as file:
        while True:
            readable, _, _ = select.select([sock_client], [], [], 10.0)
            if readable:
                file_data = sock_client.recv(1024)
                if not file_data:
                    break
                file.write(file_data)
            else:
                break




# функция отправки файла на сервер
def upload_file(file_name, file_flag=True):
    if file_flag:
        # создаем путь куда сохраним наш файл
        destin_path = os.path.join("C:/PYTHON_/_PROJECT_PYTHON/Python_Project_Other/clitent_sock/cacheCL", file_name)

        if find_copy_file(file_name, destin_path):
            # чтение нового файла и отправка его содержимого клиенту
            with open(destin_path, 'rb') as file:
                while True:
                    file_data = file.read(1024)
                    if not file_data:
                        break
                    sock_client.sendall(file_data)
    else:
        with open(file_name, 'rb') as file:
            while True:
                file_data = file.read(1024)
                if not file_data:
                    break
                sock_client.sendall(file_data)




# Функция отправки запросов и получения ответа
def send_message():
    while True:
        # Ввод команды
        cmd = input(colorize('Введите консольную команду: ', 'yellow'))

        # Отправка команды
        sock_client.sendall(cmd.encode('utf-8'))


        flag_answer_doc = True # флаг для отслежки что использовалась документация
        if cmd == 'document':
            print(sock_client.recv(1024).decode('utf-8') + '\n')
            flag_answer_doc = False

        elif cmd.startswith('download'):
            _, file_name = cmd.split(' ', 1)
            download_file(file_name)
            print(f'Файл был успешно загружен на клиент\n')
            continue
        elif cmd.startswith('upload'):
            _, file_path = cmd.split(' ', 1)
            upload_file(file_path)
            print(f'Файл был успешно отправлен на сервер\n')
            continue



        readable, _, _ = select.select([sock_client], [], [], 1.0)  # Ожидание в течение 1 секунды

        if readable:
            # Получение ответа
            answer = sock_client.recv(1024).decode("utf-8")
            if answer.strip() == '':
                print("""Ответ сервера: [- Пусто, это не ошибка! Просто сервер не может вернуть пустое значение, поэтому 
                чтобы клиент не зависал, пришлось сделать вывод этого сообщения. Например, когда вы вводите команду для 
                перехода в другую директорию сервер возвращает ничего и программа получает соответственно ничего. 
                Поэтому я решил данную проблему так -]\n""")
            elif answer == 'Клиент отключен':
                print(f'{colorize(answer.upper(), "red")}\n')
                break
            elif answer == 'Сервер был выключен':
                print(f'{colorize(answer.upper(), "red")}\n')
                break
            else:
                if flag_answer_doc:
                    print(f'{colorize("Ответ сервера: ", "green")}[- {answer.strip()} -]\n')
                else:
                    continue
        else:
            print(colorize("""Ответ сервера: [- Пусто, это не ошибка! Просто сервер не может вернуть пустое значение, 
            поэтому чтобы клиент не зависал, пришлось сделать вывод этого сообщения. Например, когда вы вводите команду 
            для перехода в другую директорию сервер возвращает ничего и программа получает соответственно ничего. 
            Поэтому я решил данную проблему так -]\n""", 'red'))


# Запуск функции отправки запросов и получения ответа в отдельном потоке
thread_send = threading.Thread(target=send_message)
thread_send.start()

# Ожидание завершения потока
thread_send.join()

# Закрытие соединения с сервером
sock_client.close()
