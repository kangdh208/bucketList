from flask import Flask, render_template, request, jsonify
from bson.objectid import ObjectId
app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://sparta:test@cluster0.bdeer72.mongodb.net/?retryWrites=true&w=majority')
db = client.dbbucket

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    bucket_list = list(db.bucket.find({}, {'_id': False}))
    count = len(bucket_list) + 1
    doc = {
        'num':count,  #버킷 등록 시, db에서 특정 버킷을 찾기 위해 'num' 이라는 고유 값 부여
        'bucket' :bucket_receive,
        'done' : 0   #'done' key값을 추가 해 각 버킷의 완료 상태 구분(0 = 미완료, 1 = 완료)
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})
    
@app.route("/bucket", methods=["GET"])
def bucket_get():
    all_buckets = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'result': all_buckets})

@app.route("/bucket", methods=["UPDATE"])
def bucket_finish():  # 완료
    id_receive = request.form["id_give"] # id 받아오기
    print(id_receive)
    # myDB = db["bucket"]
    # myCol = myDB["id_receive"]
    # print(myCol)
    # result = myCol.find({"_id":id_receive})
    # result.update_one("done", 1)  # 처리
    return jsonify({"msg": "수고했어요!"})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)