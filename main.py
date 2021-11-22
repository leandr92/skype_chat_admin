from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItems
import Skype.skype_manager as SkypeManager

# Импортируем нашу форму.
from UI.Ui_untitled import Ui_MainWindow
import sys
 
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.chats.setColumnCount(2)
        self.ui.chats.setHorizontalHeaderLabels(
            ('Имя', 'UID')
        )
        self.skype = SkypeManager.SkypeManager()

        self.ui.label_7.setText("Не подключено")
        
        # подключение клик-сигнал к слоту btnClicked
        self.ui.auth.clicked.connect(self.auth)
        self.ui.createChat.clicked.connect(self.createChat)
        self.ui.loadMore.clicked.connect(self.loadMore)
        self.ui.setChatModerate.clicked.connect(self.setChatModerate)

        # подключение потока для аутентификации
        self.authThread = AuthThread()
        self.authThread.skype = self.skype
        self.authThread.endSignal.connect(self.set_auth_label)

        # подключение потока для создания чата
        self.createChatThread = CreateChatThread()
        self.createChatThread.skype = self.skype
        self.createChatThread.endSignal.connect(self.set_create_label)

        # подключение потока для создания чата
        self.createChatChangeThread = CreateChatChangeThread()
        self.createChatChangeThread.skype = self.skype
        self.createChatChangeThread.endSignal.connect(self.set_change_label)
        
        # подключение потока для загрузки списка чатов
        self.loadConversitonsThread = LoadConversitonsThread()
        self.loadConversitonsThread.skype = self.skype
        self.loadConversitonsThread.endSignal.connect(self.btnClicked)
   
    def set_change_label(self, changed):
        if changed:
            self.ui.label_7.setText("Модерирование включено")
            self.loadConversitonsThread.start()
        else:
            self.ui.label_7.setText("Ошибка подключения") 

    def set_auth_label(self, connected):
        if connected:
            self.ui.label_7.setText("Подключено")
            self.loadConversitonsThread.start()
        else:
            self.ui.label_7.setText("Ошибка подключения")

    def set_create_label(self, created):
        if created:
            self.ui.label_7.setText("Чат создан")
        else:
            self.ui.label_7.setText("Ошибка создания чата")


    # Авторизация
    def auth(self):
        
        self.ui.label_7.setText("Если используется двухфакторная аутентификация то посмотрите в приложение Аутентификатор")
        self.authThread.user = self.ui.login.text()
        self.authThread.password = self.ui.password.text()
        self.authThread.start()


    # Получаем текущее значение строки
    def createChat(self):

        adminsText = self.ui.moderatorName.toPlainText()
        adminsText = adminsText.replace(" ", "")
        self.createChatThread.admins = adminsText.split(",")

        if self.ui.chats.currentRow() >= 0:

            self.createChatThread.chatId = self.ui.chats.item(self.ui.chats.currentRow(), 1).text()
            self.createChatThread.newChatName = self.ui.newChatName.text()

        self.createChatThread.start()

    def loadMore(self):
        self.loadConversitonsThread.start()

    def setChatModerate(self):
        
        if self.ui.chats.currentRow() >= 0:

            self.createChatChangeThread.chatId = self.ui.chats.item(self.ui.chats.currentRow(), 1).text()

        self.createChatChangeThread.start()

    def btnClicked(self, data):

        row = self.ui.chats.rowCount()

        # if row > 0:
        #     row -= 1

        for tup in data:
            
            col = 0

            self.ui.chats.insertRow(row)
            for item in tup:
                cellinfo = QTableWidgetItem(item)
 
                # Только для чтения
                cellinfo.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
                )
 
                self.ui.chats.setItem(row, col, cellinfo)
                col += 1
 
            row += 1


# отдельный поток для работы со скайпом
class AuthThread(QThread):
       
    endSignal = pyqtSignal(bool)
    skype = SkypeManager.Skype
    user = ""
    password = ""

    def __init__(self):
        super().__init__()
 
    def run(self):

        self.skype.connect(self.user, self.password)

        result = self.skype.checkAuth()

        self.endSignal.emit(result) 

# отдельный поток для работы с чатом
class CreateChatThread(QThread):
    
    endSignal = pyqtSignal(bool)
    skype = SkypeManager.Skype
    admins = ""
    chatId = ""
    newChatName = ""

    def __init__(self):
        super().__init__()
 
    def run(self):

        result = self.skype.moveChat(self.admins, self.chatId, self.newChatName)

        self.endSignal.emit(result)   

# отдельный поток для работы с изменением чата
class CreateChatChangeThread(QThread):
    
    endSignal = pyqtSignal(bool)
    skype = SkypeManager.Skype
    chatId = ""

    def __init__(self):
        super().__init__()
 
    def run(self):

        result = self.skype.setIsModerateThread(self.chatId)

        self.endSignal.emit(result)   

# отдельный поток для работы с чатами
class LoadConversitonsThread(QThread):
    
    endSignal = pyqtSignal(list)
    skype = SkypeManager.Skype

    def __init__(self):
        super().__init__()
 
    def run(self):

        result = self.skype.conversationsList()
        self.endSignal.emit(result)     

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())