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


def get_todos(user_id):
    return db.collection('user').document(user_id).collection('todo').get()
