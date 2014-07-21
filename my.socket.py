##https://wikidocs.net/20
##https://wiki.python.org/moin/UdpCommunication
#UDP hole punching

#import urllib.parse
#import urllib.request

"""
tcp/udp socket concept

"""

import socket
import time
import sys
from threading import Thread
from tkinter import *

from queue import Queue

HOST='127.0.0.1'
#HOST='175.198.124.136'
#HOST='192.168.0.37'

PORT=5007







def tcp_server(a):
	s1.set('server starting... host:%s  port:%s' % (HOST,PORT))

	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((HOST, PORT)) # You have to pass a Tuple to connect() method
	s.listen(2)  #listening  from max client =2
	connected=1
	
	while a.running:
		print('server:waiting for connection...')
		client, addr=s.accept()
		print("server:Connect acceped by" ,client ,addr)
		while connected:
			data=client.recv(1024)
			c=data.decode('UTF-8')

			##if not data: break
			put_text('SERVER:%s len:%d' % (c ,len(c)) )
			##sring must cast it to bytes(encode it)
			#if data==bytes('exit','UTF-8'): 
			##if data==b'exit': 
			if c=='exit':
				connected=0
			client.sendall(data)
			
		client.close()	
	s1.set('')
	s.close()	
	a.ready_join=1
	b3.configure(state='active')
	print('Exit server socket!')

def tcp_client(a):
	global q
	s2.set('client starting...')

	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	# You have to pass a Tuple to connect() method
	s.connect((HOST, PORT))

	while a.running:
		m=q.get()
		s.send(bytes(m,'UTF-8'))

		data=s.recv(1024)
		c=data.decode('UTF-8')
		put_text('CLIENT:%s'  % c)
		time.sleep(1)

		
	s.close()
	s.close()	
	s2.set('')
	a.ready_join=1

	print('Exit client loop!')	

def udp_server(a):
	"""
	The server needs to listen on a public ip or '0.0.0.0' to accept connections on any ip.
	The client then needs to use a public ip of the host on which the server is running
	"""

	s1.set('server starting... host:%s  port:%s' % (HOST,PORT))
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s.bind(("",PORT))
	cnt=0
	while a.running:
		cnt +=1
		put_text('[%02d]server waiting message...' % cnt)
		put_text('')

		data,addr=s.recvfrom(1024)
		d=data.decode('UTF-8')
		if d=='quit': 
			#f.close()
			#Isfile=0
			put_text('got quit')
		#print("server get data:[%s]    from %s" %(d,addr))
		put_text("server get data:[%s]    from %s" %(d,addr))

		reply='OK...'
		s.sendto(bytes(reply,'UTF-8'), addr)	
		put_text('server reply to client %s' % str(addr))
	put_text('Exit udp_server! ---')	
	s1.set('')

	s.close()	
	a.ready_join=1
	b3.configure(state='active')

def udp_client(a):
	#global s
	global q
	s2.set('client starting...')

	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	while a.running:
		#msg=input('>')
		msg=q.get()
		s.sendto(bytes(msg,'UTF-8'),(HOST,PORT))
		data, addr=s.recvfrom(1024)
		
		d=data.decode('UTF-8')
		put_text("	client get data:[%s]    from %s" %(d,addr))
	put_text('Exit udp_client! ---')	
	s.close()	
	s2.set('')
	a.ready_join=1



#--------------------------------



class myc():
	id=0  #for thread 
	running=0
	ready_join=0
	def __init__(self,name):
		self.name=name
	
	


def server_start():
	global th1
	for i in threads:
		if(i.name=='server'): return
		
	print('server running')
	a=myc('server')
	a.running=1

	print(tcp.get())
	if tcp.get()==0 :
		th1=Thread(target=udp_server,args=(a,))
	elif tcp.get()==1 :
		th1=Thread(target=tcp_server,args=(a,))
	else:
		put_text('please select tcp or udp')
		return
	th1.start()
	a.id = th1
	threads.append(a)
	
def client_start():
	global th2
	for i in threads:
		if(i.name=='client'): return

	print('client running')
	a=myc('client')
	a.running=1
	
	if tcp.get()==0 :
		th2=Thread(target=udp_client,args=(a,))
	elif tcp.get()==1 :
		th2=Thread(target=tcp_client,args=(a,))
	else:
		put_text('please select tcp or udp')
		return
		
	th2.start()
	a.id=th2
	threads.append(a)




def shutdown():
	#app.destory()
	app.quit()

def stop_threads_running():
	for i in threads:
		if(i.name=='client'):
			i.running=0
			put_text('stop thread[%s] running ' %i.name)

		if(i.name=='server'):
			i.running=0
			put_text('stop thread[%s] running ' %i.name)

def info():
	put_text('threads running=%d' % len(threads))
	for i in threads:
		put_text('	name[%s] running[%d] ready_join[%d]' % (i.name,i.running,i.ready_join))
		
def join_threads():
	for i in range(len(threads),0,-1):
		threads[i-1].id.join()
		put_text('%s joined' % threads[i-1].name)
		
	put_text('%s removed' % threads[1].name)
	put_text('%s removed' % threads[0].name)
	threads.remove(threads[1])
	threads.remove(threads[0])
	b3.configure(state='disabled')

	
def put_text(s):
    log=s+'\n'
    text0.insert(END, log)
    text0.see('end')


def client_msg_callback(event):
	'''
	Need to send get data to task using thread safe queue
	
	'''
	msg=client_msg_entry.get()
	client_msg_entry.delete(0,'end')
	q.put(msg)



'''
'''
th1=0  #thread server
th2=0   #htread client
text0=0 
log =''
threads=[] #list


q=Queue(5)

app=Tk()
app.title('tcp/udp')


s1=StringVar()
s1.set('')
s2=StringVar()
s2.set('')


# bottom frame first 
b_frame=Frame(app)
b_frame.pack(side='bottom',fill='both',expand=1) #expandable loging window

# right frame
logo=PhotoImage(file='iu.gif')
r_frame=Frame(app)
r_frame.pack(side='right')
Label(r_frame,image=logo).pack(side='right')

#0
frame0=Frame(app)
frame0.pack(side='top',fill='x',padx=5,pady=5)  #okay 
explanation='This is simple tcp/udp test'
Label(frame0,text=explanation).pack(side='left')

# Radiobutton
c_frame=Frame(app)
c_frame.pack(side='top',fill='x',padx=5)
tcp=IntVar()
#udp=IntVar()
Radiobutton(c_frame,text='tcp',variable=tcp,value=1).pack(side='left')
c1=Radiobutton(c_frame,text='udp',variable=tcp,value=0)
c1.pack(side='left')
c_frame.config(relief=GROOVE,bd=2)


#1
frame1=Frame(app)
frame1.pack(side='top',fill='x',padx=5,pady=5)  #okay 
#Label(frame,text='udp test example').pack(pady=5)

Button(frame1,text='server start',command= server_start,anchor='w').pack(side='left')
Label(frame1,text='starting...',textvariable=s1).pack(side='left')

#2
frame2=Frame(app)
frame2.pack(side='top',fill='x',padx=5,pady=5)  #okay 

Button(frame2,text='client start',command= client_start).pack(side='left',pady=5)
Label(frame2,text='starting...',textvariable=s2).pack(side='left')

#3
frame3=Frame(app)
frame3.pack(side='top',fill='x',padx=5,pady=5)  #okay 

Label(frame3,text='Client Message:').pack(side='left')
client_msg_entry=Entry(frame3)
client_msg_entry.bind("<Return>",client_msg_callback)
client_msg_entry.pack(side='left')

#4
frame4=Frame(app)
frame4.pack(side='top',fill='x',padx=5,pady=5)  #okay 

Button(frame4,text='Info',command=info).pack(side='left',padx=5,pady=5)
Button(frame4,text='stop_threads running',command=stop_threads_running).pack(side='left',padx=5,pady=5)
b3=Button(frame4,text='join threads',command=join_threads)
b3.pack(side='left',padx=5,pady=5)
b3.configure(state='disabled')







scrollbar0 = Scrollbar(b_frame)
scrollbar0.pack(side='right', fill='y',expand=0)

text0 = Text(b_frame, height=10, bd=0)
text0.pack(side='right', fill='both',expand=1)
scrollbar0.config(command=text0.yview)

text0.config(yscrollcommand=scrollbar0.set)
#T.insert('1.0', log)
text0.insert(END, log)



app.protocol('WM_DELETE_WINDOW',shutdown)

app.mainloop()


#print('Exit code!')	
#sys.exit()
	

