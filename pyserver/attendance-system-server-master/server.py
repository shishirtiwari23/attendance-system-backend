from configparser import SectionProxy
from unicodedata import name
# from django import db
from flask import Flask, jsonify, request,json
from flask_cors import CORS, cross_origin
import sqlite3
import base64
# import requests
import re,time
from io import BytesIO
from PIL import Image
# import dbcon

app=Flask(__name__)
cors=CORS(app)

# db=sqlite3.connect('./attendance.db')


# app.config['CORS_HEADERS']='Content-Type'

def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    print(type(data))
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)

def db_connection():
    # conn = None
    # try:
    #     conn = sqlite3.connect("./attendance.db")
    # except sqlite3.error as e:
    #     print(e)
    # return conn
    pass

@app.route('/')
@cross_origin()
def checking(): 
    return jsonify({"hello":234})

@app.route('/data')
@cross_origin()
def getData():
    conn = sqlite3.connect("../../attendance.db")
    # conn = dbcon.connect()
    cur=conn.cursor();
    row=cur.execute('SELECT * FROM student').fetchall()
    print(row)
    return jsonify(row);


@app.route('/register', methods=['GET', 'POST'])
@cross_origin()
def register():
    conn = sqlite3.connect("../../attendance.db")
    # conn = dbcon.connect()
    cursor = conn.cursor()

    if(request.method =='POST'):
        new_id=request.form["uid"]
        new_name=request.form["name"]
        new_rollno=request.form["rollNo"]
        new_standard=request.form["standard"]
        new_section=request.form["section"]
        new_image=request.form["image"]
        sql = """INSERT INTO student (id, name, rollNo, standard, section)
                 VALUES (?, ?, ?, ?, ?)"""
        cursor = cursor.execute(sql, (new_id, new_name, new_rollno, new_standard, new_section))
        conn.commit()
        base64_data = re.sub('^data:image/.+;base64,', '', new_image)
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)
        t = time.time()
        img.save("../../Image_Folder/"+ new_id + "_" + new_name + "_" + new_standard +'.png', "PNG")
        # image_64_decode = base64.b64decode(image_64_encode) 
        # decoded = decode_base64(new_image)
        
        # decoded = base64.b64decode(new_image)
        # print(extra


        # bin_image = "".join(["{:08b}".format(x) for x in decoded])

        # with open("../Image Folder/"+ new_id + "_" + new_name + "_" + new_standard +'.jpg','wb') as f:
        #     f.write(image_data)
        return "Success"
    else:
        return jsonify('This is a get request')

app.run(host="0.0.0.0" , port=8080, debug=True)

