from curses import curs_set
from unicodedata import name
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
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
                                        password TEXT NOT NULL
                                    )
                                """)
            print("DB Initialized.")

    def add_new_account(self, name, email, phone, account, password):
        """
            Creates a new row in 'account_info' table using provided arguments
        """
        query = f"""INSERT INTO account_info (name, email, phone, account, password) 
                    VALUES('{name}', '{email}', '{phone}', '{account}', '{password}')"""
        self.cursor.execute(query)

        # Save this change
        self.sqliteConnection.commit()

    def fetch_all_records(self):
        """
            Fetches and returns all records in 'account_info' table.
            
            Returns a [list] containing all of these records.
        """

        query = "SELECT * FROM account_info"
        self.cursor.execute(query)
        return self.cursor.fetchall()

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


class CDataLayout(BoxLayout):
    pass

class InputEntryLayout(BoxLayout):
    pass

class AddPage(BoxLayout):
    """
    Box Layout containing all elements of create account page.
    """


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def add_button_pressed(self, email_str, pass_str, mobile_no_str, account_str, name_str):
        """
        Arguments: Email Address, Password, Mobile Number, Account Address, First Name and Last name
        
        Check text inputs. If they are not empty, and they are valid, create a new account info.
        """
        print("add pressed", email_str, pass_str, mobile_no_str, account_str, name_str)

        # Check validity
        if email_str and pass_str and mobile_no_str and account_str and name_str:
            # Create the new account info
            db_object.add_new_account(name_str, email_str, mobile_no_str, account_str, pass_str)
            pass
        else:
            self._show_error_()

    def _show_error_(self):
        """
        Show a warning/error when input texts are invalid.
        """
        self.add_widget(Label(text="There's a problem!"))


class ListPage(BoxLayout):
    pass

class TabbedWindow(TabbedPanel):
    pass

class ListTab(TabbedPanelItem):
    pass

class AddTab(TabbedPanelItem):
    pass

class MainGrid(GridLayout):
    pass
        
class SatrapApp(App):
    def build(self):
        return TabbedWindow()


# Global Database Object
db_object = DBConnection()

if __name__ == '__main__':

    try:
        SatrapApp().run()
    finally:
        print(db_object.fetch_all_records())
        db_object.close_db_connection()