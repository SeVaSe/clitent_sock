import socket
import select
import threading

# функция по окраске текста
def colorize(text, color_code):
    if color_code == 'red': # покраска текста в красный (ошибка)
        return f'\033[91m{text}\033[0m'
    elif color_code == 'yellow': # покраска текста в желтый (предупреждение)
        return f'\033[93m{text}\033[0m'
    elif color_code == 'green': # покраска текста в зеленый (успешно)
        return f'\033[92m{text}\033[0m'
    else:
        return f'{text}'

# создание сокета клиента
HOST_SERVER, PORT_SERVER = '192.168.0.103', 12345
sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# подключение клиента к серваку
sock_client.connect((HOST_SERVER, PORT_SERVER))
print(colorize(f'Клиент был подключен к серверу: HOST - [*{HOST_SERVER}*],  PORT - [*{PORT_SERVER}*]', 'green'), '\n\n')







# функция отправки запросов и получения от них ответа
def send_message():
    # функция загрузки файла с сервера
    def download_file(file_name):
        # отправка команды на сервер для загрузки файла
        sock_client.sendall(f'download {file_name}'.encode('utf-8'))
        # прием файла от сервера
        file_data = sock_client.recv(1024)

        # сохранение файла на клиенте
        with open(file_name, 'wb') as file:
            file.write(file_data)


    while True:
        # ввод комманды
        cmd = input(colorize('Введите консольную команду: ', 'yellow'))

        # отправка
        sock_client.sendall(cmd.encode('utf-8')) # как я понял, sendall - он более надежный в отправке сообщения на сервак


        if cmd.startswith('download'):
            _, file_name = cmd.split(' ', 1)
            download_file(file_name)
            continue

        elif cmd.startswith('upload'):
            pass

        # ожидание данных для чтения
        # символы '_' для игнорирования этих списков, так как они не интересуют в данном контексте
        # select.select() принимает три списка: readList, writeList, excepList
        readable, _, _ = select.select([sock_client], [], [], 1.0)  # ожидание в течение 1 секунды

        if readable:
            # получение ответа
            answer = sock_client.recv(1024).decode("utf-8")
            if answer.strip() == '':
                print("""Ответ сервера: [- Пусто, это не ошибка! Просто сервер не может вернуть пустое значение, поэтому чтобы 
                клиент не зависал, пришлось сделать вывод этого сообщения. Например когда вы вводите команду для перехода
                в другую дирректорию сервер возращает ничего и программа получает соотвественно ничего. Поэтому я решил данную проблему так-]\n""")
            else:
                print(f'{colorize("Ответ сервера: ", "green")}[- {answer.strip()} -]\n')
        else:
            print(colorize("""Ответ сервера: [- Пусто, это не ошибка! Просто сервер не может вернуть пустое значение, поэтому чтобы 
                клиент не зависал, пришлось сделать вывод этого сообщения. Например когда вы вводите команду для перехода
                в другую дирректорию сервер возращает ничего и программа получает соотвественно ничего. Поэтому я решил данную проблему так -]\n""", 'red'))


threard_send = threading.Thread(target=send_message)
threard_send.start()












