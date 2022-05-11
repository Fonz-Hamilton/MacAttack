#!/usr/bin/python3

from pwn import *
import re

context.log_level = 'critical'

# need to change based on where you saved the file!!
sh = process('/home/fonz/midtermCTF_mac_attack')
print(sh.recv(1200))
#question = sh.recvline()
#print(question)

# print("\nlets see if this works\n")

counter = 0

while (counter < 50):

    question = sh.recvline()
    print(question)

    subjValue = 0
    objValue = 0
    subjLevel = ""
    subjCat = ""
    action = ""
    objLevel = ""
    objCat = ""
    catCheckFail = 0

    subjLevel = re.findall(b'Subject with level (.*?) and', question)[0]
    subjLevel = subjLevel.decode()

    subjCat = re.findall(b'a Subject with level [A-Z]+ and categories \{(.*?)\} [rw]', question)[0]
    subjCat = subjCat.decode()

    action = re.findall(b'\} (.*?) a+', question)[0]
    action = action.decode()

    objLevel = re.findall(b'Object with level (.*?) and', question)[0]
    objLevel = objLevel.decode()

    objCat = re.findall(b'an Object with level [A-Z]+ and categories \{(.*?)\}\?', question)[0]
    objCat = objCat.decode()

    #print("did you make it here??")

    if (subjLevel == "TS"):
        subjValue = 3
    elif (subjLevel == "S"):
        subjValue = 2
    elif (subjLevel == "C"):
        subjValue = 1
    elif (subjLevel == "UC"):
        subjValue = 0
    #print(subjValue)

    if (objLevel == "TS"):
        objValue = 3
    elif (objLevel == "S"):
        objValue = 2
    elif (objLevel == "C"):
        objValue = 1
    elif (objLevel == "UC"):
        objValue = 0
    #print(objValue)


    if (action == "read"):
            if (subjValue >= objValue):

                print("subject is greater than or equal to object and action is read")
                catCheck = 1
                # get ready for some horrible shitty code
                #if (re.search('NUC', objCat).group() == "NUC"):
                if (objCat.find("NUC") > -1):
                    #if (re.search('NUC', subjCat).group() != "NUC"):
                    if (subjCat.find("NUC") == -1):
                        catCheckFail = 1
                if (objCat.find("NATO") > -1):
                    if (subjCat.find("NATO") == -1):
                        catCheckFail = 1
                if (objCat.find("ACE") > -1):
                    if (subjCat.find("ACE") == -1):
                        catCheckFail = 1
                if (objCat.find("UFO") > -1):
                    if (subjCat.find("UFO") == -1):
                        catCheckFail = 1

                if (catCheckFail == 0):
                    print("yes, cat check passed")
                    sh.sendline(b'yes')
                else:
                    print("no, cat check failed")
                    sh.sendline(b'no')

            else:
                print("no")
                print("subject is less than the object and the action is read")

                sh.sendline(b'no')

    if (action == "write"):
            if(subjValue <= objValue):

                print("subject is less than or equal to the object and the action is write")
                if (subjCat.find("NUC") > -1):
                    if (objCat.find("NUC") == -1):
                        catCheckFail = 1
                if (subjCat.find("NATO") > -1):
                    if (objCat.find("NATO") == -1):
                        catCheckFail = 1
                if (subjCat.find("ACE") > -1):
                    if (objCat.find("ACE") == -1):
                        catCheckFail = 1
                if (subjCat.find("UFO") > -1):
                    if (objCat.find("UFO") == -1):
                        catCheckFail = 1

                if (catCheckFail == 0):
                    print("yes, cat check passed")
                    sh.sendline(b'yes')
                else:
                    print("no, cat check failed")
                    sh.sendline(b'no')


                #sh.sendline(b'yes')
            else:
                print("no")
                print("subject is greater than the object and the action is write")

                sh.sendline(b'no')

    print(sh.recvline())
    counter = counter + 1


print(sh.recv())

#sh.sendline(b'yes')


#sh.sendline(b'yes')
sh.close()
