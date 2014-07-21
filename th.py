


from threading import Thread
from threading import Lock
from time import sleep
from tkinter import *
import os

''' this is  multithread example code'''


lock=Lock()  #make a object named lock
threads = []  #list for thread obj
log = ''

T=0
app=0
start1=''
start2=''

#Create a Thread in Python
#Python call function within class
#race condition
class myc():
    loop=1
    count=100
    id=0  #for thread
    def __init__(self,name):
        self.name=name
        print('Constructor %s' % self.name) 

        #self.me_thread=Thread(target=self.test_run,args=())
        #self.me_thread.start()

        
    def __del__(self):
        print('Destructor %s' % self.name)
    def info(self):
        print('info %s %d %d ' % (self.name, self.loop,self.count))
    def counter(self):
        while self.loop:
            
            lock.acquire()
            
            self.count+=1;
            print("%s %d" % (self.name,self.count))
            put_text("%s %d" % (self.name,self.count))
            
            lock.release()
            sleep(0.9)
    def stop(self):
        pass
    def test_run(self):
        while 1:
            print('test running')
            sleep(2)

def put_text(s):
    log=s+'\n'
    T.insert(END, log)
    T.see('end')
def shutdown(app):
    # It is strange !!!
    # after copy global List to local List and then remove it
    '''
    a=[]
    for i in threads:
        a.append(i)
    print('tasks are %d' % len(a))

    for i in range(len(a),0,-1):
        stop_thread(a[i-1])
    '''    
    for i in range(len(threads),0,-1):
         stop_thread(threads[i-1])

    print("task are all closed")    
    put_text("task are all closed")    
    app.destroy()
    
def stop_thread(c):  # Passing by reference Okay
        
    threads.remove(c)
    print('%s removed from threads List' % c.name)
    put_text('%s removed from threads List' % c.name)
    
    c.loop=0
    c.id.join(2.0)  #timeout is  2.0 seconds 
    print('%s thread stoped' % c.name)
    put_text('%s thread stoped' % c.name)
        
def stop_1(a):
    for i in threads:
        if a==i:
            stop_thread(a)
            
            start1.set('')
            
            print('%s stop_1' % a.name)
            return
def stop_2(b):
    for i in threads:
        if b==i:
            stop_thread(b)
            start2.set('')
            print('%s stop_2' % b.name)
            return


def start_1(a):
    ''' start  thread function 'myc.counter()' 
       by pressing button 1 
    '''
    for i in threads:
        if i.name==a.name:
            print('%s already running!' % i.name)
            put_text('%s already running!' % i.name)
            return
    #print(__doc__)
    start1.set('starting1 ...')
    #print('%s start_1' % a.name)
    #print(a)
    #print(id(a))
    put_text('%s start_1' % a.name)
    #put_text(str(a))
    #put_text(str(id(a)))
    
    a.count=1
    a.loop=1
    a.id=Thread(target=a.counter,args=())
    a.id.start()
    
    threads.append(a)
def start_2(b):
    for i in threads:
        if i.name==b.name:
            print('%s already running!' % i.name)
            put_text('%s already running!' % i.name)
            return
    start2.set('starting2 ...')

    #print('%s start_2' % b.name)
    #print(b)
    #print(id(b))
    put_text('%s start_2' % b.name)
    #put_text(str(b))
    #put_text(str(id(b)))
    b.count=100
    b.loop=1
    b.id=Thread(target=b.counter,args=())
    b.id.start()
    
    threads.append(b)
def info():

    for i in threads:
        print('---- threads info ------')
        print(i)
        print(i.id)
        print('thread name: %s' % i.name)
        print('')
        
        put_text('---- threads info ------')
        put_text(str(i))
        put_text(str(i.id))
        put_text('thread name: %s' % i.name)
        put_text('--')
    

def test():
    aa=[]
    aa.append(4)
    aa.append(5)
    aa.append(6)
    print(aa)
    print('list  len:%d' % len(aa))
    for i in aa:
        print(i)

    print('---range--')
    for i in range(len(aa)):
        print(i)

    print('---end of range--')
    print(aa[0])
    print(aa[1])
    print(aa[2])

    
    for i in range(len(aa),0,-1):
        print(i-1)
        #print(aa[i])
        aa.remove(aa[i-1]) 
    print('-----------')        

    print('list  len:%d' % len(aa))
    for i in aa:
        print(i)
    return        
def stop_all():
    for i in range(len(threads),0,-1):
        print(' +%s ' % threads[i-1].name)
    stop_thread(threads[1])
    stop_thread(threads[0])
    print(' stop all')    
    return

        
    for i in range(len(threads),0,-1):
        threads[i-1].loop=0
        threads[i-1].id.join()
    print(' stop all')    
    return
    a=[]
    for i in threads:
        a.append(i)
    print('tasks are %d' % len(a))

    for i in range(len(a),0,-1):
        stop_thread(a[i-1])
    
   # stop_thread(a[1])
   # stop_thread(a[0])

def stop_app():
    app.destroy()
def main():    
    
    global T
    global app
    global start1,start2

    print('----------------------')
    print('file name:' + __file__)
    s=os.getcwd()
    print('getcwd=',s)
    #print(os.getcwd())
    s=os.path.dirname(__file__)
    print('dirname=' + s)
    print('----------------------')
    a=myc('wj')
    b=myc('hj')

    app=Tk()
    frame=Frame(app)


    b_frame=Frame(app)
    b_frame.pack(side='bottom',fill='both',expand=1) #expandable loging window

    r_frame=Frame(app)
    r_frame.pack(side='right')

    
    frame0=Frame(app)
    frame0.pack(side='top')
    
    frame1=Frame(app)
    frame1.pack()
    
    frame2=Frame(app)
    frame2.pack(side='top')
    
    frame3=Frame(app)
    frame3.pack(side='top')

    
    start1=StringVar()
    start1.set('')
    start2=StringVar()
    start2.set('')
    
    app.title('Multithread test')
    logo = PhotoImage(file='iu.gif')
    Label(r_frame,image=logo).pack(side='right')
    explanation='''    Race condition is very sensitive according to sleep().
    Sometimes thread join call has a trouble(hang up). what the hell is it?
    using join(timeout) can fix the hang up problem but the object is 
    not automatically destucted'''
    Label(frame0,text=explanation,justify=LEFT,padx=10).pack()    
    
    Button(frame1,text="start thread 1",command= lambda : start_1(a)).pack(side='left',padx=10,pady=10)
    Label(frame1,textvariable=start1).pack(side='left')
    
    Button(frame2,text="start thread 2",command=lambda: start_2(b)).pack(side='left',padx=10,pady=10)
    Label(frame2,textvariable=start2).pack(side='left')
    
    Button(frame3,text="stop thread 1",command=lambda: stop_1(a)).pack(side='top',padx=10,pady=10)
    Button(frame3,text="stop thread 2",command=lambda: stop_2(b)).pack(side='top',padx=10,pady=10)
    Button(frame3,text="Info",command=info,fg='blue').pack(side='top',padx=10,pady=10)
    Button(frame3,text="Test",command=test,fg='blue').pack(side='top',padx=10,pady=10)
    
    Button(frame3,text="Stop All",command=stop_all,fg='blue').pack(side='top',padx=10,pady=10)
    Button(frame3,text="Stop App",command=stop_app,fg='blue').pack(side='top',padx=10,pady=10)
   
    S = Scrollbar(b_frame)
    S.pack(side='right', fill='y',expand=0)

    T = Text(b_frame, height=10, bd=0)
    T.pack(side='right', fill='both',expand=1)
    S.config(command=T.yview)

    T.config(yscrollcommand=S.set)
    #T.insert('1.0', log)
    T.insert(END, log)


        
        
    app.protocol("WM_DELETE_WINDOW", lambda:shutdown(app))

    app.mainloop()  # Only window users for now

main()

'''
#http://zetcode.com/lang/python/functions/

#How can I pass arguments to Tkinter button's callback command?
#How can I pass argument to event handler ? python,tkinter porgramming
#http://stackoverflow.com/questions/3296893/how-to-pass-an-argument-to-event-handler-python-tkinter-programming
#http://www.python-course.eu/tkinter_events_binds.php


#How can I change scrollbar direction toward bottom? move mouse wheel - No!!!
##https://wikidocs.net/20

#Python does not have a preprocessor

#put text in specfic position? Okay


#http://effbot.org/tkinterbook/variable.htm

'''
'''
The Variable Classes(BooleanVar, DoubleVar,IntVar,StringVar)

'''

'''
    threading example
    https://agiliq.com/blog/2013/09/understanding-threads-in-python/


'''  
'''
    about text widget
    http://effbot.org/tkinterbook/text.htm#Tkinter.Text.bbox-method
    http://etutorials.org/Programming/Python+tutorial/Part+III+Python+Library+and+Extension+Modules/Chapter+16.+Tkinter+GUIs/16.6+The+Text+Widget/
'''

