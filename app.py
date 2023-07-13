from flask import Blueprint, Flask, render_template, request, redirect, url_for, session
import db
import string
import random
from datetime import timedelta

app = Flask(__name__)

# レイアウトサンプル


@app.route('/')
def sample_top():
    return render_template('index.html')


@app.route('/book_exe', methods=['POST'])
def book_exe():

    isbn = request.form.get('isbn')
    title = request.form.get('title')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    pages = request.form.get('pages')

    # 必要な項目が入力されているかチェック
    if not (isbn and title and author and publisher and pages):
        return render_template('book_error.html')

    db.insert_book(isbn, title, author, publisher, pages)
    book_list = db.select_all_books()
    return render_template('book_success.html', books=book_list)


@app.route('/list')
def sample_list():
    book_list = db.select_all_books()
    return render_template('list.html', books=book_list)


@app.route('/book')
def sample_register():
    return render_template('book.html')


@app.route('/search')
def sample_search():
    return render_template('search.html')


@app.route('/logout')
def logout():
    session.pop('user', None)  # session の破棄
    return redirect(url_for('index'))  # ログイン画面にリダイレクト


# @app.route('/register_exe', methods=['POST'])
# def register_exe():
#     user_name = request.form.get('username')
#     password = request.form.get('password')

#     if user_name == '':
#         error = 'ユーザ名が未入力です。'
#         return render_template('register.html', error=error, user_name=user_name, password=password)
#     if password == '':
#         error = 'パスワードが未入力です。'
#         return render_template('register.html', error=error)

#     count = db.insert_user(user_name, password)

#     if count == 1:
#         msg = '登録が完了しました。'
#         return redirect(url_for('index', msg=msg))
#     else:
#         error = '登録に失敗しました。'
#         return render_template('register.html', error=error)


if __name__ == "__main__":
    app.run(debug=True)
