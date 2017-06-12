import os.path, os
from ftplib import FTP
import time
import datetime
import smtplib
from email.mime.text import MIMEText

def SendMail():
    msg = MIMEText("Pre-released .mot files has been synchronized!")
    msg['Subject'] = 'Pre-Release Sync Schedule'
    me = 'prerelease@xx.com'
    you = 'rmishraxx.com'

    server = "HAWK-SVR2."
    port=25


    msg['From'] = me
    msg['To'] = you

    s = smtplib.SMTP()
    s.connect(server, port)
    s.sendmail(me, [you], msg.as_string())
    s.quit()
    

def TimeStamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
    return st


def OpenDirectory(project):
    global ftp
    global directory
    
    directory = "/Project_Data/"+project+"/04_Designs/Firmware/Firmware_Pre_Releases/Texecom"
    #print 'changing to '+ directory
    ftp.cwd(directory)

    #print 'File List: '

    #files = ftp.dir() #retrive all the directory names
    #files = ftp.retrlines('LIST') #Listing directory contents
    files = ftp.nlst() # printing name of the files..
    #print files
    return files
    
    

def downloadFirmware(files, ddir):
    global ftp
    global directory
    
    #Below code snippet is trial for searching a file to download

    for items in files:
        if items[0:2] == 'V4':
            t = directory+'/'+items
            ftp.cwd(t)
            q = ftp.nlst()
            for q in q:
                
                newDir = directory+'/'+items+'/'+q
                try:
                    ftp.cwd(newDir)
                    
                    newFiles = ftp.nlst()
                    for data in newFiles:
                        if data[-7:]== 'LS1.mot':
                            
                            path = os.path.join(ddir, data)

                    
                            if os.path.exists(path) == True:
                                print data[-16:-4]+' already exists'
                            else:
                                print 'Downloading '+data[-16:-4]
                                file = open(path, 'wb')
                                ftp.retrbinary('RETR '+data, file.write)
                                file.close()
                                #print data[-16:-4]+ ' Downloaded!'
                    ftp.cwd("..")            
                except:
                    #print "Doesn't have LPACK_0022"
                    continue    
    
def main():
    global ftp

    projects = {''}

    host = '10.60.1'
    port = 21
    userName = ''
    paswd = ''

    ftp = FTP()
    print 'Connecting to '+host
    ftp.connect(host, port)
    print 'Logging in as '+userName
    ftp.login(userName, paswd)

    #print ftp.getwelcome()

    for key in projects:
        print "opening "+key+' project'
        downloadDir = "D:\\Pre-\\"
        if not os.path.exists(downloadDir):
            os.makedirs(downloadDir)
        
        ddir = downloadDir+key
        if not os.path.exists(ddir):
            os.makedirs(ddir)
        files = OpenDirectory(projects[key])
        print "Syncing..."
        downloadFirmware(files, ddir)
        
          
        
    print "Done!"
    fo = open(downloadDir+'log.txt', 'a')
    fo.write("Last sync was done at "+TimeStamp()+'\n\n')
    fo.close()
    SendMail()
    ftp.quit() #Closing ftp connection

if __name__ == '__main__':
    main()

