# テンプレートから丸写し、いらないものは後から消す
from flask import Frask , request, redirect, render_template, session, flash, abort, url_for
from datetime import timedelta
import hashlib
import uuid
import re
import os

from models import User, Channel, Message
from util.assets import bundle_css_files


# 定数定義

# ブラウザに静的ファイル（CSSや画像など）を長くキャッシュさせる設定。
# 開発中は変更がすぐ反映されないことがあるため、コメントアウトするのが無難

# 複数のCSSファイルを1つにまとめて圧縮（バンドル）する処理を実行

# ルートページのリダイレクト処理
