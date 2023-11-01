from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://ditiya:sparta@cluster0.rc6xlci.mongodb.net/')

db = client.dbsparta

app = 	Flask('__name__')

@app.route('/')
def home():
	return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    num = db.bucket.count_documents({}) + 1
    doc = {
    	'num': num,
    	'bucket': bucket_receive,
    	'done': 0
    }

    db.bucket.insert_one(doc)
    return jsonify({'msg': 'data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    db.bucket.update_one(
        {'num': int(request.form['num_give'])},
        {'$set':{'done':1}}
        )
    
    return jsonify({'msg': 'Update done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.bucket.find({},{'_id':False}))
    return jsonify({'buckets': bucket_list})

@app.route('/delete', methods=["POST"])
def bucket_delete():
    db.bucket.delete_one({'num':int(request.form['num_give'])})
    return jsonify({'msg': 'bucket deleted!'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)