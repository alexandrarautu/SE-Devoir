"""

Devoir 3 - Systemes d'exploitation. 
Chat Server & Client  

Autor: Alexandra Rautu
Grupa: 1220F

"""
import sys
import socket
import select
import time

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 1024 
PORT = 6666

def chat_server():

    #Creation d'un serveur
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))

    #Le serveur peut accepter un nombre maximum de 5 personnes (ajoute un max de 5 demandes dans la fille d'attente)
    server_socket.listen(5)
 
    #Ajouter les clients dans la liste des sockets acceptees 
    SOCKET_LIST.append(server_socket)
 
    currentTime = time.ctime(time.time()) + "\r\n"
    print "Le chat client-serveur a commence sur le port  " + str(PORT) + "\nDate et heure de connexion: " + currentTime 
 
    while 1:

        # Selecter la liste des sockets disponible
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
        
        for sock in ready_to_read:
            
            #une nouvelle connexion est accepte
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print "Client (%s, %s) est connecte" % addr + "\nDate et l'heure de connexion: " + currentTime
                 
                broadcast(server_socket, sockfd, "[%s:%s] a entre dans la conversation\n" % addr)
             
            else:
                
                #le serveur voit les informations provenant du client
                try:
                    
                    #recevoir des donnes du socket, il ne peut pas recevoir que 1024bytes
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        
                        #Il existe des informations dans le socket
                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
                    else:
                        
                        #Elimine le socket qui ne marche plus   
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        #Donc s'il n'y a plus des donnees, la connexion est peut etre casees. On envoie un message aux autres clients. 
                        broadcast(server_socket, sock, "Client (%s, %s) est deconnecte\n" % addr) 

                except:
                    broadcast(server_socket, sock, "Client (%s, %s) est deconnecte\n" % addr)
                    continue

    server_socket.close()
    
#On montre les messages envoie a tous les clients qui sont connectes
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        
        #On envoie le message seulement au pair
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                
                #Exception pour le socket aui ne marche plus
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    sys.exit(chat_server())         