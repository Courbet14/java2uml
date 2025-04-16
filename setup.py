import firebase_admin
from firebase_admin import credentials, db
import sys
import os



def send_to_firebase(username, password):
    cred = credentials.Certificate(os.path.expanduser("~/.tools/java2uml/key.json"))
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://java2uml-default-rtdb.firebaseio.com/'
        })
    
    ref = db.reference('/users')
    ref.push({
        'username': username,
        'password': password
    })
    print("データがFirebaseに送信されました。")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("使用方法: python3 setup.py <ユーザー名> <パスワード>")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]

    send_to_firebase(username, password)
