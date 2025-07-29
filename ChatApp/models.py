from flask import abort
import pymysql
from util.DB import DB

#初期起動時にコネクションプールを作成し接続を確立
db_pool=DB.init_db_pool()

#ユーザークラス
class User:
    @classmethod
    def create(cls,uid,name,email,password):
        #データーベース接続プールからコネクションを借りる
        conn=db_pool.get_conn()
        try:
            #コネクションからカーソルを取得する
            with conn.cursor() as cur:
                sql="INSERT INTO user (uid,user_name,email,password) VALUES (%s,%s,%s,%s);"
                #SQLを実行し、パラメータ（uid, name, email, password）を埋め込む
                cur.execute(sql,(uid,name,email,password))
                # データベースに変更を反映（保存）する
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:#使い終わり　コネクションをプールに返す
            db_pool.release(conn)

    @classmethod
    def find_by_email(cls,email):
        conn=db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql="SELECT * FROM users WHERE emails=%s;"
                cur.execute(sql,(email,))
                user=cur.fetchone()
            return user
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)



