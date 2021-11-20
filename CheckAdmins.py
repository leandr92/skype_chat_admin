import re
import os
import Skype.skype_manager as SkypeManager
import time

chatsFileName = "chat.txt"

if os.path.exists(chatsFileName):

    f = open(chatsFileName)

    user = ""
    password = ""

    skype = SkypeManager.SkypeManager()
    skype.connect(user, password)

    for line in f:

        colArray = line.split(";")

        if colArray[0] != "":
            chatId = colArray[0]

        regex = r".*\(|\).?|\n"
        chatId = re.sub(regex, "", chatId, 0, re.MULTILINE)
            
        chat = skype.chats[chatId]
            
        print("чат " + chat.topic)            
            
        for user in chat.admins:  
            print(user.name)

    f.close()

else:
    print("Файл не доступен admins.txt")
