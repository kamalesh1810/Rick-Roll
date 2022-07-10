import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# set up firebase db credentials
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# check if a document exists in a collection
def doc_exists(email):
    doc_ref = db.collection('users').document(email)
    doc = doc_ref.get()
    if doc.exists:
        return True
    else:
        return False
 
# function which returns a user document
def get_data(email):
    doc_ref = db.collection('users').document(email)
    doc = doc_ref.get()
    if doc.exists:
        y = doc.to_dict()
        return y
    else:
        return None

# function to return the value of a particular document field
def get_field(field_name,email):
    data = get_data(email)
    try:
        return data[field_name]
    except:
        return None
    
# function to set a particular document field
def set_field(field_name,value,email):
    doc_ref = db.collection('users').document(email)
    doc = doc_ref.get()
    if doc.exists:
        db.collection('users').document(email).update(
            {
                field_name:value
            }
        )
    else:
        data = {
            field_name:value
        }
        db.collection('users').document(email).set(data)

# add a user name to the rick rolled list
def add_to_rolled_list(name):
    doc_ref = db.collection('troll').document('names')
    doc_ref.update({u'troll_list': firestore.ArrayUnion([f'{name}'])})

# get the list of users who got rick rolled
def get_rolled_list():
    doc_ref = db.collection('troll').document('names')
    doc = doc_ref.get()
    y = doc.to_dict()
    return y['troll_list']