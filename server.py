from flask import Flask, request
from summarizer import extract_summary_and_keywords
from firebase import firebase
import csv
import json

app = Flask(__name__)

firebase = firebase.FirebaseApplication('https://reddys-4fd1a.firebaseio.com', None)

@app.route("/upload_file/<class_type>/<uploaded_file>",methods=['POST', 'GET'])
def upload_file(class_type, uploaded_file):
    """Upload file, extract knowledge and post to firebase"""
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        path = os.path.dirname(os.path.abspath(f))
        knowledge_dict = {class_type:path}
        extract_summary_and_keywords(knowledge_dict)
        return 200

@app.route("/classes_csv",methods=['POST', 'GET'])
def classes_csv():
    x = firebase.get('/update', "")
    # data_json = json.dumps(data_dict)
    # x = json.loads(data_json)
    # print(x)
    f = csv.writer(open("therapy.csv", "w"))
    f.writerow(['document_id', 'topic', 'link', 'class_type'])
    print(x.items())
    for key, value in x.items():
        f.writerow([value["document_id"],
                value["topic"],
                value["link"],
                value["class_type"]])
    return str(200)



 
if __name__ == "__main__":
    app.run(debug=True)