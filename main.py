import os

import fuel
import model
import mysql.connector
from mysql.connector import errorcode

from flask import Blueprint, render_template, request, jsonify, Flask
from werkzeug.utils import redirect

import ast, json


def create_app():
  application = Flask(__name__)
  return application

app = create_app()

# Obtain connection string information from the portal
config = {
  'host':'dfsoilgas.mysql.database.azure.com',
  'user':'dfsuser@dfsoilgas',
  'password':'fuelingUp!',
  'database':'oilgas'
}

# LOCAL_SQLALCHEMY_DATABASE_URI = (
#   'mysql+pymysql://dfsuser@dfsoilgas:fuelingUp!@207.191.10.212/dfsoilgas')

type_to_keys = {
  'inventory': ['inventoryId', 'itemId', 'price', 'merchantId']
}

def tuple_to_dict(type, t):
  return dict(zip(type_to_keys[type], t))

def makeConnection():
  # Construct connection string
  try:
     conn = mysql.connector.connect(**config)
     print("Connection established")
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with the user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
  else:
    cursor = conn.cursor()

    # addUser("Alice", "1", "0", "14", cursor)
    # addUser("Bob", "2", "1", "39", cursor)
    # addUser("Charlie", "7", "1", "51", cursor)
    # addUser("Dan", "3", "0", "24", cursor)
    # addUser("Ed", "4", "0", "20", cursor)
    # addUser("Fred", "5", "0", "17", cursor)
    # addUser("George", "6", "1", "60", cursor)

    # addMerchant("Seven Eleven", "111", cursor)
    # addMerchant("Circle K", "225", cursor)
    # addMerchant("Costco Gas", "354", cursor)
    # addMerchant("HEB Gas", "587", cursor)
    # addMerchant("Speedway", "469", cursor)

    # addInventory("23","10.00","6", cursor)
    # addInventory("24", "19.99", "6", cursor)
    # addInventory("25", "25.00", "6", cursor)
    #
    # addInventory("26", "9.99", "7", cursor)
    # addInventory("27", "29.99", "7", cursor)
    # addInventory("28", "14.99", "7", cursor)
    #
    # addInventory("29", "5.99", "8", cursor)
    # addInventory("30", "19.99", "8", cursor)
    # addInventory("23", "39.99", "8", cursor)

    # addItems("Cigarettes", "https://image.flaticon.com/icons/svg/595/595593.svg", cursor)
    # addItems("Milk", "https://image.flaticon.com/icons/svg/372/372973.svg", cursor)
    # addItems("Eggs", "https://image.flaticon.com/icons/svg/1951/1951379.svg", cursor)
    # addItems("Beer", "https://image.flaticon.com/icons/svg/931/931949.svg", cursor)
    # addItems("Chips", "https://image.flaticon.com/icons/png/512/2137/2137628.png", cursor)
    # addItems("Candy", "https://image.flaticon.com/icons/png/512/2454/2454268.png", cursor)
    # addItems("Coffee", "https://image.flaticon.com/icons/svg/1046/1046785.svg", cursor)

    #cleanUp(conn, cursor)

makeConnection()

def cleanUp(conn, cursor):
  # Cleanup
  conn.commit()
  cursor.close()
  conn.close()
  print("Done.")


def addUser(name, password, isMerchant, age, cursor):

  # Insert some data into table
  cursor.execute("INSERT INTO users (username, password, isMerchant, age) VALUES (%s, %s, %s, %s);", (name, password, isMerchant, age))
  print("Inserted", cursor.rowcount, "row(s) of data.")
  cursor.execute("commit;")

def addMerchant(name, code, cursor):

  cursor.execute("INSERT INTO merchants (name, code) VALUES (%s, %s);",
                 (name, code))
  print("Inserted", cursor.rowcount, "row(s) of data.")
  cursor.execute("commit;")


def addInventory(itemId, price, merchantId, cursor):
  cursor.execute("INSERT INTO inventory (itemId, price, merchantId) VALUES (%s, %s, %s);",
                 (itemId, price, merchantId))
  print("Inserted", cursor.rowcount, "row(s) of data.")
  cursor.execute("commit;")

def addItems(name, image, cursor):
  cursor.execute("INSERT INTO items (name, imageUrl) VALUES (%s, %s);",
                 (name, image))
  print("Inserted", cursor.rowcount, "row(s) of data.")
  cursor.execute("commit;")

def getUserById(id, cursor):
  cursor.execute("SELECT * FROM users WHERE id =", id)

def getUser(name, cursor):
  cursor.execute("SELECT * FROM users where username = {}".format(name))
  user = cursor.fetchall()
  return user

def getItemsById(id, cursor):
  cursor.execute("SELECT * from items WHERE id = {};".format(id))

def getInventory(id, cursor):
  cursor.execute("SELECT * FROM inventory where merchantId = {};".format(id))
  rows = cursor.fetchall()
  print("Read", cursor.rowcount, "row(s) of data.")
  li = []
  for row in rows:
    id = row[1]
    cursor.execute("SELECT * from items WHERE id = {};".format(id))
    item = cursor.fetchall()[0]
    di = tuple_to_dict('inventory', row)
    di['itemId'] = item[0]
    li.append(di)

  return li


@app.route('/', methods=['GET', 'POST'])
def home():
  return "True"


@app.route('/getInventory/<id>', methods=['GET', 'POST'])
def getInventoryByMerchant(id):

  conn = mysql.connector.connect(**config)
  cursor = conn.cursor()
  items = getInventory(id, cursor)
  return jsonify(items)


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':

    data = request.form.to_dict(flat=True)
    print(data)
    name = data['username']
    password = data['password']
    # n = str(request.form['username'])
    # print(n)
    user = getUser(name)
    print("user")
    print(user)

  # if user is not None:
    ## check if password matches one in database


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8080, debug=True)