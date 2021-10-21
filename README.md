# skype_chat_admin
 
![image](https://user-images.githubusercontent.com/1984061/138210075-50d565a9-1daa-4b5b-aa30-d84a0818c64b.png)

 Прототип GUI (PyQt5) приложения для управления чатами в скайпе. Сейчас работает авторизация, даже двухфакторная, загрузка списка последних чатов, и копирование группового чата

для разработки форм использовался Qt Designer 

```sh
pip install pyqt5-tools
```

## Зависимости
```sh
pip install SkPy
```
```sh
pip install PyQt5
```
## Сборка в exe
Для сборки приложения в exe необходимо установить pyinstaller 
```sh
pip install pyinstaller
```
перейти в каталог приложения и запустить сборку скриптом


```sh
pyinstaller --windowed --onefile main.py
```