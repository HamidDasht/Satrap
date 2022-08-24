import sqlite3

DBNAME = "satrap_test.db"

class DBConnection():
    def __init__(self) -> None:
        # Connect to DB and create a cursor
        self.sqliteConnection = sqlite3.connect(DBNAME)
        self.cursor = self.sqliteConnection.cursor()
        print('DB Init')
    
        # Write a query and execute it with cursor
        query = 'select sqlite_version();'
        self.cursor.execute(query)
    
        # Fetch and output result
        result = self.cursor.fetchall()
        print('SQLite Version is {}'.format(result))

        # Initializes the database if it's empty
        self._initialize_database_()
    

    def _initialize_database_(self):
        """
        Check database. Initialize the database if it's empty
        """

        self.cursor.execute("SELECT name FROM sqlite_master")

        # If the list of tables is empty create table
        list_of_tables = self.cursor.fetchall()
        if len(list_of_tables) == 0:
            self.cursor.execute("""
                                    CREATE TABLE account_info 
                                    (
                                        ID INTEGER PRIMARY KEY autoincrement,
                                        name TEXT NOT NULL,
                                        email TEXT NOT NULL,
                                        phone TEXT NOT NULL,
                                        account TEXT NOT NULL,
                                        password TEXT NOT NULL,
                                        q1 TEXT NOT NULL,
                                        q2 TEXT NOT NULL,
                                        q3 TEXT NOT NULL,
                                        birthdate TEXT NOT NULL
                                    )
                                """)
            print("DB Initialized.")

    def add_new_account(self, name, email, phone, account, password, q1, q2, q3, birthdate):
        """
            Creates a new row in 'account_info' table using provided arguments
        """

        self.cursor.execute("""INSERT INTO account_info (name, email, phone, account, password, q1, q2, q3, birthdate) 
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""", (name, email, phone, account, password, q1, q2, q3, birthdate))

        # Save this change
        self.sqliteConnection.commit()

    def fetch_all_records(self):
        """
            Fetches and returns all records in 'account_info' table.
            
            Returns a [list] containing all of these records.
        """

        query = "SELECT name, email, phone, account, password, q1, q2, q3, birthdate FROM account_info"
        self.cursor.execute(query)
        return  self.cursor.fetchall()

    def delete_record(self, name, email, phone, account, password):
        self.cursor.execute("""DELETE FROM account_info WHERE name = ? AND email = ? AND
        phone = ? AND account = ? AND password = ?;""", (name, email, phone, account, password))

    def close_db_connection(self):
        """
            Close the cursor and connection when program crashes or is exited.
        """

        # Close the cursor
        self.cursor.close()

        # Close DB Connection 
        if self.sqliteConnection:
            self.sqliteConnection.close()
            print('SQLite Connection closed')

    def fetch_searched_records(self, search_text):
        """
            Fetches records based on `search_text` parameter.

            If `search_text` is numeric, searches mobile numbers.
            Otherwise seaches email, account, and name fields.
        """

        if search_text.isnumeric():
            query = f"SELECT name, email, phone, account, password, q1, q2, q3, birthdate FROM \
                 account_info WHERE phone LIKE '%{search_text}%'"    
        else:
            query = f"""SELECT name, email, phone, account, password, q1, q2, q3, birthdate FROM account_info WHERE 
                    name LIKE '%{search_text}%' OR
                    email LIKE '%{search_text}%' OR
                    account LIKE '%{search_text}%'
                    """
        
        self.cursor.execute(query)
        return  self.cursor.fetchall()


