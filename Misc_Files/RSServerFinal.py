import time
import datetime
import socket
import threading
import os
import platform


OS=platform.system()
t1 = ''



class RSentry:

    def __init__(self,hostname=None,list_port=0,cookie=0,actflag=1,ttl=6200, next_entry=None):
        self.hostname = hostname
        self.list_port = int(list_port)
        self.cookie = cookie
        if actflag == 1 :
           self.actflag = 'Active'
        else :
            self.actflag = 'Inactive'
        self.TTL = int(ttl)
        self.ActvCnt = 1
        self.RecentlyActv = time.ctime()
        self.next_entry = next_entry
        
    def get_next(self):
        return self.next_entry

    def get_hostname(self):
        return self.hostname

    def get_cookie(self):
        return self.cookie

    def get_actflag(self):
        return self.actflag

    def get_TTL(self):
        return self.TTL

    def get_list_port(self):
        return self.list_port

    def get_ActvCnt(self):
        return self.ActvCnt

    def get_RecentlyActv(self):
        return self.RecentlyActv

    def set_next(self,new_next):
        self.next_entry = new_next

    def set_ttl(self,ttl):
        self.TTL = int(ttl)

    def set_flag(self,actflag):
        if actflag == 1 :
           self.actflag = 'Active'
        else :
            self.actflag = 'Inactive'

    def set_ActvCnt(self,ActvCnt):
        self.ActvCnt = ActvCnt

    def set_cookie(self,CookieNo):
        self.cookie = CookieNo



class LinkedList():

    def __init__(self,head=None):
        self.head=head

    def CreateEntry(self,hostname,list_port,port):
        new_entry=RSentry(hostname,list_port)
        new_entry.set_next(self.head)
        self.head=new_entry
        cookieNo= "%s:%s" % (hostname,port)
        print cookieNo
        new_entry.set_cookie(cookieNo)   
        return cookieNo

    def UpdateTTL(self,hostname):
        current = self.head
        found = False
        while current and found is False:
            if current.get_hostname() == hostname:
                found = True
                current.set_ttl(7200)
            else:
                current = current.get_next()
        if current is None:
            print "Peer not in list"

    def update_activecount_ttl(self,hostname):
        current = self.head
        found = False
        while current and found is False:
            if current.get_hostname() == hostname:
                found = True
                current.set_ttl(7200)
                current.ActvCnt = current.ActvCnt + 1
            else:
                current = current.get_next()
        if current is None:
            print "Peer not in list"


    def leave_func(self,hostname):
        current = self.head
        previous = None
        found = False
        while current and found is False:
            if current.get_hostname() == hostname:
                found = True
            else:
                previous = current
                current = current.get_next()
        current.set_flag(0)

    def Peer_Table_Send(self,hostname) :
        current = self.head
        appended_response = "P2P-DI/1.0(%^&***)200(%^&***)OK(%^&***)Hostname:(%^&***)"+hostname+"(%^&***)OS:(%^&***)"+OS
        #print current.get_actflag
        while current != None: #Scope of traversing is within the function
            if (current.get_actflag()=='Active') :
                response = str(current.get_hostname())+"(%^&***)"+str(current.get_cookie())+"(%^&***)"+str(current.get_actflag())+"(%^&***)"+str(current.get_TTL())+"(%^&***)"+str(current.get_list_port())+"(%^&***)"+str(current.get_ActvCnt())+"(%^&***)"+str(current.get_RecentlyActv())
                appended_response = str(appended_response)+"(%^&***)"+str(response)
            #print "...\n" why do you need this?
            current = current.get_next()
        return appended_response
    def peer_index_file_append(self) :
        #while current != None: #Scope of traversing is within the function
        current = self.head
        response = str(current.get_hostname())+"(%^&***)"+str(current.get_cookie())+"(%^&***)"+str(current.get_actflag())+"(%^&***)"+str(current.get_TTL())+"(%^&***)"+str(current.get_list_port())+"(%^&***)"+str(current.get_ActvCnt())+"(%^&***)"+str(current.get_RecentlyActv())
                #appended_response = str(appended_response)+"\n"+str(response)
            #print "...\n" why do you need this?
                #current = current.get_next()
        return response


    def timer_function(self):
        while True :
            time.sleep(1)
            current = self.head
            if self.head != None :
                while current != None :
                    if(current.get_TTL() > 0):
                        ttl=current.get_TTL()-1
                        current.set_ttl(ttl)
                    if (current.get_TTL()==0):
                        current.set_flag(0)
                    current = current.get_next()
    def get_head(self):
        return self.get_head

    def display(self):
        current = self.head
        print "Hostname\tCookie\t\t\tActive Flag\t\tTTL\t\tListening_Port\tRegistration Count\tMost Recent Registration\n"
        while current:
            print "%s\t%s\t%s\t\t%d\t%d\t%d\t\t\t%s\n" % (current.get_hostname(), current.get_cookie(), current.get_actflag(), current.get_TTL(), current.get_list_port(), current.get_ActvCnt(), current.get_RecentlyActv())
            current = current.get_next()

def ServerMain(connectionSocket,addr):
    global t1
    msg= connectionSocket.recv(2048)
    msg1 = str.split(msg,"(%^&***)")
    if msg1[0] == "REGISTER" and msg1[4] !="Cookie:" :
        print("Registering the Client")
        hostname = msg1[3]
        list_port= msg1[5]
        a= connectionSocket.getpeername()
        Cookie=t1.CreateEntry(hostname,list_port,a[1])
        #t1.GenerateCookie(a[0],a[1]) #Doubt
        reply = "P2P-DI/1.0(%^&***)REGISTER(%^&***)200(%^&***)OK(%^&***)Hostname:(%^&***)"+hostname+"(%^&***)Cookie:(%^&***)"+Cookie+"(%^&***)OS:(%^&***)"+OS
        connectionSocket.send(reply)
        t1.display()
        response=t1.peer_index_file_append()
        print response
        f = open('file.txt', 'a+')
        try:
            f.write(response)
        finally:
            f.close()
        connectionSocket.close()
    if msg1[0] == "REGISTER" and msg1[4] =="cookie" :
        hostname = msg1[3]
        connectionSocket.update_activecount_ttl()
        reply = "P2P-DI/1.0(%^&***)REGISTER(%^&***)200(%^&***)OK(%^&***)Hostname:(%^&***)"+hostname+"(%^&***)OS:(%^&***)"+OS
        connectionSocket.send(reply)
        t1.display()

        while current != None: #Scope of traversing is within the function
            if (current.get_actflag()=='Active') :
                response = str(current.get_hostname())+"(%^&***)"+str(current.get_cookie())+"(%^&***)"+str(current.get_actflag())+"(%^&***)"+str(current.get_TTL())+"(%^&***)"+str(current.get_list_port())+"(%^&***)"+str(current.get_ActvCnt())+"(%^&***)"+str(current.get_RecentlyActv())
                appended_response = str(appended_response)+"(%^&***)"+str(response)
            #print "...\n" why do you need this?
            current = current.get_next()
        return appended_response
        connectionSocket.close()
        #inc active Count
        #cookie

    if msg1[0] == "LEAVE" :
        print("Deleting the entry from the table")
        hostname = msg1[3]
        t1.leave_func(hostname)
        reply = "P2P-DI/1.0(%^&***)LEAVE(%^&***)200(%^&***)OK(%^&***)Hostname:(%^&***)"+hostname+"\nOS:(%^&***)"+OS
        connectionSocket.send(reply)
        t1.display()
        connectionSocket.close()
    if msg1[1] == "PEER-INDEX" :
        print("Sending Peer-Index Table")
        hostname = msg1[3]
        #reply = "P2P-DI/1.0-P_INDEX 200 OK\nHostname: "+hostname+"\nOS: "+OS+"\n"
        #connectionSocket.send(reply) #create a function with loop in Linked list, append all the elements in a string and return here.
        peer_table=t1.Peer_Table_Send(hostname)
        connectionSocket.send(peer_table)
        connectionSocket.close()
    if msg1[0] =="KEEPALIVE" :
        print("Resetting the TTL value to 7200")
        hostname = msg1[3]
        t1.UpdateTTL(hostname)
        reply = "P2P-DI/1.0(%^&***)KEEPALIVE(%^&***)200(%^&***)OK(%^&***)Hostname:(%^&***)"+hostname+"\nOS:(%^&***)"+OS
        connectionSocket.send(reply)
        t1.display()
        connectionSocket.close()



    #time.sleep(60)
    #t1.CreateEntry('10.0.128.1',65100)
    #t1.GenerateCookie('127.0.0.1')

def main():
    global t1
    t1= LinkedList()
    t = threading.Thread(target=t1.timer_function, args=())
    t.start()

    ServerSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    ServerSocket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    ServerSocket.bind( ( '192.168.1.23', 65423 ) )

    ServerSocket.listen(1)
    while True:
        connectionSocket,addr = ServerSocket.accept()
        print "Connection from: " + str(addr)
        MainThread = threading.Thread(target=ServerMain,args=(connectionSocket,addr))
        MainThread.start()





if __name__ == '__main__':
    main()
#def GenerateCookie(self):
 #       self.cookie=CookieNo

#def CalcActiveCnt(self):
  #      for i in
 #       self.ActvCnt = ActvCnt

#def DeterRecentActvTime(self):

 #       self.RecentlyActv
