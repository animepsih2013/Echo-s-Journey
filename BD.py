import sqlite3 as sq


connection = sq.connect('bd/login.db')
cursor = connection.cursor()

dd = (2, 'dasgf')
request_to_insert_data = '''INSERT or IGNORE INTO log(id_user, login_user) 
                            VALUES(?, ?)'''            # SQL запрос для добавления информации из базы данных
cursor.execute(request_to_insert_data, dd)

read_data = '''SELECT id_user FROM log
            '''                 # SQL запрос для поиска информации из базы данных
cursor.execute(read_data)
us_id = cursor.fetchall()
connection.commit()
print(us_id)