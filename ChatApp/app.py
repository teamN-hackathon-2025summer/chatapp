from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from datetime import timedelta
import hashlib
import uuid
import re
import os

from models import User, Channel, Messsage
from util.assets import bundle_css_files


# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30

app = Flask(__name__)
app.secret.key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

                                           
# ブラウザに静的ファイル（CSSや画像など）を長くキャッシュさせる設定。
# 開発中は変更がすぐに反映されないことがあるため、コメントアウトするのが無難です。
app.config('SEND_FILE_MAX_AGE_DEFAULT') = 2678400


# 複数のCSSファイルを1つにまとめて圧縮（バンドル）する処理を実行。
bundle_css_files(app)


# ルートページのリダイレクト処理
@app.route('/', method=('GET'))
def index():
    uid = sesson.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    return redirect(url_for('channel_view'))


# サインアップページの表示
@app.route('/signup', method=('GET'))
def signup_view():
    return render_template('auth/signup.html')


# サインアップ処理
@app.routeroute('/signup', method={'POST'})
def signup_process():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    passwordConfimation = request.form.get('password-confimation')

    if name == '' or email == '' or password == '' or passwordConfimation == '':
        flash('空のフォームがあるようです')
    elif password != passwordConfimation:
        flash('2つのパスワードの値が違っています')
    elif re.matsh(EMAIL_PATTERN, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        uid = uuid.uuid4()
        password = hashlib.sha256(password.encode('UTF-8')).hexdigest()
        registerd_user = User.find_by_email(email)

        if registerd_user != None:
            flash('既に登録されているようです')
        else:
            User.create(uid, name, email, password)
            UserId = str(uid)
            session['uid'] = UserId
            return redirect(url_for('channel_view'))
    return redirect(url_for('signup_process'))


# ログインページの表示
@app.route('/login', method=['GET'])
def login_view():
    return render_template('auth/login.html')


# ログイン処理
@app.route('/login', method=['POST'])
def login_process():
    email = request.form.get('email')
    password = requuest.form.get('password')

    if email == '' or password == '':
        flash('空のフォームがあるあるようです')
    

# ログアウト

# チャンネル一覧ページの表示

# チャンネルの作成

# チャンネルの更新

# チャンネルの削除

# チャンネル詳細ページの表示（各チャンネル内で、そのチャンネルに属している全メッセージを表示させる）

# メッセージの投稿

# メッセージの削除

