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
                sql="INSERT INTO users (uid,user_name,email,password) VALUES (%s,%s,%s,%s);"
                #SQLを実行し、パラメータ（uid, name, email, password）を埋め込む
                cur.execute(sql,(uid,name,email,password,))
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
                sql="SELECT * FROM users WHERE email=%s;"
                cur.execute(sql,(email,))
                user=cur.fetchone()
            return user
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)

#チャンネルクラス
class Channel:
    @classmethod
    def create(cls,uid,new_channel_name,new_channel_descreption):
        conn=db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql="INSERT INTO channels (uid,name,abstract) VALUES (%s,%s,%s);"
                cur.execute(sql,(uid,new_channel_name,new_channel_descreption,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_all(cls):
        conn=db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql="SELECT * FROM channels;"
                cur.execute(sql) 
                channels=cur.fetchall()
                return channels
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_cid(cls,cid):
        conn=db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql="SELECT *FROM channels WHERE id=%s;"
                cur.execute(sql,(cid,))
                channnel=cur.fetchone()
                return channnel
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_name(cls,channel_name):
        conn=db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql="SELECT * FROM channels WHERE name=%s;"
                cur.execute(sql,(channel_name,))
                channel=cur.fetchone()
                return channel
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)
 
    @classmethod
    def update(cls,uid,new_channel_name,new_channel_description,cid):
        conn=db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql="UPDATE channels SET uid=%s,name=%s,abstract=%s WHERE id=%s;"
                cur.execute(sql,(uid,new_channel_name,new_channel_description,cid,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)
    
    @classmethod
    def delete(cls,cid):
        conn=db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql="DELETE FROM channels WHERE id=%s;"
                cur.execute(sql,(cid,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)
        

#メッセ―ジクラス
class Message:
    #@classmethod
    def __init__(self, id, uid, user_name, message):
        self.id = id
        self.uid = uid
        self.user_name = user_name
        self.message = message   # デフォルトは0、あとでLikeから埋める
        self.like_count = 0




    @classmethod
    def create(cls,uid,cid,message):
        conn=db_pool.get_conn()
        try:
            with conn.cursor() as cur:
               sql = "INSERT INTO messages(uid, cid, message) VALUES(%s, %s, %s)"
               cur.execute(sql,(uid,cid,message,))
               conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)



    @classmethod
    def get_all(cls,cid):
        conn=db_pool.get_conn()
        try:
            with conn.cursor() as cur:
               sql = """
                   SELECT id, u.uid, user_name, message 
                   FROM messages AS m 
                   INNER JOIN users AS u ON m.uid = u.uid 
                   WHERE cid = %s 
                   ORDER BY id ASC;

                """
               cur.execute(sql,(cid,))
               rows = cur.fetchall()
               for row in rows:
                   print(row["id"])
                   print(row["uid"])
                   print(row["user_name"])
                   print(row["message"])
               return [cls(row["id"], row["uid"], row["user_name"], row["message"]) for row in rows]
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)
    

    @classmethod
    def delete(cls,message_id):
        conn=db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql="DELETE FROM messages WHERE id=%s;"
                cur.execute(sql,(message_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)


#likesテーブルについて
class Like:
    @classmethod
    def like_research(cls,uid,message_id):
        conn=db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                # 既にいいねがあるか確認
                sql_check = "SELECT id FROM likes WHERE uid=%s AND message_id=%s;"
                cur.execute(sql_check, (uid, message_id))
                row = cur.fetchone()
                if row:
                    return True  # 削除された
                else:
                    # なければ追加
                    return False  # 追加された
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def like_insert(cls,uid,message_id):
        conn=db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                    # なければ追加
                    sql_insert = "INSERT INTO likes (uid, message_id) VALUES (%s, %s);"
                    cur.execute(sql_insert, (uid, message_id,))
                    conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn) 
    
    @classmethod
    def like_delete(cls,uid,message_id):
        conn=db_pool.get_conn()
        try:
            with conn.cursor() as cur: 
                    #既にあれば削除
                    sql_delete = "DELETE FROM likes WHERE uid=%s AND message_id=%s;"
                    cur.execute(sql_delete, (uid,message_id,))
                    conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)


    @classmethod
    def count_all_like(cls,message_id):
        conn=db_pool.get_conn()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:#どういうこと？
                sql="SELECT COUNT(*) AS cnt FROM likes WHERE message_id = %s;"
                cur.execute(sql,(message_id,))
                likes_number=cur.fetchone()
                return likes_number['cnt'] if likes_number else 0  # 数字だけ返すなんだこれ？
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)
