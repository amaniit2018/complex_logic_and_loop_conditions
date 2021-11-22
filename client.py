import socket
import threading
import pickle
import AES
import random

g=None
n=None
b=None
sk=None

class msg:
	def __init__(self):
		self.type = ""
		self.msg = ""

msgs = {}
contact_list = []

def sender(s):
	global uni
	while True:
		somet = input()
		x = msg()
		if somet[0] == '#':
			uni = somet[1:]
			x.type = "connection"
			x.msg = name + "," + uni
		else:
			a = AES.AESCipher(str(sk))
			somet = a.encrypt(somet)
			x.type = "msg"
			x.msg = somet + "," + uni
		s.send(pickle.dumps(x))


def receiver(s):
	global uni
	global g,n,sk,b
	while True:
		m = pickle.loads(s.recv(1024))
		if m.type == "new":
			contact_list.append(m.msg)
		elif m.type == "msg":
			strc = m.msg
			stra = strc.split(":")[0]
			strb =  strc.split(":")[1]
			a = AES.AESCipher(str(sk))
			strb = a.decrypt(strb)
			print(stra+" : "+strb)
		elif m.type == "connection":
			uni = m.msg.split(':')[0]
		elif m.type == 'key':
			nos = m.msg.split(',')[0]
			n = int(nos.split(':')[0])
			g = int(nos.split(':')[1])
			st = msg()
			st.type = "p"
			b = random.randint(2,n-1)
			ln = pow(g,b,n)
			st.msg = str(ln)+','+uni
			s.send(pickle.dumps(st))
		elif m.type == "p":
			y = int(m.msg.split(':')[1])
			sk = pow(y,b,n)		
			print("connected to " + m.msg.split(':')[0])


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("127.0.0.1",12345))
#sending the name through cmd
print('If you want to connect with your friendes use # followed by his/her name')
name = input('\tPlease Enter your Nick name : ')
print("\n")
s.send(name.encode())
contact_list = pickle.loads(s.recv(4000)) #Got previous contact_list
uni = None
threading.Thread(target=receiver, args = (s,)).start()
threading.Thread(target=sender, args= (s,)).start()