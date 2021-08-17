# app.py

# Required imports
import os
from flask import Flask, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app

# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('firebase_creds.json')
default_app = initialize_app(cred)
db = firestore.client()
log_ref = db.collection('workoutLog')

@app.route('/', methods=['POST', 'GET'])
def index():
    all_log = [doc.to_dict() for doc in log_ref.stream()]
    return render_template('index.html', all_log=all_log)

@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        print('start here')
        id = request.json['id']
        print(id)
        log_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON.
        log : Return document that matches query ID.
        all_log : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        log_id = request.args.get('id')
        if log_id:
            log = log_ref.document(log_id).get()
            return jsonify(log.to_dict()), 200
        else:
            all_log = [doc.to_dict() for doc in log_ref.stream()]
            return jsonify(all_log), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        log_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        log_id = request.args.get('id')
        log_ref.document(log_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

#port = int(os.environ.get('PORT', 8080))

if __name__ == '__main__':
    #app.run(threaded=True, host='0.0.0.0', port=port)
    app.run(debug=True)
