import socket
import threading

nickname = input("Nickname : ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    host = '127.0.0.1'  
    port = 64201  

    c.connect((host, port))

    def receive() :
        while True :
            try :
                message = c.recv(1024).decode('ascii')
                if message == 'ER' :
                    c.send(nickname.encode('ascii'))
                else :
                    print(message)
            except :
                print("Error")
                c.close()
                break
    
    def write() :
        while True :
            message = f'{nickname} : {input("")}'
            c.send(message.encode('ascii'))

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    
    write_thread = threading.Thread(target=write)
    write_thread.start()
