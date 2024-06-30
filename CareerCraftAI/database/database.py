from firebase_admin import firestore
from schemas import item 

# Get a reference to the Firestore database
db = firestore.client()

def create_user(user_id, data):
    doc_ref = db.collection('users').document(user_id)
    doc_ref.set(data)
    print(f"User {user_id} created successfully")


def read_user(user_id):
    doc_ref = db.collection('users').document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        print(f"User data: {doc.to_dict()}")
        return doc.to_dict()
    else:
        print("No such user!")
        return None

# UPDATE operation
def update_user(user_id, data):
    doc_ref = db.collection('users').document(user_id)
    doc_ref.update(data)
    print(f"User {user_id} updated successfully")

# DELETE operation
def delete_user(user_id):
    db.collection('users').document(user_id).delete()
    print(f"User {user_id} deleted successfully")


def create_doc(data: item.Item, job_id):
    doc_ref = db.collection('documents').document(job_id)
    doc_ref.set({
        'email': data.email,
        'username': data.username,
        'timestamp': firestore.SERVER_TIMESTAMP,
        'description': data.description,
        'questions': data.questions,
        'script': data.script
    })

    print(f"Document {job_id} created successfully")

def read_doc(job_id):
    doc_ref = db.collection('documents').document(job_id)
    doc = doc_ref.get()
    if doc.exists:
        print(f"Document data: {doc.to_dict()}")
        return doc.to_dict()
    else:
        print("No such document!")
        return None
    
def update_job(job_id, data):
    doc_ref = db.collection('jobs').document(job_id)
    doc_ref.update(data)
    print(f"Job {job_id} updated successfully")

# DELETE operation
def delete_job(job_id):
    db.collection('jobs').document(job_id).delete()
    print(f"Job {job_id} deleted successfully")

