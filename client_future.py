import select
import socket
import subprocess
import os
import threading
import signal
import shutil



# функция по окраске текста
def colorize(text, color_code):
    if color_code == 'red': # покраска текста в красный (ошибка)
        return f'\033[91m{text}\033[0m'
    elif color_code == 'yellow': # покраска текста в желтый (предупреждение)
        return f'\033[93m{text}\033[0m'
    elif color_code == 'green': # покраска текста в зеленый (успешно)
        return f'\033[92m{text}\033[0m'
    elif color_code == 'purple':  # Покраска текста в фиолетовый (команды)
        return f'\033[95m{text}\033[0m'
    else:
        return f'{text}'



# КЛАС ДОП ФУНКЦИОНАЛА
class DopFunctionalClient():

    # MENU
    def main_menu(self):
        while True:
            print(f'''\n
{colorize('ГЛАВНОЕ МЕНЮ:', 'green')}
{"-" * 60}
{colorize('КУДА ВЫ ХОТИТЕ ПЕРЕЙТИ?', 'yellow')}
{colorize('1', 'purple')} - cmd-команды
{colorize('2', 'purple')} - меж-клиентная связь
{colorize('exit', 'purple')} - выход
''')

            # логика меню
            com_choice = input(colorize('Введите запрос: ', 'yellow'))

            # выбор куда перейти
            if com_choice == '1':
                print('\n' + colorize('ВЫ ПЕРЕШЛИ В РАЗДЕЛ "cmd-команды"!', 'red'))
                print(f'Чтобы открыть справку по командам, введите - {colorize("document", "purple")}' + '\n\n\n\n'+'-'*80)
                command_functionality()
                #self.sock_client.close()
                return
            elif com_choice == '2':
                print('\n' + colorize('ВЫ ПЕРЕШЛИ В РАЗДЕЛ "меж-клиентная связь"!', 'red'))
                print(f'Чтобы открыть справку по командам, введите - {colorize("document", "purple")}' + '\n\n\n\n' + '-' * 80)
                inter_client_commun()
                return
            elif com_choice == 'exit':
                print(f'{colorize("ВЫ ВЫШЛИ ИЗ ПРОГРАММЫ.", "red")}')
                return
            else:
                print(f'{colorize("ВЫ ВВЕЛИ НЕ КОРРЕКТНОЕ ЗНАЧЕНИЕ.", "red")}')



# экземляр класса: доп-функционала
dop_functional_client = DopFunctionalClient()





# 1 - CMD-КОМАНДЫ
def command_functionality():
    # Создание сокета клиента
    HOST_SERVER, PORT_SERVER = '192.168.0.103', 12345
    sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Подключение клиента к серверу
    sock_client.connect((HOST_SERVER, PORT_SERVER))
    print(colorize(f'Клиент был подключен к серверу: {colorize(f"HOST - [*{HOST_SERVER}*],  PORT - [*{PORT_SERVER}*]", "red")}', 'green') + '\n  |\n  |\n  |')



    # поиск файла и копирование
    def find_copy_file(file_name, destin_path):
        # проверка файла, на то, что есть ли он в текущей дирректории
        destin_file_now = os.path.join("C:\PYTHON_\_PROJECT_PYTHON\Python_Project_Other\clitent_sock", file_name)
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
            destin_path = os.path.join("C:/PYTHON_/_PROJECT_PYTHON/Python_Project_Other/clitent_sock/cacheCL",
                                       file_name)

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

            flag_answer_doc = True  # флаг для отслежки что использовалась документация
            if cmd == 'document':
                print(sock_client.recv(1024).decode('utf-8') + '\n')
                flag_answer_doc = False
            elif cmd == 'MainMenu':
                dop_functional_client.main_menu()
                sock_client.close()  # Закрытие соединения с сервером
                flag_answer_doc = False
                return
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
                    return
                elif answer == 'Сервер был выключен':
                    print(f'{colorize(answer.upper(), "red")}\n')
                    return
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



# 2 - МЕЖ-КЛИЕНТНАЯ СВЯЗЬ
def inter_client_commun():
    while True:
        soo = input('Введи соо: ')

        if soo != 'MainMenu':
            print(soo)
        else:
            dop_functional_client.main_menu()



dop_functional_client.main_menu()