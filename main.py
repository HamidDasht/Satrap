import enum
from kivy.properties import StringProperty
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from dbconnection import DBConnection
import arabic_reshaper
from bidi.algorithm import get_display
from kivy.core.window import Window
from image_button import ImageButton
from kivy.uix.behaviors import FocusBehavior


Q1_OPTIONS = \
(
"What is the first name of your best friend in high school?",
"What was the name of your first pet?",
"What was the first thing you learned to cook?",
"What was the first film you saw in the theater?",
"Where did you go the first time you flew on a plane?",
"What is the last name of your favorite elementary school teacher?"
)

Q2_OPTIONS = \
(
"What is your dream job?",
"What is your favorite children's book?",
"What was the model of your first car?",
"What was your childhood nickname?",
"Who was your favorite film star or character in school?",
"Who was your favorite singer or band in high school?"
)

Q3_OPTIONS = \
(
"In what city did your parents meet?",
"What was the first name of your first boss?",
"What is the name of the street where you grew up?",
"What is the name of the first beach you visited?",
"What was the first album that you purchased?",
"What is the name of your favorite sports team?",
)


# A list of newly added account informations
DB_JOURNAL = []

# Minimum length for searchable text
MIN_SEARCH_TEXT_LENGTH = 3

# Global Database Object
db_object = DBConnection()


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
            q1
            q2
            q3
            birthdate
        """

        self.name = data_record['name']
        self.email = data_record['email']
        self.phone = data_record['phone']
        self.account = data_record['account']
        self.password = data_record['password']
        self.q1 = data_record['q1']
        self.q2 = data_record['q2']
        self.q3 = data_record['q3']
        self.birthdate = data_record['birthdate']

        super().__init__(**kwargs)
        self._add_row(data_record)

    def _add_row(self, data_record):
        """
            Adds the row to the scrollview's list
        """

        # If name is written in Persian, render it in Persian
        if self.name.isascii():
            name_label = Label(text=self.name)
        else:
            name_label = Label(text=get_display(arabic_reshaper.reshape(self.name)), font_name="Fonts/IranSans.ttf")
        
        self.add_widget(name_label)
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
        self.fill_records_list()
        
    def fill_records_list(self):
        """
            Fetches all the records in 'account_info' table from the database
            and fills the RecordsGridLayout with these rows.
        """
        # Retrive records from database
        account_records = db_object.fetch_all_records()
        
        for record in account_records:
            # Convert columns to string
            record = list(map(str, record))
            self.add_new_row(record)
        
    def fill_with_records(self, records_list):
        """
            Gets a list of records and fills the ReordsGridLayout with them
        """
        for record in records_list:
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
        record = dict(zip(['name','email','phone','account','password','q1','q2','q3','birthdate'], record))
            
        # Create CDataLayout which contains the record's data plus controllers
        new_row = CDataLayout(record)
        self.add_widget(new_row)


class AddPage(BoxLayout):
    """
    Box Layout containing all elements of create account page.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def add_button_pressed(self, email_widget, pass_widget, mobile_no_widget, account_widget, name_widget, q1, q1_answer,
    q2, q2_answer, q3, q3_answer, birthdate_widget):
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
        birthdate = birthdate_widget.text
        q1_str = f'{q1}:{q1_answer.text}'
        q2_str = f'{q2}:{q2_answer.text}'
        q3_str = f'{q3}:{q3_answer.text}'
        print("add pressed", email_str, pass_str, mobile_no_str, account_str, name_str, birthdate, q1_str, q2_str, q3_str)
        
        # Check validity
        if email_str and pass_str and mobile_no_str and account_str and name_str:
            # Create the new account info
            db_object.add_new_account(name_str, email_str, mobile_no_str, account_str, pass_str, q1_str, q2_str, q3_str, birthdate)
            
            # Add new row to the DB_JOURNAL's list so that when we go to the scrollview's tab,
            # all of these rows are read by the scrollview and added to the RecordsGridLayout's list
            # and displayed.
            DB_JOURNAL.append([name_str, email_str, mobile_no_str, account_str, pass_str, q1_str, q2_str, q3_str, birthdate])

            # Clear TextInput forms
            email_widget.text = ""
            pass_widget.text = ""
            mobile_no_widget.text = ""
            account_widget.text = ""
            name_widget.text = ""
            birthdate_widget.text = ""
            q1_answer.text = ""
            q2_answer.text = ""
            q3_answer.text = ""
        else:
            self._show_error_()

    def _show_error_(self):
        """
        Show a warning/error when input texts are invalid.
        """
        self.add_widget(Label(text="There's a problem!"))


class ListPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.records_grid_layout : RecordsGridLayout = None

    def on_search_press(self, search_text_input):
        """
            Triggered when the user clicks search button or presses enter for text validation.

            'search_text_input' is a reference to a TextInput widget.

            Search is done only if the text inside `search_text_inside` is longer than MIN_SEARCH_TEXT_LENGTH
        """

        # Check search text's length
        if len(search_text_input.text) < MIN_SEARCH_TEXT_LENGTH:
            return

        # Reference to RecordsGridLayout which contains all the account records
        self.records_grid_layout = self.children[0].children[0]

        # Bind `text` property to `_on_text_update_` to repeat the search when
        # text gets updated.
        search_text_input.bind(text = self._on_text_update_)
        
        # Do the search
        self._show_searched_records_(search_text_input.text)
        
    def _on_text_update_(self, text_input, text):
        """
            Repeat the search each time the search text is changed until
            its length gets lower than `MIN_SEARCH_TEXT_LENGTH`
        """
        search_text_len = len(text)

        # If length gets lower than `MIN_SEARCH_TEXT_LENGTH` unbind this function
        # and exit search mode by restoring all of the records.
        if search_text_len < MIN_SEARCH_TEXT_LENGTH:
            text_input.unbind(text = self._on_text_update_)
            self._remove_all_records_()
            self._restore_all_records_()

        # Do search based on the search text
        elif search_text_len >= MIN_SEARCH_TEXT_LENGTH:
            self._show_searched_records_(text)


    def _show_searched_records_(self, search_text):
        self._remove_all_records_()
        searched_records = db_object.fetch_searched_records(search_text)
        self.records_grid_layout.fill_with_records(searched_records)
    
    def _remove_all_records_(self):
        """
            Removes all records from the observable list.
            Has no effect on the database.
        """
        self.records_grid_layout.clear_widgets()

    def _restore_all_records_(self):
        """
            Redisplay all records and add them to the observable list. 
            Has no effect on the database.
        """
        self.records_grid_layout.fill_records_list()

        
class TabbedWindow(TabbedPanel):
    pass

class ListTab(TabbedPanelItem):
    """
        This is the tab that contains the list of account informations
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def _update_list(self, list_page_widget):
        """
            We keep a list of newly added account informations in DB_JOURNAL when AddTab is activated.
            The moment ListTab is clicked, DB_JOURNAL list is read, and all the account informations are
            added to the account information list in ListPage.
            
            list_page_widget: is the pointer to ListPage. We have to traverse its children to find RecordsGridLayout
        """
        
        for row in DB_JOURNAL:
            records_grid_layout = list_page_widget.children[0].children[0]
            records_grid_layout.add_new_row(row)
            
        if len(DB_JOURNAL) > 0:
            DB_JOURNAL.clear()


class AddTab(TabbedPanelItem):
    pass
        

class SatrapApp(App):
    def build(self):
        return TabbedWindow()


class RecordsHeadingLabel(Label):
    """
        Add support for Persian for RecordsHeadingLabel
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(text = self.on_pawn)

    def on_pawn(self, label_widget, label_text):
        self.unbind(text = self.on_pawn)
        self.text = get_display(arabic_reshaper.reshape(label_text))

class InputFormLabel(Label):
    """
        Add support for Persian for InputFromLabels
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(text = self.on_pawn)

    def on_pawn(self, label_widget, label_text):
        self.unbind(text = self.on_pawn)
        self.text = get_display(arabic_reshaper.reshape(label_text))


class QuestionDropDown(DropDown, FocusBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _on_focus(self, instance, value, *largs):
        print(self)

class MySpinner(Spinner, FocusBehavior):
    pass
    #def _on_focus(self, instance, value, *largs):
        #pass
        #self.is_open = True
        #self.value = self.values[0]

if __name__ == '__main__':

    try:
        #print(dir(Window))
        SatrapApp().run()
    finally:
        db_object.close_db_connection()

