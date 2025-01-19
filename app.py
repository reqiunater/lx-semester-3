from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import random
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
            "profile_image": document.get('profile_image', ''),
            "created_at": document.get('created_at', ''),
            "updated_at": document.get('updated_at', ''),
        })        
        
    return jsonify({
        'status': 'success',
        'data' : result_array
    })
    
@app.route('/diary_data', methods=['POST'])
def get_diary():
    result_array = []

    # Mendapatkan id dari request
    update_id = request.form.get('id')
    try:
        # Mengonversi id ke ObjectId
        update_id = ObjectId(update_id)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Invalid ObjectId format"
        })
    
    all_docs = collection.find_one({"_id": update_id})

    if all_docs:
        result_array.append({
            "id": str(all_docs.get('_id', '')),
            "title": all_docs.get('title', ''),
            "description": all_docs.get('description', ''),
            "bg_image": all_docs.get('bg_image', ''),
            "profile_image": all_docs.get('profile_image', ''),
            "created_at": all_docs.get('created_at', ''),
            "updated_at": all_docs.get('updated_at', ''),
        })

        return jsonify({
            "status": "success",
            "data": result_array
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Document not found"
        })
        
@app.route('/diary', methods=['POST'])
def save_diary():
    title = request.form['title']
    description = request.form["description"]

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    image_time = datetime.now().strftime('%Y-%m-%d-%H-%M')
    
    bg_image = request.files['bg_image']
    extension = bg_image.filename.split('.')[1]
    bg_temp = f'bg_{random.randint(1, 1000)}_{image_time}.{extension}'
    bg_save_path = f'static/images/background/{bg_temp}'
    bg_image.save(bg_save_path)

    profile_image = request.files['profile_image']
    extension = profile_image.filename.split('.')[1]
    profile_temp = f'prfl_{random.randint(1, 1000)}_{image_time}.{extension}'
    profile_save_path = f'static/images/profile/{profile_temp}'
    profile_image.save(profile_save_path)
    
    if not title or not description or not bg_image or not profile_image:
        return jsonify({'msg': 'Missing required data!'}), 400
    result = collection.insert_one({
        "title" : title,
        "description" : description,
        "bg_image": bg_save_path,
        "profile_image": profile_save_path,
        "created_at": current_time,
        "updated_at": ""
        })
    return jsonify({'status': 'success'})
@app.route('/diary_update', methods=['POST'])
def update_diary():
    update_id = request.form['update_id']
    title = request.form['title']
    description = request.form["description"]

    if not title or not description:
        return jsonify({'msg': 'Missing required data!'}), 400

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    new_data = {
        "title": title,
        "description": description,
        "updated_at": current_time
    }

    result = collection.update_one(
        {"_id": ObjectId(update_id)},
        {"$set": new_data}
    )
    
    if result.modified_count > 0:
        return jsonify({'status': 'success', 'msg': 'Document updated successfully'})
    else:
        return jsonify({'status': 'error', 'msg': 'No changes made to the document'}), 400

@app.route('/diary_delete', methods=['POST'])
def delete_diary():
    delete_id = request.form['delete_id']

    if not delete_id:
        return jsonify({'msg': 'ID is required!'}), 400

    result = collection.delete_one({"_id": ObjectId(delete_id)})

    if result.deleted_count > 0:
        return jsonify({'status': 'success', 'msg': 'Document deleted successfully'})
    else:
        return jsonify({'status': 'error', 'msg': 'Document not found'}), 404
    

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)
