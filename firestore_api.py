import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import date
from datetime import timedelta


class FirestoreAPI():
    def __init__(self, projectId, collection, user):
        self.projectId = projectId
        self.collection = collection
        self.user = user
        self.db = self.GetDatabaseObj()

    def GetDatabaseObj(self):
        # Use the application default credentials
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
        'projectId': self.projectId,
        })
        db = firestore.client()
        return db

    def writeDataframeToFirestore(self, df):
        doc_ref = db.collection(f'{self.collection}').document(f'{date.today() - timedelta(days=1)}_test')
        doc_ref.set(df.to_json())
