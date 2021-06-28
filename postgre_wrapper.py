import psycopg2

def UseDataBase():
    connection = psycopg2.connect(database="parseravito", user="postgres", password="password", host="localhost", port=5432)
    cursor = connection.cursor()
    return cursor
    
#cursor = connection.cursor()

#cursor.execute('SELECT *  FROM public."2021-06-07_iphone";')

# Fetch all rows from database
#record = cursor.fetchall()

#print("Data from Database:- ", record)