import socket
import select
import threading

# Функция по окраске текста
def colorize(text, color_code):
    if color_code == 'red':  # Покраска текста в красный (ошибка)
        return f'\033[91m{text}\033[0m'
    elif color_code == 'yellow':  # Покраска текста в желтый (предупреждение)
        return f'\033[93m{text}\033[0m'
    elif color_code == 'green':  # Покраска текста в зеленый (успешно)
        return f'\033[92m{text}\033[0m'
    else:
        return f'{text}'


# Создание сокета клиента
HOST_SERVER, PORT_SERVER = '192.168.0.103', 12345
sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключение клиента к серверу
sock_client.connect((HOST_SERVER, PORT_SERVER))
print(colorize(f'Клиент был подключен к серверу: HOST - [*{HOST_SERVER}*],  PORT - [*{PORT_SERVER}*]', 'green'), '\n\n')



# Функция загрузки файла с сервера
def download_file(file_name):
    # Отправка команды на сервер для загрузки файла
    sock_client.sendall(f'download {file_name}'.encode('utf-8'))
    # Прием файла от сервера
    with open(file_name, 'wb') as file:
        while True:
            readable, _, _ = select.select([sock_client], [], [], 1.0)
            if readable:
                file_data = sock_client.recv(1024)
                if not file_data:
                    break
                file.write(file_data)
            else:
                break




# Функция отправки запросов и получения ответа
def send_message():
    while True:
        # Ввод команды
        cmd = input(colorize('Введите консольную команду: ', 'yellow'))

        # Отправка команды
        sock_client.sendall(cmd.encode('utf-8'))

        if cmd.startswith('download'):
            _, file_name = cmd.split(' ', 1)
            download_file(file_name)
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
            else:
                print(f'{colorize("Ответ сервера: ", "green")}[- {answer.strip()} -]\n')
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
