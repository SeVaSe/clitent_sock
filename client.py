import socket
import select

# создание сокета клиента
HOST_SERVER, PORT_SERVER = 'localhost', 12345
sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# подключение клиента к серваку
sock_client.connect((HOST_SERVER, PORT_SERVER))
print(f'Клиент был подключен к серверу: HOST - [*{HOST_SERVER}*],  PORT - [*{PORT_SERVER}*]')

while True:
    # ввод комманды
    cmd = input('Введите консольную команду: ')

    # отправка
    sock_client.sendall(cmd.encode('utf-8')) # как я понял, sendall - он более надежный в отправке сообщения на сервак

    # ожидание данных для чтения
    # символы '_' для игнорирования этих списков, так как они не интересуют в данном контексте
    # select.select() принимает три списка: readList, writeList, excepList
    readable, _, _ = select.select([sock_client], [], [], 1.0)  # ожидание в течение 1 секунды

    if readable:
        # получение ответа
        answer = sock_client.recv(1024).decode("utf-8")
        if answer.strip() == '':
            print('Ответ сервера: [- пусто -]')
        else:
            print(f'Ответ сервера: [- {answer.strip()} -]')
    else:
        print('Ответ сервера: [- пусто -]')















