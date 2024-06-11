import mysql.connector

database = mysql.connector.connect(
    host = 'localhost',
    user = 'admin',
    passwd = '976431'
    
)

cursorObject = database.cursor()

cursorObject.execute("CREATE DATABASE wcrm")

print("All done!")
