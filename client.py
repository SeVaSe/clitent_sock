import socket

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

    # получение ответа
    print(f'Ответ сервера: [- {sock_client.recv(1024).decode("utf-8")} -]')

















