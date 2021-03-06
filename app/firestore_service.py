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


def create_user(username, password):
    result = db.collection('user').add({'username': username, 'password': password})
    return result[1]


def get_todos(user_id):
    return db.collection('user').document(user_id).collection('todo').get()


def create_todo(user_id, description):
    result = db.collection('user').document(user_id).collection(
        'todo').add({'description': description, 'done': False})
    return result[1]


def delete_todo(user_id, todo_id):
    todo_ref = db.document(f'user/{user_id}/todo/{todo_id}')
    todo_ref.delete()


def update_todo(user_id, todo_id, done):
    todo_ref = db.document(f'user/{user_id}/todo/{todo_id}')
    todo_ref.update({'done': not bool(done)})
