# from flask import Flask, render_template, request, redirect, url_for, session
# import db
# import string
# import random
# from datetime import timedelta
# from user import user_bp

# app = Flask(__name__)


# @app.route('/', methods=['POST'])
# def login():
#     user_name = request.form.get('username')
#     password = request.form.get('password')

#     # ログイン判定
#     if db.login(user_name, password):
#         session['user'] = True  # session にキー：'user', バリュー:True を追加
#         session.permanent = True  # session の有効期限を有効化
#         app.permanent_session_lifetime = timedelta(
#             minutes=1)  # session の有効期限を 5 分に設定
#         return redirect(url_for('mypage'))
#     else:
#         error = 'ユーザ名またはパスワードが違います。'

#         # dictで返すことでフォームの入力量が増えても可読性が下がらない。
#         input_data = {'user_name': user_name, 'password': password}
#         return render_template('index.html', error=error, data=input_data)


# @app.route('/mypage', methods=['GET'])
# def mypage():
#     # session があれば mypage.html を表示
#     if 'user' in session:
#         return render_template('layout.html')
#     else:
#         return redirect(url_for('index'))  # session がなければログイン画面にリダイレクト


# @app.route('/register')
# def register_form():
#     return render_template('register.html')


# @app.route('/logout')
# def logout():
#     session.pop('user', None)  # session の破棄
#     return redirect(url_for('index'))  # ログイン画面にリダイレクト


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
