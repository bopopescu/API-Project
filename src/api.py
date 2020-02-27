import flask
from flask import jsonify, Flask
from flask import render_template
import mysql.connector as connector

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.errorhandler(404)
def not_found(e):
    return render_template('err404.html')


def connect():
    mydb = connector.connect(
        host='localhost',
        user='root',
        passwd='root',
        database='mazao'
    )
    return mydb


@app.route('/home', methods=['GET'])
def home():
    return render_template("index.html")


@app.route('/api/v1/resources/transaction/all', methods=['GET'])
def transaction():
    columns = []
    transaction_data = []
    try:
        mydb = connect()
    except connector.Error:
        return render_template('swh.html')
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT * FROM transaction;")
    data = cursor.fetchall()
    # Get table columns
    cursor.execute("SHOW COLUMNS FROM transaction;")
    data_columns = cursor.fetchall()
    for col in data_columns:
        columns.append(col[0])

    for single_row_data in data:
        i = 0
        transaction = {}
        for item in single_row_data:
            transaction[columns[i]] = item
            i += 1
        transaction_data.append(transaction)

    json_transaction_data = jsonify(transaction_data)
    return json_transaction_data


@app.route('/transactions')
def draw_transaction_table():
    json_data = transaction()


### Very large table. Would not recommend running in a weak computer ###
@app.route('/api/v1/resources/transactionentry/all')
def transaction_entry():
    columns = []
    transaction_entry_data = []
    try:
        mydb = connect()
    except connector.Error:
        print(connector.Error)
        return '''
                <h1>Check your internet connection</h1>
               '''
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT * FROM transactionentry;")
    data = cursor.fetchall()
    # Get table columns
    cursor.execute("SHOW COLUMNS FROM transactionentry;")
    data_columns = cursor.fetchall()
    for col in data_columns:
        columns.append(col[0])

    for single_row_data in data:
        i = 0
        transaction_entry = {}
        for item in single_row_data:
            transaction_entry[columns[i]] = item
            i += 1
        transaction_entry_data.append(transaction_entry)

    json_transaction_data = jsonify(transaction_entry_data)
    return json_transaction_data
##################################################################

@app.route('/settings')
def settings():
    return render_template('settings.html')


app.run()
