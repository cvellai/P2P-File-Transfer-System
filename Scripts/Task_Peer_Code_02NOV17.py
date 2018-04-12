import socket
import threading
import shlex
import os
import platform
import time


ReqRFC_list = [8127, 8181, 8187, 8189, 8191, 8193, 8194, 8204, 8205, 8206, 8207, 8208, 8209, 8210, 8211, 8213, 8214, 8215, 8216, 8218, 8219, 8220, 8221, 8223, 8227, 8228, 8229, 8230, 8231, 8232, 8233, 8234, 8235, 8236, 8238, 8239, 8240, 8241, 8242, 8243, 8244, 8245, 8246, 8247, 8248, 8249, 8250, 8251, 8252, 8253]
SERVER_NAME = '' 
SERVER_PORT = 65423
HOST = socket.gethostbyname(socket.gethostname())
LISTENING_PORT = 40000
OS = platform.system()
FilePath = ''
Cookieval = None


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

    def GetPort(self,hostname):                     #To obtain listening port of peer from Peer-Index
        current = self.head
        while current != None:
            if current.hostname == hostname:
                return current.get_list_port()
            current = current.get_next()
        print "ERROR! No Port found for %s\n" %(hostname)

    def Display(self):
        current = self.head
        print "Peer-Index:--->"
        print "Hostname\tCookie\tActive Flag\tTTL\tListening Port\tRegistration count\tRecent Registration time\n"
        while current != None:
            print "%s\t%s\t%s\t%d\t%d\t\t%d\t\t%s" %(current.hostname,current.cookie,current.actflag,current.TTL,current.list_port,current.ActvCnt,current.RecentlyActv)
            current = current.next_entry




class RFC_Entry():

    def __init__(self,RFCno=0,RFCtitle='',hostname=socket.gethostbyname(socket.gethostname()),ttl=7200,next_entry=None):

        self.RFCno = str(RFCno)
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

    def set_TTL(self,ttl):
        self.TTL = ttl



class RFC_Index():

    def __init__(self,head=None):
        self.head = head

    def get_head(self):
        return self.head

    def CreateEntry(self,RFCno,RFCtitle,hostname,ttl):
        new_entry=RFC_Entry(RFCno,RFCtitle,hostname,ttl)
        new_entry.set_next(self.head)
        self.head=new_entry
        #new_entry =
        #current = self.head
        #while current.get_next() != None:
            #current = current.next_entry
        #current.set_next(new_entry)

    def LocalRFC_Search(self,RFCno):                #To check whether the required RFC is present on the local system before contacting RS
        global HOST               
        current = self.head                         
        while current != None:
            if current.hostname == HOST:
                if current.RFCno == str(RFCno):
                    print "RFC %d is already present on the system\n" %(RFCno)
                    return True
            current = current.next_entry
        print "Contacting RS server for obtaining RFC %d......\n" %(RFCno)
        return False


    def Check_DuplicateEntry(self,RFCno,hostname):      #To Check for duplicate entry before appending peer RFC Index to local Index
            current = self.head
            while current != None:
                if current.RFCno == str(RFCno) and current.hostname == hostname:
                    return True
                else:
                    current = current.next_entry
            return False

    def SearchRFC_Index(self,RFCno):                    #To search the merged RFC-Index for the required RFC
        current = self.head                             
        status = False
        print "Searching Merged RFC-Index....\n"
        while current != None:
            if current.hostname != HOST:
                if current.RFCno == str(RFCno):
                    status = True
                    return (status,current.hostname)
            current = current.next_entry
        print " RFC %d is not found !\n" %(RFCno)
        return (status,None)

    def UpdateRFC_List(self):           #Update RFC Index local file list
        current = self.head
        entry = str(current.get_RFCno())+"\t"+str(current.get_RFCtitle())+"\t"+str(current.get_hostname())+"\t"+str(current.get_TTL())+"\n"
        return entry

    def display(self):
       current = self.head
       print "RFC-Index\n"
       while current != None:
           print "%s\t%s\t%s\t%d" % (current.RFCno,current.RFCtitle,current.hostname,current.TTL)
           current=current.next_entry

    def GenerateIndex_Response(self):       #To send across the whole RFC-Index
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





def Get_LocalFile_List():                    #To obtain list of RFCs already present on localhost
        global FilePath                         
        files = []
        count = 0
        for file in os.listdir(FilePath):
            if file.startswith("8"):
                count += 1
                files.append(os.path.splitext(file)[0])
        return (files,count)

def Get_FileTitle():                        #To obtain RFC titles of local RFCs
    global FilePath
    title = []
    start = 0
    end = 0
    for file in os.listdir(FilePath):
            if file.startswith("8"):
                f = open(file,"r")
                contents = f.read()
                f.close()
                contents = str(contents)+'\''
                c = shlex.split(contents)
                elem = 0
                count = 0
                for elem in c:
                    if elem == "2017":
                        start = count
                        break
                    count += 1
                elem = 0
                count = 0
                for elem in c:
                    if elem == "Abstract":
                        end = count
                        break
                    count += 1
                hd = ''
                for elem in range(start+1,end):
                    hd = hd +" "+c[elem]
                title.append(hd)
    return title



def ServerMain(socket,addr,object):
        global FilePath
        global HOST
        global OS
        msg = socket.recv(1024)
        message = str.split(msg,"(%^&***)")
        if message[0] == 'GET':
            if message[1] == 'RFC-INDEX':
                print "Sending RFC-INDEX to %s.....\n" %(str(addr))
                response = object.GenerateIndex_Response()
                socket.send(response)
                print "Finished sending RFC-Index to %s\n" %(str(addr))
            elif message[1] == 'RFC':
                os.chdir(FilePath)              #Changes CWD to 'CWD\IP_Project'
                print "Sending RFC %s to %s......\n" %(message[2],str(addr))
                response = "P2P-DI/1.0(%^&***)200(%^&***)OK(%^&***)Host:(%^&***)"+HOST+"(%^&***)OS:(%^&***)"+OS
                filename = str(message[2])+".txt"
                if os.path.isfile(filename):
                    with open(filename,"r") as f:
                            filedata = f.read()
                            response = response +"(%^&***)"+filedata
                            socket.send(response)
                    print "Finished sending RFC %s to %s\n" %(message[2],str(addr))
        socket.close()


def ServerModule(object):
    global HOST
    global LISTENING_PORT
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_socket.bind((HOST,LISTENING_PORT))

    server_socket.listen(25)
    print "Starting server.....\n"
    while True:
        client_socket,addr = server_socket.accept()
        print "Connection from: " + str(addr)
        MainThread = threading.Thread(target=ServerMain,args=(client_socket,addr,object,))
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
        time.sleep(1)
        message = "KEEPALIVE(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)"+HOST+"(%^&***)Cookie:(%^&***)"+str(Cookieval)+"(%^&***)OS:(%^&***)"+OS
        print "\nKEEP ALIVE!!!!\n"
        KAsock.send(message)
    KAsock.close()

def Leave_Func():
    global SERVER_NAME
    global SERVER_PORT
    global HOST
    global OS
    global Cookieval
    s = socket.socket()
    s.connect((SERVER_NAME,SERVER_PORT))
    message = "LEAVE(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)"+HOST+"(%^&***)Cookie:(%^&***)"+str(Cookieval)+"(%^&***)OS:(%^&***)"+OS
    s.send(message)
    rep = s.recv(1024)
    reply = str.split(rep,"(%^&***)")
    if reply[1] == "200" and reply[2] == "OK":
        print "Leaving the peer network...BYE :("
    return s





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

    #SERVER_NAME = '10.25.5.217'
    #SERVER_PORT = 65423
    #Cookieval = None

    f1 = open("RFC_Index.txt","w+")
    f1.write("\nRFC NUMBER\tRFC TITLE\tHOSTNAME\tTTL\n")
    f1.close()
    
    s = socket.socket()
    s.connect((SERVER_NAME,SERVER_PORT))
    if os.path.isfile("Cookie.txt"):
        with open("Cookie.txt","r") as f:
            Cookieval = f.read()
    else:
        Cookieval = None
    
    if Cookieval != None:
        message = "REGISTER(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)"+HOST+"(%^&***)Cookie:(%^&***)"+str(Cookieval)+"(%^&***)Port:(%^&***)"+str(LISTENING_PORT)+"(%^&***)OS:(%^&***)"+OS
    else:
        message = "REGISTER(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)"+HOST+"(%^&***)Port:(%^&***)"+str(LISTENING_PORT)+"(%^&***)OS:(%^&***)"+OS
    s.send(message)
    rep = s.recv(1024)
    reply = str.split(rep,"(%^&***)")
    if reply[1] == "200" and reply[2] == "OK":
        print "Peer %s registered with RS\n" %(str(s.getsockname()))
        Cookieval = str(reply[4])
        s.close()
        f = open("Cookie.txt","w+")
        f.write(Cookieval)
        f.close()
    Keep_AliveThread = threading.Thread(target=Generate_KeepAlive,args=())
    Keep_AliveThread.daemon = True
    Keep_AliveThread.start()

    (localfiles,count) = Get_LocalFile_List()
    if not localfiles:
        print "No RFCs on localhost\n"
    else:
        print 'RFCs on local system:\n'
        for i in localfiles :
            print i
        title = Get_FileTitle()
        print "Updating local RFCs to RFC-Index..\n"
        for idx in range(0,count):
            RFCtable.CreateEntry(localfiles[idx],title[idx],HOST,7200)
            entry = RFCtable.UpdateRFC_List()
            os.chdir(FilePath)
            f = open("RFC_Index.txt", "a+")
            try:
                f.write(entry)
            finally:
                f.close()
    MainThread = threading.Thread(target=ServerModule,args=(RFCtable,))
    MainThread.start()
    time.sleep(20)
    start_time_cumulative = time.time()
    RFCtable.display()
    for RFCno in ReqRFC_list:
        status = RFCtable.LocalRFC_Search(RFCno)
        if status == False:
            start_time_each = time.time()
            s = socket.socket()
            s.connect((SERVER_NAME,SERVER_PORT))
            message = "GET(%^&***)PEER-INDEX(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)"+HOST+"(%^&***)Cookie:(%^&***)"+str(Cookieval)+"(%^&***)OS:(%^&***)"+OS
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
                print "Peer-Index successfully downloaded on %s\n" %(str(s.getsockname()))
            elif reply[1] == "404" and reply[2] == "ERROR":
                print "ERROR: %s!\n" %(str(reply[7]))
                Peertable.Display()
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
                                entry = RFCtable.UpdateRFC_List()
                                os.chdir(FilePath)
                                f = open("RFC_Index.txt", "a+")
                                try:
                                    f.write(entry)
                                finally:
                                    f.close()
                            idx = idx + 4
                            print "...\n"
                        print "RFC-Index successfully downloaded on %s\n" %(str(s.getsockname()))
                    else:
                        print "ERROR while downloading RFC-Index from peer %s:%s\n" %(peername,str(peerport))
                    s.close()

                    (status,peername)= RFCtable.SearchRFC_Index(RFCno)
                    if status == True:
                        peerport = Peertable.GetPort(peername)
                        s = socket.socket()
                        s.connect((peername,peerport))
                        message = "GET(%^&***)RFC(%^&***)"+str(RFCno)+"(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)"+HOST+"(%^&***)OS:(%^&***)"+OS
                        print "Requesting RFC %d from peer %s:%s..\n" %(RFCno,peername,str(peerport))
                        s.send(message)
                        rep = s.recv(204800)
                        reply = str.split(rep,"(%^&***)")
                        if reply[1] == "200" and reply[2] == "OK":
                            idx = 7
                            filename = str(RFCno)+".txt"
                            f = open(filename,"w+")
                            f.write(reply[7])
                            f.close()
                            end_time_each = time.time()
                            print "RFC %d successfully downloaded!\n" %(RFCno)
                            final_time_each = end_time_each - start_time_each
                            f = open("Timer.txt","a+")
                            try:
                                f.write("\nThe time taken for obtaining RFC "+str(RFCno)+": "+str(final_time_each))
                            finally:
                                f.close()
                            s.close()
                            break
                        s.close()
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
    print "\nCompleted searching for all required RFCs\n"
    while True:
        userinput = raw_input("Leave or stay??\n")
        if userinput == "leave":
            LeaveSock = Leave_Func()
            break
        elif userinput == "stay":
            print "Waiting before closing server....\n"
            time.sleep(60)
    
    Keep_AliveThread.join()
    MainThread.join(10)
    LeaveSock.close()





if __name__ == '__main__':
    main()
