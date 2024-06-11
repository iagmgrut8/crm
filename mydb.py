import mysql.connector

database = mysql.connector.connect(
    host = ' ',
    user = ' ',
    passwd = ' '
    
)

cursorObject = database.cursor()

cursorObject.execute("CREATE DATABASE wcrm")

print("All done!")
