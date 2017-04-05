"""

Devoir 3 - Systemes d'exploitation. 
Chat Server & Client  

Autor: Alexandra Rautu
Grupa: 1220F

"""

import sys
import socket
import select
 
def chat_client():
    if(len(sys.argv) < 3) :
        print "Ce n'est pas une commande valable. Il faut introduire pour se connecter:  python chat_client.py hostname port"
        sys.exit()

    host = sys.argv[1] #On lit le premier argv du commande (le hostname)
    port = int(sys.argv[2]) #On lit le deuxieme argv du commande (le nombre du port)

    #Une variable qui compte le nombre des clients connectes
    #clients_counter = 0
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    #Connexion au host
    try :
        s.connect((host, port))
        ##clients_counter = 1
    except :
        print 'Connexion impossible'
        sys.exit()
     
    #S'il n'y a pas plus qu'un client dans le chat, le client connecte ne peut pas parler.
    #if(clients_counter < 2):
    #    print "Il n'y a pas un pair pour parler. Attendre qu'une autre personne rejoint le chat" 
    #elif(clients_counter > 2):
    #    print 'Connexion reussie. Vous pouvez envoyer des messages maintenant.'
    #    sys.stdout.write('[Moi] '); sys.stdout.flush()
    
    print 'Connexion reussie. Vous pouvez envoyer des messages maintenant.'
    sys.stdout.write('[Moi] '); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        #Liste des sockets valables
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])

        for sock in ready_to_read:             
            if sock == s:
                #Message du serveur
                data = sock.recv(1024)
                    
                if not data :
                    print '\nDeconnecte du serveur'
                    sys.exit()
                else :
                    #Afficher les messages
                    sys.stdout.write(data)
                    sys.stdout.write('[Moi] '); sys.stdout.flush()     
                
            else :
                #L'utilisateur courant a envoye un message
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.write('[Moi] '); sys.stdout.flush() 
        
if __name__ == "__main__":

    sys.exit(chat_client())