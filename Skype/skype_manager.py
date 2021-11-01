from skpy import Skype
import time
from skpy import SkypeAuthException
from skpy import SkypeApiException
import skpy

class SkypeManager():

    user = ""
    _sk = Skype()
    chats = _sk.chats
    _tokenFile = ""

    def __init__(self):
        super(SkypeManager, self).__init__()

    def connect(self, user, password):

        self.user = user
        self._tokenFile = self.user + ".tokens-app";
        self._sk.conn.setTokenFile(self._tokenFile)

        try:
            self._sk.conn.readToken()
        except SkypeAuthException:
            print("пытаюсь подключиться")
            if not self._sk.conn.connected: 
                
                self._sk.conn.setUserPwd(self.user, password)
                tryCount = 10
                i = 0
                while not self._sk.conn.connected and i < tryCount:
                    
                    try:
                        self._sk.conn.getSkypeToken()
                    except:     
                        time.sleep(10)
                        pass
                    finally:        
                        i += 1 

        try:
            self._sk.conn
            print("подключено")
        except SkypeAuthException as authEx:
            skype_auth_error = authEx.args[0]
            print(skype_auth_error)

    def checkAuth(self):
        
        return self._sk.conn.connected

    def conversationsList(self):

        groupChats = []

        chats = self.chats.recent()
        
        if len(chats) > 0:
            for item in chats: 
                if isinstance(chats[item], skpy.SkypeGroupChat):
                    groupChats.append((chats[item].topic, chats[item].id))
        return groupChats


    def moveChat(self, admins, chatId, newChatName, moderate=False):

        chat = self._sk.chats[chatId]
        members = chat.userIds
        result = False

        try:
            newChat = self._sk.chats.create(members, admins)

            newChat.setTopic(newChatName)
            newChat.setIsModerateThread(self, moderate)

            result = True
        except:
            pass

        return result

    # Сделать группу модерируемой 
    def setIsModerateThread(self, chatId, moderate=True):

        result = False

        try:
            chat = self._sk.chats[chatId]
            chat.setIsModerateThread(moderate)

            result = True
            # print("id: " + chatId + " name: " + chat.Topic)

        except:
            pass

        return result