"""
Le premier prgramme en Python
* utilisation des arguments de la lignne de commande
* les listes et la fonction map
* les threads
* le logger
@author Dragos STOICA
@version 0.4
@date 16.feb.2014
"""
#pun in Bonjour si queue, iar in init pun in loc de personne queue
import sys, threading, logging, os
from multiprocessing import Queue

class Bonjour(threading.Thread):
    def __init__(self, personne):
        threading.Thread.__init__(self)
        self.personne = personne
    def run(self):
        #Fonction polie - saluer une personne
        print "Bonjour %(personne)s!\n" % \
          {"personne":self.personne},
        logging.info("Bonjour : %(personne)s" %{"personne":self.personne})
   
def utilisation():
    #Affichage mode d'utilisation
    print """
          Le programme doit etre appelle avec minimum 1 argument:
          python bonjour_listes.py Dragos
          """

def main(argv=None):
    working_dir = os.path.dirname(os.path.abspath(__file__)) + os.path.sep
    #Configurez le logging pour ecrire dans un fichier texte
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        filename = working_dir + 'bonjour.log',
                        level=logging.INFO)    
    logging.info("Main start")
    
    #La boucle principale
    if argv is None:
        argv = sys.argv

    if len(argv) == 1:
        utilisation()
    else:
        #Creation des filles d'attente
        tasks_queue = Queue()
        started_queue = Queue()
        
        #Argument 1 est le nom de fichier avec un noms per ligne
        mmeThread = []
        mThread = []
        mlleThread = []
        with open(working_dir + argv[1],'r') as f:
            #Dites bonjour a chaque personne de fichier
            for ligne in f:
                if ligne[0:2] == "M.":
                    #in loc de append pun put in queue
                    mThread.append(Bonjour(ligne.strip(' \r\n')))
                elif ligne[0:4] == "Mme.":
                    mmeThread.append(Bonjour(ligne.strip(' \r\n')))
                elif ligne[0:5] == "Mlle.":
                    mlle_local = Bonjour(ligne.strip(' \r\n'))
                    mlleThread.append(mlle_local)
                    mlle_local.start()

        for mlle in mlleThread:
            tasks_queue.put(mlle) 
            tasks_queue.get().join()
            
        for mme in mmeThread:
            tasks_queue.put(mme)
            tasks_queue.get().start()
            started_queue.put(mme)
            started_queue.get().join()
        for m in mThread:
            tasks_queue.put(m)
            tasks_queue.get().start()
            started_queue.put(m)
            started_queue.get().join()
        
    logging.info("Main stop")                
    return 0

if __name__ == "__main__":
    #Simplifiez la logique de la fonction principale
    sys.exit(main())
