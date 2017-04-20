from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import cgi
import Queue

PORT_NUMBER = 8000

#This class will handles any incoming request from the browser 
class myHandler(BaseHTTPRequestHandler):

	def __init__(self, nsa_queue, *args):
		self.nsa_queue = nsa_queue
		BaseHTTPRequestHandler.__init__(self, *args)

	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"

		try:
			#Check the file extension required and set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
	#Handler for the POST requests
	def do_POST(self):
		if self.path=="/send":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

            		crypt_text = cryptage_caesar(form["le_texte"].value, 3) #On prend le text du index.html pour le crypter.
			self.nsa_queue.put(crypt_text) #On ajoute le texte dans la fille d'attente pour qu'il peuve etre decrypte. 
			print "Le texte en clair: %s" % form["le_texte"].value
			self.send_response(200)
			self.end_headers()
			self.wfile.write(crypt_text)
			return			

		if self.path=="/decrypt":
			le_texte = self.nsa_queue.get() #On prend le texte de la fille d'attente pour le decrypter.
            		decryptage = decryptage_caesar(le_texte, 3) #On fait le decrpytage du texte 
			print "Le texte en encode: %s" % le_texte
			self.send_response(200)
			self.end_headers()
			self.wfile.write("Le texte intercepte: %s." % le_texte) #On affiche le texte crypte
			self.wfile.write(" Le texte decode: %s" % decryptage) ##On affiche le texte decrypte
			return			

def cryptage_caesar(plaintext,shift):

	alphabet=["a","b","c","d","e","f","g","h","i","j","k","l",
	"m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

	#Creation d'un dictionaire 
	dic={}
	for i in range(0,len(alphabet)):
		dic[alphabet[i]]=alphabet[(i+shift)%len(alphabet)]

	#Changer chaque lettre du plaintext dans la lettre crypte correspondante dans le dictionaire, en creant le cryptext
	ciphertext=""
	for l in plaintext.lower():
		if l in dic:
			l=dic[l]
		ciphertext+=l

	return ciphertext    

def decryptage_caesar(plaintext,shift):

	alphabet=["a","b","c","d","e","f","g","h","i","j","k","l",
	"m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

	#Creation d'un dictionaire 
	dic={}
	for i in range(0,len(alphabet)):
		dic[alphabet[i]]=alphabet[(i-shift)%len(alphabet)]

	ciphertext=""
	for l in plaintext.lower():
		if l in dic:
			l=dic[l]
		ciphertext+=l

	return ciphertext             
			
try:
	nsa_queue = Queue.Queue()

	def handler(*args):
		myHandler(nsa_queue, *args)
	
	#Create a web server and define the handler to manage the incoming request
	server = HTTPServer(('', PORT_NUMBER), handler)
	print 'Started httpserver on port ' , PORT_NUMBER
	#Wait forever for incoming http requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
