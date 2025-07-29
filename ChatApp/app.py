from flask import Flask,request,redirect,render_template,session,flash,url_for
from datetime import timedelta
import hashlib
import uuid
import re
import os

from models import User,channnel,Message
from util.assets import bundle_css_files


#定数定義
EMAIL_PATTERN=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS=30

app=Flask(__name__)
#秘密鍵の生成
app.secret_key=os.getenv('SECRET_KEY',uuid.uuid4().hex)
app.permanent_session_lifetime=timedelta(days=SESSION_DAYS)

# ブラウザに静的ファイル（CSSや画像など）を長くキャッシュさせる設定。
# 開発中は変更がすぐ反映されないことがあるため、コメントアウトするのが無難です。
app.config['SEND_FILE_MAX_AGE_DEAULT']=2678400

# 複数のCSSファイルを1つにまとめて圧縮（バンドル）する処理を実行。
bundle_css_files(app)

#ルートページのリダイレクト処理
@app.route('/',methods=['GET'])
def index():
    uid=session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    return redirect(url_for('channel_view'))

#サインアップページの表示
@app.route('/signup',methods=['GET'])
def signup_view():
    return render_template('auth/signup.html')

#サインアップ処理
@app.route('/signup',methods=['POST'])
def signup_process():
    name=request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('password')
    passwordConfirmation=request.form.get('password-confirmation')

    if name=='' or email=='' or password=='' or passwordConfirmation=='' :
        flash('空のフォームがあるようです')
    elif password!=passwordConfirmation:
        flash('二つのパスワードの値が違っています')
    elif re.match(EMAIL_PATTERN,email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        uid=uuid.uuid4()
        password=hashlib.sha256(password.encode('utf-8')).hexdigest()
        registered_user=User.find_by_email(email)

        if registered_user !=None:
            flash('既に登録されているようです')
        else:
            User.create(uid,name,email,password)
            UserId=str(uid)
            session['uid']=UserId
            return redirect(url_for('channels_view'))
        return redirect(url_for('signup_process'))
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_view'))

#チャンネル一覧ページの表示



