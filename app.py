from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
app = Flask(__name__)

uri = "mongodb+srv://root:aldy0921@cluster0.mon5i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri);

db = client['LX']
collection = db['semester_3']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    all_docs = collection.find()
    result_array = []
    
    for document in all_docs:
        result_array.append({
            "id": str(document.get('_id', '')),
            "title": document.get('title', ''),
            "description": document.get('description', ''),
            "bg_image": document.get('bg_image', ''),
            "icon_image": document.get('icon_image', ''),
            "created_at": document.get('created_at', ''),
            "updated_at": document.get('updated_at', ''),
        })        
        
    return jsonify({
        'status': 'success',
        'data' : result_array
    })

@app.route('/diary', methods=['POST'])
def save_diary():
    titleReceive = request.form['title']
    contentReceive = request.form["description"]

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if not titleReceive or not contentReceive:
        return jsonify({'msg': 'Title and description are required!'}), 400
    result = collection.insert_one({
        "title" : titleReceive,
        "description" : contentReceive,
        "bg_image": "",
        "icon_image": "",
        "created_at": current_time,
        "updated_at": ""
        })
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)
