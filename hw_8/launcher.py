import subprocess

proc_list = []

while True:
    user_action = input("Выберите команду:\n"
                        "up - запустить сервер и клиентов\n"
                        "close - закрыть все окна\n"
                        "exit - выход\n"
                        "Ввод: ")
    if user_action == "up":
        clients_num = int(input("Введите количество пользователей: "))
        proc_list.append(subprocess.Popen("python server.py", creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(clients_num):
            proc_list.append(subprocess.Popen(f"python client.py -n ", creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif user_action == "close":
        while proc_list:
            used_action = proc_list.pop()
            used_action.kill()
    elif user_action == "exit":
        break
