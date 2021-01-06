import socket, sys, time, pickle, threading, engine
import colorama as color


color.init()

greenL = color.Fore.LIGHTGREEN_EX
yellowL = color.Fore.LIGHTYELLOW_EX
redL = color.Fore.LIGHTRED_EX
red = color.Fore.RED
white = color.Fore.WHITE


maxTries = 5
maxSize = 10
headerSize = 7
bufferSize = 500

run = True; tries = 0; user_amount = 0; maxheaderSize = pow(10, headerSize-2) #100,000  10*10*10*10*10
users = []


def create_socket(_ip, _port):
    global server, maxTries, tries
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((_ip, _port))
        server.listen(5)
        print("\nServer created!\n")
        return True
    except:
        tries += 1
        if tries >= maxTries:
            tries = 0
            print(redL + f"\nERROR: Server could not be created after {maxTries} tries!" + white)
            print("Possibly the IP or the port is wrong.\n")
            return False
        print(redL + f"ERROR: Server could not be created!\n       Retrying...({tries})" + white)
        time.sleep(0.5)
        create_socket(_ip, _port) 


def remove_user(conn, address):
    global user_amount, users
    for user in users:
        if user == [conn, address]:
            users.remove(user)
            engine.remove_cam(address)
            print(yellowL + f"\n{address} removed!" + white)
            conn.close()
            user_amount -= 1
            for user in users:
                sendMessage(user[0], user[1], f"User {address[0]} disconnected!", "yellowL")


def sendMessage(conn, address, msg, colorIndex):
    try:
        d = pickle.dumps([False, msg, colorIndex])
        conn.send(bytes(f"{len(d):<{headerSize}}", "utf-8") + d)
    except socket.error:
        print(red + "\nERROR: User, whom we are sending a message, does not exsist." + white)
        remove_user(conn, address)
        return


def sendInfo(conn, address): 
    global headerSize, bufferSize, info
    while run:    
        try:
            length = int(conn.recv(headerSize))
            if length > maxheaderSize:
                print(red + "\nERROR: User, we are receiving data from, has given a faulty data size." + white); remove_user(conn, address)
            data = bytes("", "utf-8")
            while length > 0:
                data += conn.recv(bufferSize); length -= bufferSize
            pos, rot = pickle.loads(data)
            engine.update_user_info(address, pos, rot)
            d = pickle.dumps([True, engine.get_info()])
            conn.send(bytes(f"{len(d):<{headerSize}}", "utf-8") + d)
        except:
            print(red + "\nERROR: User, we are receiving data from, does not exsist, or is giving faulty data." + white)
            remove_user(conn, address)
            return 


def start():
    global user_amount, maxSize
    threading.Thread(target=engine.start).start()
    while run:
        conn, address = server.accept()
        if maxSize <= user_amount: 
            sendMessage(conn, address, "SERVER: Server is full!    Try again later.", "yellowL")
            conn.close()
        else:
            for user in users:
                sendMessage(user[0], user[1], f"SERVER: User {address} joined the server!", "yellowL")
            users.append([conn, address])
            engine.add_cam(address)
            print(greenL + f"User {address} connected!" + white)
            sendMessage(conn, address, "Welcome to the server!", "greenL")
            threading.Thread(target=sendInfo, args=[conn, address]).start()
            user_amount += 1


def stop():
    global run
    run = False