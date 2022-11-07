import requests
from flask import Flask, request,jsonify
import json


TOKEN = '5718500704:AAGcjqRiyZ0DpzJXa25X_FcY03Xzzg6aPFo'

app = Flask(__name__)



@app.route("/",methods= ["GET",'POST'])
def hello_world():
    if request.method == 'POST':
        data = request.get_json()
        print(f'DATA: {data}')
        return{'statusCode': 200, 'body': 'Success','data': data}
    else:
        return{'statusCode':200, 'body':'Success'}

if __name__ == '__main__':
    app.run(debug=True)