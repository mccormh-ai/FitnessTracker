from gmail_api import GetService, GetMessages, GetAttachement
from firestore_api import FirestoreAPI
import pandas as pd
import os


class GmailParse():
    def __init__(self):
        self.userId = 'me'
        self.labelName = 'API_BOX'
        self.parsedDF = self.runMsgs()

    def RequestConcat(self, service, msgs):
        concatList = []
        for msg in msgs:
            print(msg['id'])
            returnDf = GetAttachement(service=service, msg_id=msg['id'])
            try:
                returnDf['msgId'] = msg['id']
            except:
                print("No attachment")
            concatList.append(returnDf)
        return pd.concat(concatList, axis=0)
        
    def runMsgs(self):
        _service = GetService()
        _msgs = GetMessages(service=_service, labelName=self.labelName)
        return self.RequestConcat(service=_service, msgs=_msgs)
        
   


def main():
    _df = GmailParse().parsedDF
    FirestoreAPI(collection='nutritionLog', user='hmccormick').writeDataframeToFirestore(df=_df)

if __name__ == '__main__':
    main()