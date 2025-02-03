import sqlite3 as sq


connection = sq.connect('bd/login.db')
cursor = connection.cursor()

dd = (1, 'ыпып', '1223')
request_to_insert_data = '''INSERT INTO log(id_user, login_user, pass) 
                            VALUES(?, ?, ?)'''            # SQL запрос для добавления информации из базы данных
cursor.execute(request_to_insert_data, dd)

read_data = '''SELECT id_user FROM log
            '''                 # SQL запрос для поиска информации из базы данных
cursor.execute(read_data)
us_id = cursor.fetchall()
connection.commit()
print(us_id)