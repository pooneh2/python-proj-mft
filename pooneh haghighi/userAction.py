import sqlite3

cnt=sqlite3.connect("shop.db")


def user_login(user,pas):
    sql=''' SELECT * FROM users WHERE user=? and pass=? '''
    result=cnt.execute(sql,(user,pas))
    rows=result.fetchall()
    if len(rows)<1:
        return False
    else:
        return rows[0][0]

def user_submit(user,pas):
    if len(pas)<8:
        return False,"password length error!"
    elif pas.isalpha() or pas.isdigit():
        return False,"password combination error!"
    
    sql='''SELECT * FROM users WHERE user=?'''
    result=cnt.execute(sql,(user,))
    rows=result.fetchall()
    if len(rows)>0:
        return False,"username already exist!"
    sql='''INSERT INTO users (user,pass,score) VALUES (?,?,?)'''
    cnt.execute(sql,(user,pas,5))
    cnt.commit()
    return True,""

def get_user():
    sql=''' SELECT * FROM users '''
    result=cnt.execute(sql)
    rows=result.fetchall()
    return rows

def get_single_user(uid):
    sql=''' SELECT * FROM users WHERE id=? '''
    result=cnt.execute(sql,(uid,))
    row=result.fetchone()
    return row
    
def get_score(user):
    sql='''SELECT score FROM users WHERE user=?'''
    result=cnt.execute(sql,(user,))
    rows=result.fetchone()
    if int(rows[0])>=30:
        return True
    else:
        return False
