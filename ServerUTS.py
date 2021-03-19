import socket
import select
import threading
import sys


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    host = '127.0.0.1'  
    port = 64201  

    #Untuk menghubungkan Socket dengan Network Interface dan Port
    s.bind((host,port))
    
    #Untuk mendengar / menerima req dari client
    s.listen()
    
    clients = []
    nicknames = []

    def broadcast (message) :
        for client in clients :
            client.send(message)
    
    def handle(client) :
        while True :
            try : 
                message = client.recv(1024)
                broadcast(message)
            except :
                index = clients.index(client)
                clients.remove(client)
                client.close()

                nickname = nicknames[index]
                clients.remove(client)
                client.close()

                nickname = nickname[index]
                broadcast(f'{nickname} left the chat'.encode('ascii'))
                nicknames.remove(nickname)
                break
    
    def receive() :
        while True :
            client , address = s.accept()
            print(f"Connected with {str(address)}")

            client.send('ER'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            print(f"Nickname of the the client is {nickname}")
            broadcast(f"{nickname} Joined the chat!".encode('ascii'))
            client.send('Connected to the server!'.encode('ascii'))

            thread = threading.Thread(target = handle, args = (client,))
            thread.start()

    receive()