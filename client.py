import socket
import select
from tkinter import *
from tkinter import scrolledtext

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
HOST_SERVER, PORT_SERVER = 'localhost', 12345
sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# подключение клиента к серваку
sock_client.connect((HOST_SERVER, PORT_SERVER))
print(colorize(f'Клиент был подключен к серверу: HOST - [*{HOST_SERVER}*],  PORT - [*{PORT_SERVER}*]', 'green'), '\n\n')



# окно
window = Tk()
window.title('CMD-контроль')
window.geometry('700x470')


lbl = Label(window, text='КЛИЕНТ БЫЛ ПОДКЛЮЧЕН К СЕРВЕРУ', foreground='red')
lbl.pack()

# отображение текста
message_display = scrolledtext.ScrolledText(window)
message_display.pack(fill=X)

# ввод запроса
input_text = Entry(window)
input_text.pack(fill=X)


def send_command():

    # ввод комманды
    cmd = input_text.get()

    # отправка
    sock_client.sendall(cmd.encode('utf-8'))  # как я понял, sendall - он более надежный в отправке сообщения на сервак

    # ожидание данных для чтения
    # символы '_' для игнорирования этих списков, так как они не интересуют в данном контексте
    # select.select() принимает три списка: readList, writeList, excepList
    readable, _, _ = select.select([sock_client], [], [], 3.0)  # ожидание в течение 1 секунды

    if readable:
        # получение ответа
        answer = sock_client.recv(1024).decode("utf-8")
        if answer.strip() == '':
            message_display.insert(END, "ОТВЕТ СЕРВЕРА: [- Пусто! Вы отправили пустой запрос... -]\n\n")

            print(colorize("ОТВЕТ СЕРВЕРА: [- Пусто! Вы отправили пустой запрос... -]\n\n", 'red'))


        else:
            message_display.insert(END,f'ОТВЕТ СЕРВЕРА: [- {answer.strip()} -]\n\n')

            print(f'{colorize("Ответ сервера: ", "green")}[- {answer.strip()} -]\n')
    else:
        message_display.insert(END, "ОТВЕТ СЕРВЕРА: [- Пусто, это не ошибка! Просто сервер не может вернуть пустое значение, поэтому чтобы "
                               "клиент не зависал, пришлось сделать вывод этого сообщения. Например когда вы вводите команду для перехода "
                               " в другую дирректорию сервер возращает ничего и программа получает соотвественно ничего. Поэтому я решил данную проблему так -]\n\n")

        print(colorize("""Ответ сервера: [- Пусто, это не ошибка! Просто сервер не может вернуть пустое значение, поэтому чтобы 
                    клиент не зависал, пришлось сделать вывод этого сообщения. Например когда вы вводите команду для перехода
                    в другую дирректорию сервер возращает ничего и программа получает соотвественно ничего. Поэтому я решил данную проблему так -]\n""",
                       'red'))


# кнопка
btn = Button(window, text='Отправить запрос', command=send_command)
btn.pack()

mainloop()



















