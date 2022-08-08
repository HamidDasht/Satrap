from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
import sqlite3

DBNAME = "satrap_test.db"

# A list of newly added account informations
DB_JOURNAL = []

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

        query = "SELECT name, email, phone, account, password FROM account_info"
        self.cursor.execute(query)
        return  self.cursor.fetchall()

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
    """
    A box layout for a single record of account_info.
    Contains account's info plus buttons for modifying, deleting, copying, and showing full details.
    """
    def __init__(self, data_record, **kwargs):
        """
        data_record contains account information as a dictionary. This dictionary has 5 keys:
            name
            email
            phone
            account
            password
        """
        self.name = data_record['name']
        self.email = data_record['email']
        self.phone = data_record['phone']
        self.account = data_record['account']
        self.password = data_record['password']

        super().__init__(**kwargs)
        self._add_row(data_record)

    def _add_row(self, data_record):
        """
            Adds the row to the scrollview's list
        """
        self.add_widget(Label(text=self.name))
        self.add_widget(Label(text=self.email))
        self.add_widget(Label(text=self.phone))
        self.add_widget(Label(text=self.account))
        self.add_widget(Label(text=self.password))



class InputEntryLayout(BoxLayout):
    pass

class RecordsGridLayout(GridLayout):
    """
    The GridLayout a series of CDataLayout box layouts each containing a record of account_info.

    data_rows list contains a list of CDataLayouts that represent a row in the account info list
    """
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)        
        
        # Retrive records from database
        account_records = db_object.fetch_all_records()
        
        self.data_rows = []

        for record in account_records:
            # Convert columns to string
            record = list(map(str, record))

            self.add_new_row(record)
        

    def add_new_row(self, record):
        """
            Gets a list that contains account information, turns the list into
            a dictionary for making referencing easier, then creates 
            CDataLayout which contains the record's data plus controllers
        """
        # Turn the list into a dictionary for making referencing easier
        record = dict(zip(['name','email','phone','account','password'], record))
            
        # Create CDataLayout which contains the record's data plus controllers
        new_row = CDataLayout(record)
        self.data_rows.append(new_row)
        self.add_widget(new_row)


class AddPage(BoxLayout):
    """
    Box Layout containing all elements of create account page.
    """


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def add_button_pressed(self, email_widget, pass_widget, mobile_no_widget, account_widget, name_widget):
        """
        Arguments: TextInput Widget of Email Address, Password, Mobile Number, Account Address, First Name and Last name
        
        Check text inputs. If they are not empty, and they are valid, create a new account info.
        """


        # Get text from TextInput widgets
        email_str = email_widget.text
        pass_str = pass_widget.text
        mobile_no_str = mobile_no_widget.text
        account_str = account_widget.text
        name_str = name_widget.text
        print("add pressed", email_str, pass_str, mobile_no_str, account_str, name_str)
        print(self.parent.parent.children[1].children[2].children[0].children[1])
        # Check validity
        if email_str and pass_str and mobile_no_str and account_str and name_str:
            # Create the new account info
            db_object.add_new_account(name_str, email_str, mobile_no_str, account_str, pass_str)
            
            # Add new row to the DB_JOURNAL's list so that when we go to the scrollview's tab,
            # all of these rows are read by the scrollview and added to the RecordsGridLayout's list
            # and displayed.
            DB_JOURNAL.append([name_str, email_str, mobile_no_str, account_str, pass_str])


            # Clear TextInput forms
            email_widget.text = ""
            pass_widget.text = ""
            mobile_no_widget.text = ""
            account_widget.text = ""
            name_widget.text = ""
            
            
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
    """
        This is the tab that contains the list of account informations
        
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def _update_list(self, widget):
        """
            We keep a list of newly added account informations in DB_JOURNAL when AddTab is activated.
            The moment ListTab is clicked, DB_JOURNAL list is read, and all the account informations are
            added to the account information list in ListTab's page.
            
            widget: is the pointer to ListTab. We have to traverse its children to find RecordsGridLayout
        """
        
        for row in DB_JOURNAL:
            records_grid_layout = widget.children[0].children[0]
            records_grid_layout.add_new_row(row)
            
        if len(DB_JOURNAL) > 0:
            DB_JOURNAL.clear()

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
        db_object.close_db_connection()
