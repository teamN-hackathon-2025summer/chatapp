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

# サインアップページの表示

# サインアップ処理

# ログインページの表示

# ログイン処理

# ログアウト

# チャンネル一覧ページの表示

# チャンネルの作成

# チャンネルの更新

# チャンネルの削除

# チャンネル詳細ページの表示（各チャンネル内で、そのチャンネルに属している全メッセージを表示させる）

# メッセージの投稿

# メッセージの削除

