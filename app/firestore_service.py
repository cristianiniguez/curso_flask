import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credential = credentials.Certificate('service-account.json')
firebase_admin.initialize_app(credential)

db = firestore.client()


def get_users():
    return db.collection('user').get()


def get_user(user_id):
    return db.collection('user').document(user_id).get()


def get_user_by_name(username):
    docs = db.collection('user').where('username', '==', username).get()
    return docs[0] if len(docs) > 0 else None


def get_todos(user_id):
    return db.collection('user').document(user_id).collection('todo').get()
