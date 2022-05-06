# Установка

## Скачивание Python 
Скачайте python 3.9.10 или более поздюю версию с оффициального сайта.
[Python 3.9.12](https://www.python.org/ftp/python/3.9.12/python-3.9.12-amd64.exe)

## Создание виртуальной среды
* Чтобы продолжить таботу откройте командную строку (cmd).

* Перейдите папку в которой бы хотите разместить сайт:
```
cd "Путь к папке"
```
* Скачайте проект из github.
* Далее необходимо распоковать архим с сайтом в вашу папку.
* Перейдите в папку Web-Project-Yandex-Lyceum
```
cd Web-Project-Yandex-Lyceum
``` 
* Установите и создайте виртуальную среду.
```
pip install virtualenv
python -m venv venv
```
* Активируйте виртуальную среду.
```
venv\Scripts\activate.bat
```
* Скачайте все необходимые библиотеки
```
pip install -r requirements.txt
python -m nltk.downloader omw-1.4
```
* Установите переменные виртуальной среды.
## Запуск
```
set FLASK_APP=Project/main.py
set FLASK_DEBUG=1
```
* Запуск.
```
cls & python -m flask run --host localhost --port 8080 --reload --debugger
```

## Запуск через PyCharm
* Для того чтобы запустить прокт через pycharm необходимо в setting.py установить:
```
is_pycharm = True
```
И запустить как обычный проект выбрав точку входа Project/main.py