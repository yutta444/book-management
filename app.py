from flask import Blueprint, Flask, render_template, request, redirect, url_for, session
import db
import string
import random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

# レイアウトサンプル


@app.route('/')
def sample_top():
    return render_template('index.html')

# 図書登録遷移


@app.route('/book')
def book_register():
    return render_template('book.html')

# 図書登録


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
def list_exe():
    book_list = db.select_all_books()
    return render_template('list.html', books=book_list)

# 図書削除


@app.route('/book_delete', methods=['GET'])
def book_delete():
    book_id = request.args.get('id')
    return render_template('book_delete.html', id=book_id)

# 図書削除


@app.route('/book_delete', methods=['post'])
def book_delete_exe():
    id = request.form.get('id')
    db.delete_book(id)
    book_list = db.select_all_books()
    return render_template('mypage.html', books=book_list)


@app.route('/book')
def delete_exe():
    return render_template('book_delete.html')


# 他の関数定義の後にsearch_books関数を追加

@app.route('/search_books', methods=['POST'])
def search_books():
    search_query = request.form.get('search_query')

    # 検索クエリが入力されている場合にのみ検索を実行
    if search_query:
        connection = db.get_connection()
        cursor = connection.cursor()

        # 部分一致で書籍を検索
        sql = "SELECT isbn, title, author, publisher, pages FROM book_management WHERE title LIKE %s"
        cursor.execute(sql, ('%' + search_query + '%',))
        search_results = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('search.html', books=search_results)
    else:
        # 検索クエリが入力されていない場合は、書籍リストを表示
        book_list = db.select_all_books()
        return render_template('search.html', books=book_list)


@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')

    if msg == None:
        return render_template('index.html')
    else:
        return render_template('index.html', msg=msg)


@app.route('/', methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')

    # ログイン判定
    if db.login(user_name, password):
        session['user'] = True  # session にキー：'user', バリュー:True を追加
        session['username'] = user_name
        session.permanent = True  # session の有効期限を有効化
        app.permanent_session_lifetime = timedelta(
            minutes=1)  # session の有効期限を 5 分に設定
        return redirect(url_for('mypage'))
    else:
        error = 'ユーザ名またはパスワードが違います。'

        # dictで返すことでフォームの入力量が増えても可読性が下がらない。
        input_data = {'user_name': user_name, 'password': password}
        return render_template('index.html', error=error, data=input_data)


@app.route('/mypage', methods=['GET'])
def mypage():
    # session があれば mypage.html を表示
    if 'user' in session:
        book_list = db.select_all_books()
        return render_template('mypage.html', books=book_list)
    else:
        return redirect(url_for('index'))  # session がなければログイン画面にリダイレクト

# 図書の詳細表示


@app.route('/detail', methods=['GET'])
def book_detail():
    id = request.args.get('id')
    isbn = request.args.get('isbn')
    title = request.args.get('title')
    author = request.args.get('author')
    publisher = request.args.get('publisher')
    pages = request.args.get('pages')

    book = db.select_book_detail(isbn)

    session['id'] = id
    session['title'] = title

    return render_template('book_detail.html', book=book)


@app.route('/edit', methods=['GET'])
def book_edit():
    book_id = request.args.get('id')
    title = request.args.get('title')
    return render_template('book_edit.html', id=book_id, title=title)


@app.route('/register')
def register_form():
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user', None)  # session の破棄
    return redirect(url_for('index'))  # ログイン画面にリダイレクト


@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    password = request.form.get('password')

    if user_name == '':
        error = 'ユーザ名が未入力です。'
        return render_template('register.html', error=error, user_name=user_name, password=password)
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('register.html', error=error)

    count = db.insert_user(user_name, password)

    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)


if __name__ == "__main__":
    app.run(debug=True)
