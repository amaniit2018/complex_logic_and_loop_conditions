import socket
import threading
import pickle
import primitive_root as pr
import getprime as gp


class msg:
	def __init__(self):
		self.type = ""
		self.msg = ""

class contact:
	def __init__(self):
		self.name = ""
		self.PORT = ""
		self.sock = None

def handle(a, sock, addr):
	global contacts
	while True:
		maka = pickle.loads(sock.recv(1024))
		saki = maka.msg
		print(saki.split(',')[0], "from ", addr,a.name)
		saki, to = saki.split(',')
		for i in contacts:
			if i.name == to:
				break
			# else:
			# 	print("INVALID NAME")
		r = msg()
		if maka.type == "connection":
			
			r.type = "connection"
			
			r.msg = a.name + ":"+ saki.split(',')[0]
			i.sock.send(pickle.dumps(r))


			name1, name2 = maka.msg.split(',')
			var = msg()
			var.type = 'key'
			n = gp.funct()
			g = pr.findPrimitive(n)
			print('n : ',n,'     g : ',g,'\n')
			var.msg = str(n)+':'+str(g)+','+name1
			for j in contacts:
				if j.name == name1:
					break

			j.sock.send(pickle.dumps(var))
			var.msg = str(n)+':'+str(g)+','+name2

			for j in contacts:
				if j.name == name2:
					break

			j.sock.send(pickle.dumps(var))	
		elif maka.type == "p":
			r.type = "p"
			r.msg = a.name+":"+saki.split(',')[0]
			i.sock.send(pickle.dumps(r))
		else:
			r.type = "msg"
			r.msg = a.name + ":"+ saki.split(',')[0]
			i.sock.send(pickle.dumps(r))
			
		


IP = "127.0.0.1"
PORT = 12345

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind((IP,PORT))
s.listen(5)
contacts = []
shared_contacts = []
while True:
	sock, addr = s.accept()
	print("Got connection from ", addr)
	a = contact()
	a.name = sock.recv(1024).decode()
	print("Nick name : ",a.name)
	a.PORT = addr[1]
	a.sock = sock
	# Sending all the previous contacts
	sock.send(pickle.dumps(shared_contacts))
	shared_contacts.append(a.name)
	## sending broad cast to add new client to their contact_list
	for i in contacts:
		d = msg()
		d.type = "new"
		d.msg = a.name
		i.sock.send(pickle.dumps(d))
	contacts.append(a) #appending the new contact to contact_list

	print("Starting thread for this connection....\n")
	x = threading.Thread(target = handle, args = (a, sock, addr,))
	x.start()