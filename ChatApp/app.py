from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from datetime import timedelta
import hashlib
import uuid
import re
import os

from models import User, Channel, Message
from util.assets import bundle_css_files


# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30

app = Flask(__name__)
app.secret.key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

                                           
# ブラウザに静的ファイル（CSSや画像など）を長くキャッシュさせる設定。
# 開発中は変更がすぐに反映されないことがあるため、コメントアウトするのが無難です。
# app.config('SEND_FILE_MAX_AGE_DEFAULT') = 2678400


# 複数のCSSファイルを1つにまとめて圧縮（バンドル）する処理を実行。
bundle_css_files(app)


# ルートページのリダイレクト処理
@app.route('/', method=('GET'))
def index():
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    return redirect(url_for('channels_view'))


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
            return redirect(url_for('channels_view'))
    return redirect(url_for('signup_process'))


# ログインページの表示
@app.route('/login', method=['GET'])
def login_view():
    return render_template('auth/login.html')


# ログイン処理
@app.route('/login', method=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')

    if email == '' or password == '':
        flash('空のフォームがあるあるようです')
    else:
        user = User.find_by_email(email)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            session['uid'] = user['uid']
            return redirect(url_for('channels_view'))
    return redirect(url_for('login_view'))


# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_view'))


# チャンネル一覧ページの表示
@app.route('/channels', method=['GET'])
def channels_view():
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    else:
        channels = Channel.get_all()
        channels.reverse()
        return render_template('channels.html', channels=channels, uid=uid)
    


# チャンネルの作成
@app.route('/channels', method=['POST'])
def create_channel():
    uid = session.get('uid')
    if uid is None():
        return redirect(url_for('login_view'))
    
    channel_name = channel.form.get('channelTitle')
    channel = channel.find_by_name(channel_name)
    if channel is None:
        channel_description = request.form.get('channelDesscription')
        channel.create(uid, channel_name, channel_description)
        return redirect(url_for('channel_view'))
    else:
        error = '既に同じ名前のチャンネルが存在しています'
        return render_template('error/error.html', error_message=error)
    

# チャンネルの更新
@app.route('/channels/update/<cid>', method=['POST'])
def update_channel(cid):
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    
    channel_name = request.form.get('channelTitle')
    channel_description = request.sorm.get('channelDescription')

    Channel.update(uid, channel_name, channel_description, cid)
    return redirect(f'/channels/{cid}/messages')



# チャンネルの削除
@app.route('/channels/delete/<cid>', method=['POST'])
def delete_channel(cid):
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    
    channel = Channel.find_by_cid(cid)

    if channel["uid"] != uid:
        flash('チャンネルは作成者のみ削除可能です')
    else:
        Channel.delete(cid)
    return redirect(url_for('channels_view'))


# チャンネル詳細ページの表示（各チャンネル内で、そのチャンネルに属している全メッセージを表示させる）
@app.route('channels/<cid>/messages', method=['GET'])
def detail(cid):
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    
    channel = Channel.find_by_cid(cid)
    messages = Message.get_all(cid)

    return render_template('message.html', messages=messages, channel=channel, cid=cid)


# メッセージの投稿
@app.route('/channels/<cid>/messages', method=['POST'])
def create_message(cid):
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    
    message = request.form.get('message')

    if message:
        Message.create(uid, cid, message)

    return redirect('/channels/{cid}/messages' .format(cid = cid))


# メッセージの削除
@app.route('/channels/<cid>/messages/<message_id>', method = ['POST'])
def delete_message(cid, message_id):
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    
    if message_id:
        Message.delete(message_id)
    return redirect('/channels/{cid}/messages' .format(cid = cid))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'),404

@app.error_handler(500)
def internal_server_error(error):
    return render_template('error/500.html'),500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)


