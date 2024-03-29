import sqlite3
import config
from datetime import date


db = sqlite3.connect("DataBase.db")
cursor = db.cursor()

def create_names_db():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (tg_id INT NOT NULL, name STRING NOT NULL, nickname STRING NOT NULL, is_here INTEGER);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS day_info (date DATE NOT NULL, stud_attend INTEGER,day_code TEXT);""")
    db.commit()

def get_student(user_id):
    info = cursor.execute("SELECT * FROM users WHERE tg_id = ?;" ,(user_id,)).fetchone()
    return info

def get_all_group():
    info = cursor.execute("SELECT * FROM users;").fetchall()
    return info

def insert_in_group(tg_id, name, nickname):
    if get_student(tg_id) is None:
        cursor.execute("INSERT INTO users VALUES(?,?,?,?)",(tg_id,name,nickname,0))
        db.commit()

def add_attendance(tg_id):
    info = cursor.execute("SELECT * FROM day_info WHERE date = ?;",(date.today(),))
    if info.fetchone() is None:
        cursor.execute("UPDATE users SET is_here = ?;",[0])
        cursor.execute("INSERT INTO day_info VALUES (?,?,?);",(date.today(),0,''))
        db.commit()
    if get_student(tg_id)[3] == 0:
        cursor.execute("UPDATE users SET is_here = ? WHERE tg_id = ?;",(1,tg_id))
        cursor.execute("UPDATE day_info SET stud_attend = stud_attend + 1 WHERE date = ?;",(date.today(),))
        db.commit()
    
def is_attendance_fin():
    info = cursor.execute("SELECT day_code FROM day_info WHERE date = ?;",(date.today(),)).fetchone()
    if info is None:
        return True
    return info[0] == ''
    
def is_name_available(name):
    info = cursor.execute("SELECT * FROM users WHERE name = ?;",(name,)).fetchone()
    return info    


def get_quantity():
    info = cursor.execute("SELECT stud_attend FROM day_info WHERE date = ?;",(date.today(),)).fetchone()[0]
    return info


def drop_day_code():
    cursor.execute("UPDATE day_info SET day_code = ? WHERE date = ?;",('',date.today()))
    db.commit()
    
def delete_student(user_id):
    cursor.execute("DELETE FROM users WHERE tg_id = ?;", (user_id,))
    db.commit()


def create_tab1_image():
    info = cursor.execute("SELECT * FROM users").fetchall()
    with open(config.tab_names[0],'w+') as f:
        for line in info:
            for el in line:
                f.write(f'{el} ')
            f.write('\n')
            
    
def create_dict():
    info = cursor.execute("SELECT name,is_here FROM users;").fetchall()
    sl = dict()
    for el in info:
        if el[1] == 0:
            sl[el[0]] = 2
        else:
            sl[el[0]] = 1
    return sl
    

def new_day():
    info = cursor.execute("SELECT is_here FROM users;").fetchall()
    day_code = ""
    for el in info:
        day_code += str(el[0])
    cursor.execute("UPDATE day_info SET day_code = ? WHERE date = ?;",(day_code,date.today()))
    db.commit()

create_names_db()
