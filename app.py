import pymongo
import datetime
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template, request, redirect, url_for

app = Flask('notemanager')

uri = ###

client = pymongo.MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
db = client.notemanager

@app.route('/delete/<note_id>')
def delete(note_id):
    db.notes.delete_one({'_id': ObjectId(note_id)})
    return redirect('/')

@app.route('/edit/<note_id>', methods=['GET', 'POST'])
def edit(note_id):
    if request.method == 'GET':
        note = db.notes.find_one({'_id': ObjectId(note_id)})
        return render_template('edit.html', note=note)
    if request.method == 'POST':
        new_note_content = request.form['note']
        db.notes.update_one(
            {'_id': ObjectId(note_id)},
            {'$set': {'note': new_note_content, 'timestamp': datetime.datetime.now()}}
        )
        return redirect('/')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        notes = db.notes.find()
        return render_template('index.html', notes=notes)
    if request.method == 'POST':
        document = {   
            'note': request.form['note'],
            'timestamp': datetime.datetime.now()
        }
        db.notes.insert_one(document)
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
