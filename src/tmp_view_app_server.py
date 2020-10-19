import sys
from flask import Flask
from flask_cors import cross_origin


def calcOp(text):
    
    return "abc"

app = Flask(__name__)

@app.route("/<input>")
@cross_origin()
def calc(input):    
    return calcOp(input)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001)
