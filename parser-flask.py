from flask import Flask, render_template, request, session, redirect, send_from_directory, jsonify, url_for 
from parser_new import fullparse, getpages
from postgre_wrapper import UseDataBase
#from mysql.connector import Error
from functools import wraps
from datetime import datetime
import csv
import os, traceback, sys


app = Flask(__name__)


class AjaxPage():
    default_step = 100
    old_step = 0
    new_step = 0
    step = 50
    def do_refresh(self):
        if self.new_step != 0:
            self.old_step = self.new_step
        else:
            self.old_step = self.default_step
        self.new_step = self.old_step + self.step
    def do_reload(self):
        self.old_step = 0
        self.new_step = 0

page = AjaxPage()
parser_db = UseDataBase()


def exception_handler(err):
    time = 'Time: ' + str(datetime.now())
    ip = 'ip: ' + str(request.remote_addr)
    browser = 'Browser: ' + str(request.user_agent.browser)
    error = 'Error: ' + str(err)

    try:
        with open('errors.log', 'a') as errors:
            print(time, ip, browser, error, sep=' || ', file=errors)
    except:
        print(time, ip, browser, error, sep=' || ')


def check_status(func):
    @wraps(func)
    def wrapper(*args, **kwargs):        
        if 'logged_in' in session:
            return func(*args, **kwargs)
        return redirect('/login')
    return wrapper
app.secret_key = '#$Aqk^&45$$2oPfgHnmKloU5i99fG%$#'


def ask_DB(*args):
    try:
        #cursor = parser_db.create_connection()    
        #parser_db.query_insert(*args)
        #contents = cursor.fetchall()
        #parser_db.close()

        if len(contents) == 0:
            return False
        return contents
    except Error as e:
        exception_handler(e)


@app.route('/signin')
def do_signin():
    return render_template('signin.html')


@app.route('/login')
def do_login():
    return  render_template('login.html')


@app.route('/logout')
def do_logout():
    try:
        session.pop('logged_in')
        session.pop('name')
    except:
        text = 'Вы не в системе'
        return render_template('registration.html', the_text = text)
    text = 'Вы вышли из ситемы'
    return render_template('registration.html', the_text = text)


@app.route('/login_registration', methods = ['GET','POST'])
def check_registration():    
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']

        _SQL = 'SELECT username FROM users WHERE username=%s'
        #dbuser = ask_DB(_SQL, (username,))

        _SQL = 'SELECT password FROM users WHERE username=%s'
        #dbpassword = ask_DB(_SQL, (username,))
        dbuser = "admin"
        if dbuser:
            if 1==1:
                session['logged_in'] = True
                session['name'] = username
                return redirect('/entry')
            else:             
                text = 'Имя или пароль не верны'
                return render_template('registration.html', the_text = text)
        else:
            text = 'Такого пользователя не существует'
            return render_template('registration.html', the_text = text)

    return render_template('registration.html')


@app.route('/signin_registration', methods = ['GET','POST'])
def check_signin():
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']

        if len(password) < 4 or len(username) < 4:
            text = 'Логин и пароль должны содержать не менее 4х символов'
            return render_template('signin.html',the_text=text)

        cursor = parser_db.create_connection()
        _SQL = 'SELECT username FROM users WHERE username=%s'
        parser_db.query_insert(_SQL, (username,))
        dbuser = cursor.fetchall()

        if dbuser:
            text = 'Имя "%s" занято' %username
            cursor.close()
            return render_template('signin.html',the_text=text)
            
        _SQL = 'INSERT INTO users (username, password) VALUES (%s, %s)'
        parser_db.query_insert(_SQL, (username, password))
        parser_db.close()

        session['logged_in'] = True 
        session['name'] = username

    return redirect('/entry')


@app.route('/')
@app.route('/entry')
@check_status
def entry_page():    
    return render_template('entry.html')


@app.route('/results', methods = ['POST','GET']) 
@check_status
def do_search():
    #city = request.form['city']
    search = request.form['search']
    lowprice = request.form['lowprice']
    highprice = request.form['highprice']
    #pagecount = request.form['pagecount']
    
    print(search)
    print(lowprice)
    print(highprice)

    if request.method == 'POST':
        try:
            pages = getpages(search, lowprice, highprice)
            print("pages\n" + str(pages))
            
            return render_template('entry_pages.html', pages=pages, search=search, lowprice=lowprice, highprice=highprice)
            #link = fullparse(search, lowprice, highprice,pagecount)
            
            #titles = ("id", "Запрос")
            #cursor = UseDataBase()
            #_SQL2 = "SELECT row_number() OVER () as rn,tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public' ORDER BY  rn DESC;"
            #cursor.execute(_SQL2)
            #data = cursor.fetchall()
            #return render_template('viewresults.html', the_row_titles = titles, link=link,
            #                                       the_data = data, pages=pages)
        except Exception as e:
            exception_handler(e)
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return exception_handler(e)
            
            
@app.route('/results_pages', methods = ['POST','GET']) 
@check_status
def do_parse():
    #city = request.form['city']
    search = request.form['search']
    lowprice = request.form['lowprice']
    highprice = request.form['highprice']
    pagecount = request.form['pagecount']
    
    print(search)
    print(lowprice)
    print(highprice)

    if request.method == 'POST':
        try:
            
            link = fullparse(search, lowprice, highprice,pagecount)
            
            titles = ("id", "Запрос")
            cursor = UseDataBase()
            _SQL2 = "SELECT row_number() OVER () as rn,tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public' ORDER BY  rn DESC;"
            cursor.execute(_SQL2)
            data = cursor.fetchall()
            return render_template('viewresults.html', the_row_titles = titles, link=link,
                                                   the_data = data)
        except Exception as e:
            exception_handler(e)
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return exception_handler(e)

    	


@app.route('/viewresults')
@check_status
def view_the_parse():
    titles = ("id", "Запрос")
    cursor = UseDataBase()
    _SQL2 = "SELECT row_number() OVER () as rn,tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public' ORDER BY  rn DESC;"
    cursor.execute(_SQL2)
    #data = cursor.fetchall()
    #_SQL_time = 'UPDATE parse SET time="Время размещения неизвестно" WHERE LENGTH(time) > 60'
    #_SQL_phone = 'UPDATE parse SET phone="Неизвестно" WHERE LENGTH(phone) > 60'
    #_SQL = 'SELECT * FROM parseravito WHERE id <= %s' %(page.default_step)
    _SQL = 'SELECT *  FROM public."2021-06-07_iphone"'
    
    #cursor.execute('SELECT *  FROM public."2021-06-07_iphone";')
    #parser_db.query_insert(_SQL_time)
    #parser_db.query_insert(_SQL_phone)
    #parser_db.query_insert(_SQL)

    data = cursor.fetchall()
    print("data:\n"+ str(data))
    parser_db.close()

    page.do_reload()
    try:
        return render_template('viewresults.html', the_row_titles = titles,
                                                   the_data = data)
    except Exception as e:
        exception_handler(e)
        return 'Error'
        
@app.route('/viewresults/<search>')
@check_status
def view_the_parse_search(search):
    titles = ("Город", "Район", "Ссылка", "Цена", "Время", "Наименование")

    cursor = UseDataBase()
    #_SQL_time = 'UPDATE parse SET time="Время размещения неизвестно" WHERE LENGTH(time) > 60'
    #_SQL_phone = 'UPDATE parse SET phone="Неизвестно" WHERE LENGTH(phone) > 60'
    #_SQL = 'SELECT * FROM parseravito WHERE id <= %s' %(page.default_step)
    _SQL = 'SELECT *  FROM public."' + search + '"'
    _SQL2 = "SELECT row_number() OVER (),tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';"
    
    cursor.execute(_SQL)
    #cursor.execute('SELECT *  FROM public."2021-06-07_iphone";')
    #parser_db.query_insert(_SQL_time)
    #parser_db.query_insert(_SQL_phone)
    #parser_db.query_insert(_SQL)
    data = cursor.fetchall()
    print("data:\n"+ str(data))
    parser_db.close()

    #page.do_reload()
    try:
        return render_template('viewresults_big.html', the_row_titles = titles,
                                                   the_data = data, search= search)
    except Exception as e:
        exception_handler(e)
        return 'Error'

@app.route('/downloads/<search>')
@check_status
def download_results(search):
    #_SQL = 'SELECT phone FROM parse WHERE id=1'
    #answer = ask_DB(_SQL)[0][0]

    #if answer:
     #   
    #else:
    #    titles = ('ID', 'Заголовок', 'Цена', 'Время', 'Место', 'URL')
    titles = ("Город", "Район", "Ссылка", "Цена", "Время", "Наименование")
    cursor = UseDataBase()
    _SQL = 'SELECT *  FROM public."' + search + '"'
    cursor.execute(_SQL)
    with open('results.excel', 'w') as results:
        writer = csv.writer(results, dialect='excel')
        writer.writerow(titles)
        writer.writerows(cursor.fetchall())

    return send_from_directory('', 'results.excel')
    
@app.route('/viewresultsajax', methods = ['GET'])
def get_ajax_request():
    page.do_refresh()
    titles = ('ID', 'Заголовок', 'Цена', 'Время', 'Место', 'Номер телефона', 'URL')

    _SQL = 'SELECT * FROM parse WHERE id BETWEEN %s AND %s' %(page.old_step + 1, page.new_step)
    #data = ask_DB(_SQL)

    if data:
        return render_template('new_ajax_results.html', the_row_titles = titles,
                                                        the_data = data,)
    page.do_reload()
    return jsonify(False)





if __name__ == '__main__':
    app.run(debug=True)
