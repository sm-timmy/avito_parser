# Web parser для Avito

## Установка:
- Скачать ZIP проекта
- Распаковать
```
cd /путь до распакованной папки
```

### Если на локальной машине установлен mysql:
#### В консоли:
```
pip install virtualenv (Если не получилось: sudo pip install virtualenv)
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python database_creator.py
```
#### Для запуска веб приложения:
```
python parser-flask.py
```
##### Готово, переходим по ссылке http://127.0.0.1:5000/
#### Для авторизации внутри приложения использовать логин "admin" пароль "root"


### Если на локальной машине НЕ установлен mysql:
- Заменить файл 'mysql_wrapper.py' в папке 'avito-parser-master' файлом 'mysql_wrapper.py' из папки 'mysql_wrapper_for_remote_acsess'
- Перейти по ссылке https://cp-hosting.jino.ru/management/mysql/ipaccess/
- Login: 92oopss
- Password: 4Jg2xFmu
- Добавить разрешенный IP
- В диапазон IP добавить ваш текущий IP адрес
#### В консоли:
```
pip install virtualenv (Если не получилось: sudo pip install virtualenv)
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
#### Для запуска веб приложения:
```
python parser-flask.py
```
##### Готово, переходим по ссылке http://127.0.0.1:5000/
#### Для авторизации внутри приложения использовать логин "admin" пароль "root"
# avito_parser
