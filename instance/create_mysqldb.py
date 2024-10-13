import pymysql
import sys

try:
    print("Attempting to connect to MySQL...")
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='1234'
    )
    print("Connected successfully.")

    with connection.cursor() as cursor:
        print("Creating database if it doesn't exist...")
        # cursor.execute("CREATE DATABASE our_users")
        cursor.execute("SHOW DATABASES")
        print("Database operation completed.")

    connection.close()
    print("Connection closed.")

except pymysql.Error as e:
    print(f"PyMySQL Error: {e}")
    print(f"Error Code: {e.args[0]}")
    print(f"Error Message: {e.args[1]}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    print(f"Error type: {type(e).__name__}")

print(f"Python version: {sys.version}")
print(f"PyMySQL version: {pymysql.__version__}")
print("Script completed.")