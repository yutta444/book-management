import os
import psycopg2
import string
import random
import hashlib


def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection


def select_all_books():
    connection = get_connection()
    cursor = connection.cursor()
    SQL = "SELECT isbn, title, author, publisher, pages FROM book_management"

    cursor.execute(SQL)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows


def insert_book(isbn, title, author, publisher, pages):

    connection = get_connection()
    cursor = connection.cursor()
    sql = 'INSERT INTO book_management VALUES (default, %s, %s, %s, %s, %s)'
    cursor.execute(sql, (isbn, title, author, publisher, pages))
    connection.commit()
    cursor.close()
    connection.close()


def select_book_detail(isbn):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM book_management WHERE isbn = %s'

    cursor.execute(sql, (isbn,))
    rows = cursor.fetchall()
    connection.close()
    cursor.close()
    if rows:
        book = {
            'id': rows[0][0],
            'isbn': rows[0][1],
            'title': rows[0][2],
            'author': rows[0][3],
            'publisher': rows[0][4],
            'pages': rows[0][5]
        }
        return book
    else:
        return None


def delete_book(id):

    connection = get_connection()
    cursor = connection.cursor()
    sql = 'DELETE FROM book_management WHERE id =%s'
    cursor.execute(sql, (id,))
    connection.commit()
    cursor.close()
    connection.close()


def get_salt():
    charset = string.ascii_letters + string.digits

    salt = ''.join(random.choices(charset, k=30))
    return salt


def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1246).hex()
    return hashed_password


def insert_user(user_name, password):
    sql = 'INSERT INTO book_user VALUES(default, %s, %s, %s)'

    salt = get_salt()
    hashed_password = get_hash(password, salt)

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (user_name, hashed_password, salt))
        count = cursor.rowcount  # 更新件数を取得
        connection.commit()

    except psycopg2.DatabaseError:
        count = 0

    finally:
        cursor.close()
        connection.close()

    return count


def login(user_name, password):
    sql = 'SELECT hashed_password, salt FROM book_user WHERE name = %s'
    flg = False

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (user_name,))
        user = cursor.fetchone()

        if user != None:
            # SQLの結果からソルトを取得
            salt = user[1]

            # DBから取得したソルト + 入力したパスワード からハッシュ値を取得
            hashed_password = get_hash(password, salt)

            # 生成したハッシュ値とDBから取得したハッシュ値を比較する
            if hashed_password == user[0]:
                flg = True

    except psycopg2.DatabaseError:
        flg = False

    finally:
        cursor.close()
        connection.close()

    return flg
