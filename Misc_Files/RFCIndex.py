import socket
import threading
import os
import platform
import time


ReqRFC_list = []
SERVER_NAME = '' 
SERVER_PORT = 0
HOST = socket.gethostbyname(socket.gethostname())
LISTENING_PORT = 40000 
OS = platform.system()
FilePath = ''
Cookieval = ''


class Peer_entry:

    def __init__(self,hostname,cookie,actflag,ttl,port,actvcnt,recentlyactv,next_entry=None):
        self.hostname = hostname
        self.cookie = cookie
        self.actflag = actflag
        self.TTL = int(ttl)
        self.list_port = int(port)
        self.ActvCnt = int(actvcnt)
        self.RecentlyActv = recentlyactv
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

    def set_hostname(self,hostname):
        self.hostname = hostname

    def set_list_port(self,port):
        self.list_port = port

    def set_cookie(self,CookieNo):
        self.cookie = CookieNo
        
    def set_actflag(self,actflag):
        self.actflag = actflag

    def set_TTL(self,ttl):
        self.TTL = ttl

    def set_ActvCnt(self):
        self.ActvCnt = actvcnt

    def set_RecentlyActv(self):
        self.RecentlyActv = recentlyactv
      

class Peer_Index():

    def __init__(self,head=None):
        self.head = head

    def get_head(self):
        return self.head

    def set_head(self,head):
        self.head = head

    def CreateEntry(self,hostname,cookie,actflag,ttl,port,actvcnt,recentlyactv):
        new_entry = Peer_entry(hostname,cookie,actflag,ttl,port,actvcnt,recentlyactv)
        new_entry.set_next(self.head)
        self.head = new_entry
          
    def GetPort(self,hostname):
        current = self.head
        while current != None:
            if current.hostname == hostname:
                return current.get_list_port()
            current = current.get_next()
        print "ERROR! No Port found for %s\n" %(hostname)
    
    def Display(self):
        current = current.head
        print "Hostname\tCookie\tActive Flag\tTTL\tListening Port\tRegistration count\tRecent Registration time\n"
        while current != None:
            print "%s\t%s\t%s\t%d\t%d\t\t%d\t\t%s" %(current.hostname,current.cookie,current.actflag,current.TTL,current.list_port,current.actvcnt,current.recentlyactv)
            current = current.next_entry


            

class RFC_Entry():

    def __init__(self,RFCno=0,RFCtitle='',hostname=socket.gethostbyname(socket.gethostname()),ttl=7200,next_entry=None):

        self.RFCno = int(RFCno)
        self.RFCtitle = str(RFCtitle)
        self.hostname = str(hostname)
        self.TTL = int(ttl)
        self.next_entry = next_entry

    def get_next(self):
        return self.next_entry

    def get_RFCno(self):
        return self.RFCno

    def get_RFCtitle(self):
        return self.RFCtitle

    def get_hostname(self):
        return self.hostname

    def get_TTL(self):
        return self.TTL

    def set_next(self,new_next):
        self.next_entry = new_next

    def set_ttl(self,ttl):
        self.TTL = ttl



class RFC_Index():

    def __init__(self,head=None):
        self.head = head
    
    def get_head(self):
        return self.head

    def CreateEntry(self,RFCno,RFCtitle,hostname,ttl):
        new_entry = RFC_Entry(RFCno,RFCtitle,hostname,ttl)
        current = self.head
        while current.next_entry != None:
            current = current.next_entry
        current.next_entry = new_entry

    def LocalRFC_Search(self,RFCno):                #Create required RFC list
        current = self.head                         #Create socket to RS if not present
        while current != None:
            if current.hostname == HOST:
                if current.RFCno == RFCno:
                    print "RFC %d is already present on the system\n" %(RFCno)
                    return True
            current = current.next_entry
        print "Contacting RS server for obtaining RFC %d......\n" %(RFCno)
        return False


    def Check_DuplicateEntry(self,RFCno,hostname):      #Check for duplicate entry before appending peer RFC Index to local Index
            current = self.head
            while current != None:
                if current.RFCno == RFCno and current.hostname == hostname:
                    return True             
                else:
                    current = current.next_entry
            return False

    def SearchRFC_Index(self,RFCno):                    #Search for required RFC in final RFC Index
        current = self.head                             #Search each peer's RFC list
        ststus = False
        print "Searching Merged RFC-Index....\n"
        while current != None:
            if current.hostname != HOST:
                if current.RFCno == RFCno:
                    status = True
                    return (status,current.hostname)
            current = current.next_entry
        print " RFC %d is not found !\n"
        return (status,None) 

   #def UpdateRFC_List():           #Update RFC Index and local file list


    def GenerateIndex_Response(self):
        global HOST
        global OS
        current = self.head
        message = "P2P-DI/1.0(%^&***)200(%^&***)OK(%^&***)Host:(%^&***)"+HOST+"(%^&***)OS:(%^&***)"+OS  
        while current != None:
            data = str(current.get_RFCno())+'(%^&***)'+str(current.get_RFCtitle())+'(%^&***)'+str(current.get_hostname())+'(%^&***)'+str(current.get_TTL())
            message = message +"(%^&***)"+data
            print "...\n"
            current = current.next_entry
        return message
    



            
def Get_LocalFile_List():                       #Create entries for local files
        global FilePath                         #Write local file list to a file
        files = []
        for file in os.listdir(FilePath):
            if file.endswith(".txt"):
                files.append(os.path.splitext(file)[0])
        return files     

    

def ServerMain(csocket,addr,object):
        global FilePath
        global HOST
        global OS
        msg = csocket.recv(1024)
        message = str.split(msg,"(%^&***)")
        if message[0] == 'GET':
            if message[1] == 'RFC-INDEX':
                response = object.GenerateIndex_Response()
                print "Sending RFC-INDEX to %s.....\n" %(str(addr))
                csocket.send(response)
                print "Finished sending RFC-Index to %s\n" %(str(addr))
            elif message[1] == 'RFC':                                       
                os.chdir(FilePath)   #Changes CWD to 'CWD\IP_Project' 
                print "Sending RFC %s to %s......\n" %(message[2],str(addr))
                response = "P2P-DI/1.0(%^&***)200(%^&***)OK(%^&***)Host:(%^&***)"+HOST+"(%^&***)OS:(%^&***)"+OS
                #socket.send(response)
                filename = str(message[2])+".txt"
                if os.path.isfile(filename):
                    with open(filename,"r") as f:
                        #response = f.read(1024)
                        #socket.send(response)
                        #while response != "":
                            filedata = f.read()
                            response = response +"(%^&***)"+filedata
                            csocket.send(response)
                    print "Finished sending RFC %s to %s\n" %(message[2],str(addr))
        csocket.close()

                
def ServerModule(object):

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_socket.bind((HOST,LISTENING_PORT))

    server_socket.listen(25)
    while True:
        client_socket,addr = server_socket.accept()
        print "Connection from: " + str(addr)
        MainThread = threading.Thread(target=ServerMain(),args=(client_socket,addr,object))
        MainThread.start()


def Generate_KeepAlive():
    global SERVER_NAME
    global SERVER_PORT
    global HOST
    global OS
    global Cookieval
    KAsock = socket.socket()
    KAsock.connect((SERVER_NAME,SERVER_PORT))
    
    while True:
        time.sleep(300)
        message = "KEEPALIVE(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)"+HOST+"(%^&***)Cookie:(%^&***)"+Cookieval+"(%^&***)OS:(%^&***)"+OS
        KAsock.send(message)

    KAsock.close()
        

#def ClientModule():
    



def main():
    
    global SERVER_NAME
    global SERVER_PORT
    global HOST
    global LISTENING_PORT
    global OS
    global ReqRFC_list
    global FilePath
    global Cookieval
    
    wd = os.getcwd()
    if OS == "Windows":
        directory = wd+"\IP_Project"
    else:
        directory = wd+"/IP_Project"
    if not os.path.exists(directory):
        os.makedirs(directory)

    FilePath = directory
    os.chdir(FilePath)
    
    
    RFCtable = RFC_Index()
    Peertable = Peer_Index()
    
    print "Hello"
    #MainThread = threading.Thread(target=ServerModule(),args=(RFCtable))
    #MainThread.start()
    print "Hello again"

    
    SERVER_NAME = '127.0.0.1'
    SERVER_PORT = 65423
    Cookieval = None

    s = socket.socket()
    s.connect((SERVER_NAME,SERVER_PORT))
    print "SERVER CONNECT"
    if os.path.isfile("Cookie.txt"):
        with open("Cookie.txt","r") as f:
            Cookieval = f.read()
    else:
        Cookieval = None
      
    if Cookieval != None:
        message = "REGISTER(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)"+HOST+"(%^&***)Cookie:(%^&***)"+Cookeival+"(%^&***)Port:(%^&***)"+str(LISTENING_PORT)+"(%^&***)OS:(%^&***)"+OS
    else:
        message = "REGISTER(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)"+HOST+"(%^&***)Port:(%^&***)"+str(LISTENING_PORT)+"(%^&***)OS:(%^&***)"+OS
    s.send(message)
    rep = s.recv(1024)
    reply = str.split(rep,"(%^&***)")
    if reply[1] == "200" and reply[2] == "OK":
        print "Peer %s registered with RS\n" %(str(s.getsockname()))
        Cookieval = str(reply[4])
        f = open("Cookie.txt","w+")
        f.write(Cookieval)
        f.close()
    s.close()

    Keep_AliveThread = threading.Thread(target=Generate_KeepAlive(),args=())
    Keep_AliveThread.start()

    localfiles = Get_LocalFile_List()
    if not localfiles:
        print "No RFCs on localhost\n"
    else:
        print "Updating local RFCs to RFC-Index..\n"
        for files in localfiles:
            RFCtable.CreateEntry(files,'',HOST,7200)
    start_time_cummulative = time.time()      
    for RFCno in ReqRFC_list:
        status = RFCtable.LocalRFC_Search(RFCno)
        if status == False:
            start_time_each = time.time()
            s = socket.socket()
            s.connect((SERVER_NAME,SERVER_PORT))
            message = "GET(%^&***)PEER-INDEX(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)"+HOST+"(%^&***)Cookie:(%^&***)"+Cookieval+"(%^&***)OS:(%^&***)"+OS
            print "Requesting Peer-Index from RS....\n" 
            s.send(message)
            rep = s.recv(4096)
            reply = str.split(rep,"(%^&***)")
            if reply[1] == "200" and reply[2] == "OK":
                Peertable.set_head(None)             # To CHECK!!
                idx = 7
                while (idx < len(reply)):
                    Peertable.CreateEntry(reply[idx],reply[idx+1],reply[idx+2],reply[idx+3],reply[idx+4],reply[idx+5],reply[idx+6])
                    idx = idx + 7
                    print "...\n"
                print "Peer-Index successfully downloaded on %s" %(str(s.getsockname()))
            s.close()
            
            current = Peertable.get_head()
            while current != None:
                if current.hostname != HOST:
                    peername = current.get_hostname()
                    peerport = current.get_list_port()
                    s = socket.socket()
                    s.connect((peername,peerport))
                    message = "GET(%^&***)RFC-INDEX(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)"+HOST+"(%^&***)OS:(%^&***)"+OS
                    print "Requesting RFC-Index from Peer %s:%s....\n" %(peername,str(peerport))
                    s.send(message)
                    rep = s.recv(4096)
                    reply = str.split(rep,"(%^&***)")
                    if reply[1] == "200" and reply[2] == "OK":
                        idx = 7
                        while (idx < len(reply)):
                            res = RFCtable.Check_DuplicateEntry(reply[idx],reply[idx+2])
                            if res == False:
                                RFCtable.CreateEntry(reply[idx],reply[idx+1],reply[idx+2],reply[idx+3])
                            idx = idx + 4
                            print "...\n"
                        print "RFC-Index successfully downloaded on %s\n" %(str(s.getsockname()))
                    else:
                        print "ERROR while downloading RFC-Index from peer %s:%s\n" %(peername,str(peerport))
                    s.close()
                    
                    (status,peername)= SearchRFC_Index(RFCno)
                    if status == True:
                        peerport = Peertable.GetPort(peername)
                        s = socket.socket()
                        s.connect((peername,peerport))
                        message = "GET(%^&***)RFC(%^&***)"+RFCno+"(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)"+HOST+"(%^&***)OS:(%^&***)"+OS
                        print "Requesting RFC %d from peer %s:%s..\n" %(RFCno,peername,str(peerport))
                        s.send(message)
                        rep = s.recv(4096)
                        reply = str.split(rep,"(%^&***)")
                        if reply[1] == "200" and reply[2] == "OK":
                            idx = 7
                            filename = str(RFCno)+".txt"
                            f = open(filename,"w+")
                            f.write(reply[7])
                            f.close()
                            end_time_each = time.time()
                            print "RFC %d successfully downloaded!\n" %(RFCno) 
                            s.close()    
                            break
                        s.close()
                final_time_each = end_time_each - start_time_each
                f = open("Timer.txt","a+")
                try:
                    f.write("\nThe time taken for obtaining RFC "+str(RFCno)+": "+str(final_time_each))
                finally:
                    f.close()
                current = current.get_next()
            if current == None:
                print "RFC %d is not present with any peer\n" %(RFCno)

    end_time_cumulative = time.time()
    final_time_cumulative = end_time_cumulative - start_time_cumulative
    f = open("Timer.txt","a+")
    try:
        f.write("\nThe cumulative time taken for obtaining all required RFCs: "+str(final_time_cumulative))
    finally:
        f.close()
    print "Completed searching for all required RFCs\n"
    s = socket.socket()
    s.connect((SERVER_NAME,SERVER_PORT))
    message = "LEAVE(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)"+HOST+"(%^&***)Cookie:(%^&***)"+Cookieval+"(%^&***)OS:(%^&***)"+OS
    s.send(message)
    rep = s.recv(1024)
    reply = str.split(rep,"(%^&***)")
    if reply[1] == "200" and reply[2] == "OK":
        print "Leaving the peer network...BYE :("
        s.close()
    
           

    
    
         
        
    
if __name__ == '__main__':
    main()
    
