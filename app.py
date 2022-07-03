from flask import Flask, request, jsonify
import mysql.connector
from functools import wraps
# import sqlite3 as sql

try:
    app = Flask(__name__)

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="@1Nfr4struktur",
        database="uasapi"
    )      
    cursor = mydb.cursor()
  
    # mydb = sql.connect('hp.db')
    # mydb.execute("CREATE TABLE `handphone` (`id` int(11) NOT NULL,`nama` varchar(64) NOT NULL,`jenis` varchar(64) NOT NULL,`nomor` int(11) UNSIGNED ZEROFILL NOT NULL,`created_at` timestamp NOT NULL DEFAULT current_timestamp(),`updated_at` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp()ENGINE=InnoDB DEFAULT CHARSET=utf8mb4);")
    # mydb.close()

    print("Status Database : ", mydb.is_connected())
except Exception as e:
    print("Error : ", e)
    exit()

@app.route("/handphone", methods=['GET'])
def gethandphone():
    try:
        cursor.execute("SELECT * FROM handphone")
        # print(cursor.fetchall())
        result = []
        for i in cursor.fetchall():
            result.append({
                "id": i[0],
                "nama": i[1],
                "jenis": i[2],
                "nomor": i[3],
                "created_at": i[4],
                "updated_at": i[5]
            })
        # mydb.commit()
        return jsonify({"data":result, "code": 200}), 200
    except Exception as e:
        return jsonify({"data":str(e), "code": 500}), 500

@app.route("/handphone/<int:id>", methods=['GET'])
def gethandphonebyid(id):
    try:
        cursor.execute("SELECT * FROM handphone WHERE id = %s" % (id,))
        i = cursor.fetchone()
        result = {
            "id": i[0],
            "nama": i[1],
            "jenis": i[2],
            "nomor": i[3],
            "created_at": i[4],
            "updated_at": i[5]
            }
        return jsonify({"data":result, "code": 200}), 200
    except Exception as e:
        return jsonify({"data":str(e), "code": 500}), 500

@app.route("/handphone", methods=['POST'])
def inserthandphone():
    try:
        data = request.json
        sql = "INSERT INTO handphone (id, nama, jenis, nomor) VALUES (NULL, %s, %s, %s)"
        value = (data['nama'], data['jenis'], data['nomor'])
        cursor.execute(sql, value)
        mydb.commit()
        return jsonify({"data":"1 Record Inserted!", "code": 200}), 200
    except Exception as e:
        return jsonify({"data":str(e), "code": 500}), 500

@app.route("/handphone/<int:id>", methods=['PUT'])
def updatehandphonebyid(id):
    try:
        data = request.json
        sql = "UPDATE handphone SET nama = %s, jenis = %s, nomor = %s WHERE id = %s"
        value = (data['nama'], data['jenis'], data['nomor'], id)
        cursor.execute(sql, value)
        mydb.commit()
        return jsonify({"data":"1 Record Affected!", "code": 200}), 200
    except Exception as e:
        return jsonify({"data":str(e), "code": 500}), 500

@app.route("/handphone/<int:id>", methods=['DELETE'])
def deletehandphonebyid(id):
    try:
        cursor.execute("DELETE FROM handphone WHERE id = %s" % (id,))
        return jsonify({"data":"1 Record Deleted!", "code": 200}), 200
    except Exception as e:
        return jsonify({"data":str(e), "code": 500}), 500

if "__main__" == __name__:
    # app.run(port=1000)
    # app.run(debug=True, port=1000)
    app.run(debug=True, host="0.0.0.0", port=2000)
