import socket

# создание сокета клиента
HOST_SERVER, PORT_SERVER = 'localhost', 12345
sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# подключение клиента к серваку
sock_client.connect((HOST_SERVER, PORT_SERVER))
print(f'Клиент был подключен к серверу: HOST - [*{HOST_SERVER}*],  PORT - [*{PORT_SERVER}*]')

while True:
    cmd = input('Введите консольную команду: ')
    sock_client.sendall(cmd.encode('utf-8')) # как я понял, sendall - он более надежный в отправке сообщения на сервак

















