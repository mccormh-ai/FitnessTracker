import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import date
from datetime import timedelta


class FirestoreAPI():
    def __init__(self, collection, user):
        self.collection = collection
        self.user = user
        self.db = self.GetDatabaseObj()

    def GetDatabaseObj(self):
        # Use the application default credentials
        cred = credentials.Certificate('firebase_creds.json')
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db

    def writeDataframeToFirestore(self, df):
        df['createdDate'] = str(date.today() - timedelta(days=1))
        for count, record in enumerate(df.to_dict(orient='records')):
            doc_ref = self.db.collection(f'{self.collection}').document(f'{date.today() - timedelta(days=1)}_{count}')
            doc_ref.set(record)
