import cx_Oracle

# Database configuration
dsn = "localhost:1521/XE"
username = "system"
password = "oracle"

# Attempt to establish a connection
try:
    cx_Oracle.init_oracle_client(lib_dir=r"C:\PROJECTFOLDER\instantclient_23_5")
    connection = cx_Oracle.connect(
        user=username,
        password=password,
        dsn=dsn,
        encoding="UTF-8"
    )
    print("Connection successful!")
    connection.close()
except cx_Oracle.DatabaseError as e:
    error, = e.args
    print(f"Database error code: {error.code}")
    print(f"Database error message: {error.message}")
except Exception as e:
    print(f"Unexpected error: {e}")
