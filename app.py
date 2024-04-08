from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient, ReturnDocument
from bson import ObjectId

uri = "mongodb+srv://shivmodi21:shivmodi@cluster0.p8k9ttj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client.sparta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('note.html')

@app.route('/notes', methods=['GET', 'POST', 'PUT', 'DELETE'])
def notes():
    if request.method == 'GET':
        notes = list(db.notes.find({}, {'_id': 1, 'title': 1, 'text': 1}))
        for note in notes:
            note['_id'] = str(note['_id'])  # Convert ObjectId to string
        return jsonify(notes)
    elif request.method == 'POST':
        note = request.get_json()
        db.notes.insert_one(note)
        return '', 201
    elif request.method == 'PUT':
        note_id = request.args.get('id')
        note = request.get_json()
        db.notes.find_one_and_update({'_id': ObjectId(note_id)}, {'$set': note}, return_document=ReturnDocument.AFTER)
        return '', 200
    elif request.method == 'DELETE':
        note_id = request.args.get('id')
        db.notes.delete_one({'_id': ObjectId(note_id)})
        return '', 200

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)