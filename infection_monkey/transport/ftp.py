import socket, threading, time
import StringIO

__author__ = 'hoffer'


class FTPServer(threading.Thread):
    def __init__(self, local_ip, local_port, files):
        self.files=files
        self.cwd='/'
        self.mode='I'
        self.rest=False
        self.pasv_mode=False
        self.local_ip = local_ip
        self.local_port = local_port
        threading.Thread.__init__(self)

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.local_ip,self.local_port))
        self.sock.listen(1)
        
        self.conn, self.addr = self.sock.accept()

        self.conn.send('220 Welcome!\r\n')
        while True:
            if 0 == len(self.files):
                break
            cmd=self.conn.recv(256)
            if not cmd: break
            else:
                try:
                    func=getattr(self,cmd[:4].strip().upper())
                    func(cmd)
                except Exception as e:
                    self.conn.send('500 Sorry.\r\n')
                    break
        
        self.conn.close()
        self.sock.close()

    def SYST(self,cmd):
        self.conn.send('215 UNIX Type: L8\r\n')
    def OPTS(self,cmd):
        if cmd[5:-2].upper()=='UTF8 ON':
            self.conn.send('200 OK.\r\n')
        else:
            self.conn.send('451 Sorry.\r\n')
    def USER(self,cmd):
        self.conn.send('331 OK.\r\n')

    def PASS(self,cmd):
        self.conn.send('230 OK.\r\n')

    def QUIT(self,cmd):
        self.conn.send('221 Goodbye.\r\n')

    def NOOP(self,cmd):
        self.conn.send('200 OK.\r\n')

    def TYPE(self,cmd):
        self.mode=cmd[5]
        self.conn.send('200 Binary mode.\r\n')

    def CDUP(self,cmd):
        self.conn.send('200 OK.\r\n')

    def PWD(self,cmd):
        self.conn.send('257 \"%s\"\r\n' % self.cwd)

    def CWD(self,cmd):
        self.conn.send('250 OK.\r\n')

    def PORT(self,cmd):
        if self.pasv_mode:
            self.servsock.close()
            self.pasv_mode = False
        l = cmd[5:].split(',')
        self.dataAddr='.'.join(l[:4])
        self.dataPort=(int(l[4])<<8)+int(l[5])
        self.conn.send('200 Get port.\r\n')

    def PASV(self,cmd):
        self.pasv_mode = True
        self.servsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.servsock.bind((self.local_ip,0))
        self.servsock.listen(1)
        ip, port = self.servsock.getsockname()
        self.conn.send('227 Entering Passive Mode (%s,%u,%u).\r\n' %
                (','.join(ip.split('.')), port>>8&0xFF, port&0xFF))

    def start_datasock(self):
        if self.pasv_mode:
            self.datasock, addr = self.servsock.accept()
        else:
            self.datasock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.datasock.connect((self.dataAddr,self.dataPort))

    def stop_datasock(self):
        self.datasock.close()
        if self.pasv_mode:
            self.servsock.close()

    def LIST(self,cmd):
        self.conn.send('150 Here comes the directory listing.\r\n')
        self.start_datasock()
        for fn in self.files.keys():
            k=self.toListItem(fn)
            self.datasock.send(k+'\r\n')
        self.stop_datasock()
        self.conn.send('226 Directory send OK.\r\n')

    def toListItem(self,fn):
        fullmode='rwxrwxrwx'
        mode = ''
        d = '-'
        ftime=time.strftime(' %b %d %H:%M ', time.gmtime())
        return d+fullmode+' 1 user group '+str(self.files[fn].tell())+ftime+fn

    def MKD(self,cmd):
        self.conn.send('257 Directory created.\r\n')

    def RMD(self,cmd):
        self.conn.send('450 Not allowed.\r\n')

    def DELE(self,cmd):
        self.conn.send('450 Not allowed.\r\n')

    def SIZE(self,cmd):
        self.conn.send('450 Not allowed.\r\n')        

    def RNFR(self,cmd):
        self.conn.send('350 Ready.\r\n')

    def RNTO(self,cmd):
        self.conn.send('250 File renamed.\r\n')

    def REST(self,cmd):
        self.pos=int(cmd[5:-2])
        self.rest=True
        self.conn.send('250 File position reseted.\r\n')

    def RETR(self,cmd):
        fn = cmd[5:-2]
        if self.mode=='I':
            fi=self.files[fn]
        else:
            fi=self.files[fn]
        self.conn.send('150 Opening data connection.\r\n')
        if self.rest:
            fi.seek(self.pos)
            self.rest=False
        data= fi.read(1024)
        self.start_datasock()
        while data:
            self.datasock.send(data)
            data=fi.read(1024)
        fi.close()
        del self.files[fn]
        self.stop_datasock()
        self.conn.send('226 Transfer complete.\r\n')

    def STOR(self,cmd):
        fn = cmd[5:-2]
        fo = StringIO.StringIO()
        self.conn.send('150 Opening data connection.\r\n')
        self.start_datasock()
        while True:
            data=self.datasock.recv(1024)
            if not data: break
            fo.write(data)
        fo.seek(0)
        self.stop_datasock()
        self.conn.send('226 Transfer complete.\r\n')
