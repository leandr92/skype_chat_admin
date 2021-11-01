# Skype chat admin
 
![image](https://user-images.githubusercontent.com/1984061/139675661-d880a635-078c-44cc-b0c7-380a2d6a66c2.png)

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
