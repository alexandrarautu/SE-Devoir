#Devoir 3 - chat client - serveur

J'ai réalisé un chat client - serveur où un max de 5 clients peuvent se connecter et parler. 
C'est un chat en temps réels, qui affiche les message de chaque client. 
Pour l'utiliser il faut commencer le serveur premièrement: 'python time_server.py' 
Après il faut ouvrir d`autres fenêtres de terminal pour commencer l'utilisation du chat pour un client: 'python time_client.py localhost 6666' 
Après la connexion le chat commence et vous pouvez envoyer des messages.
Pour se déconnecter il faut soit fermer le terminal ou appuyez "ctrl + C" dans le terminal. 

Problème rencontrée: J'ai essayé à mettre des conditions pour la situation où il n'y a qu'un seul personne dans le chat, mais je n'ai pas pu trouver une solution
pour memoriser la valeur du compteur quand un nouvel terminal (client) s'ouvre. Il commence toujours avec la valeur 0 et il affiche évidement l'erreur
pour la situation d'un seul utilisateur.  J'ai essayé aussi faire le compteur dans le serveur.
