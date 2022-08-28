from os import remove
from kivy.uix.label     import Label
from kivy.uix.popup     import Popup
from kivy.uix.button    import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics       import dp
from dbconnection       import DBConnection
from functools          import partial

import pyperclip
import win32ui
import win32print
import win32con


def _getfontsize_(dc, PointSize):
    inch_y = dc.GetDeviceCaps(win32con.LOGPIXELSY)
    return int(-(PointSize * inch_y) / 72)


def show_info_popup(cdatalayout):
    """
    Shows a popup that contains cdatalayout's Q1 thorugh Q3 along with answers
    """
    info_popup = Popup( size_hint=(None, None), size=(dp(500),dp(300)), auto_dismiss=False)
    info_popup.title = f"Questions For {cdatalayout.account} Account "
    
    info_boxlayout = BoxLayout(orientation="vertical")
    q1, q1_ans = cdatalayout.q1.split(':')[0:2]
    q2, q2_ans = cdatalayout.q2.split(':')[0:2]
    q3, q3_ans = cdatalayout.q2.split(':')[0:2]
    birthdate = f'Birth Date: {cdatalayout.birthdate}'
    
    info_boxlayout.add_widget(Label(text=q1, text_size = (450,None), shorten=True))
    info_boxlayout.add_widget(Label(text=q1_ans, text_size = (450,None), shorten=True))
    info_boxlayout.add_widget(Label(text=q2, text_size = (450,None), shorten=True))
    info_boxlayout.add_widget(Label(text=q2_ans, text_size = (450,None), shorten=True))
    info_boxlayout.add_widget(Label(text=q3, text_size = (450,None), shorten=True))
    info_boxlayout.add_widget(Label(text=q3_ans, text_size = (450,None), shorten=True))
    info_boxlayout.add_widget(Label(text=birthdate, text_size = (450,None), shorten=True))
    info_boxlayout.add_widget(Button(text="Close", on_release=info_popup.dismiss))
    
    info_popup.add_widget(info_boxlayout)
    
    info_popup.open()

def show_delete_popup(cdatalayout):
    """
    Shows a confirmation popup for deleting cdatalayout's record
    """
    delete_popup = Popup( size_hint=(None, None), size=(dp(300),dp(200)), auto_dismiss=False)
    delete_popup.title = f"Deleting {cdatalayout.account} Record"

    delete_outer_boxlayout = BoxLayout(orientation="vertical")
    delete_outer_boxlayout.add_widget(Label(text="Sure?"))
    
    delete_inner_boxlayout = BoxLayout(orientation="horizontal", size_hint=(1,None), height=dp(40))
    reference_to_singleton_db = DBConnection()

    def remove_from_scroll_view(_):
        delete_popup.dismiss()
        grid_layout = cdatalayout.parent
        grid_layout.remove_widget(cdatalayout)

    delete_inner_boxlayout.add_widget(Button(text="Yes", on_press=lambda _ : reference_to_singleton_db.delete_record(
        cdatalayout.name,
        cdatalayout.email,
        cdatalayout.phone,
        cdatalayout.account,
        cdatalayout.password
    ), on_release=remove_from_scroll_view))
    delete_inner_boxlayout.add_widget(Button(text="No", on_release=delete_popup.dismiss))

    delete_outer_boxlayout.add_widget(delete_inner_boxlayout)

    delete_popup.add_widget(delete_outer_boxlayout)
    delete_popup.open()


def to_printer_and_clipbaord(cdatalayout):
    """
    Sends cdatalayout's data to both the default printer and the clipboard
    """
    hDC = win32ui.CreateDC()
    print(win32print.GetDefaultPrinter())  # test
    fontsize = _getfontsize_(hDC, 11)
    fontdata = { 'name':'Arial', 'height':fontsize, 'italic':True, 'weight':win32con.FW_NORMAL}
    font = win32ui.CreateFont(fontdata);
    try:
        hDC.CreatePrinterDC(win32print.GetDefaultPrinter())
        hDC.SelectObject(font)
        hDC.StartDoc("Test doc")
        hDC.StartPage()
        
        hDC.TextOut(500,1000, "Name:     " + cdatalayout.name)
        hDC.TextOut(500,1200, "Email:     " + cdatalayout.email)
        hDC.TextOut(500,1400, "Phone:    " + cdatalayout.phone)
        hDC.TextOut(500,1600, "Account:  " + cdatalayout.account)
        hDC.TextOut(500,1800, "Birthdate: " + cdatalayout.birthdate)
        hDC.TextOut(500,2000, "----------------------------------")
        hDC.TextOut(500,2200, "Password: " + cdatalayout.password)

        hDC.TextOut(500,2400, "Q1:       " + cdatalayout.q1.split(':')[0])
        hDC.TextOut(500,2600, "             " + cdatalayout.q1.split(':')[1])
        hDC.TextOut(500,2800, "Q2:       " + cdatalayout.q2.split(':')[0])
        hDC.TextOut(500,3000, "             " + cdatalayout.q2.split(':')[1])
        hDC.TextOut(500,3200, "Q3:       " + cdatalayout.q3.split(':')[0])
        hDC.TextOut(500,3400, "             " + cdatalayout.q3.split(':')[1])
        

        
        hDC.EndPage()
        hDC.EndDoc()
    except Exception:
        print(Exception)

    clipboard_str = f"""
{'Name:':11}{cdatalayout.name}
{'Email:':11}{cdatalayout.email}
{'Phone:':11}{cdatalayout.phone}
{'Account:':11}{cdatalayout.account}
{'Birthdate:':11}{cdatalayout.birthdate}
----------------------------------
{'Password:':11}{cdatalayout.password}
{'Q1:':11}{cdatalayout.q1.split(':')[0]}
{'':11}{cdatalayout.q1.split(':')[1]}
{'Q2:':11}{cdatalayout.q2.split(':')[0]}
{'':11}{cdatalayout.q2.split(':')[1]}
{'Q3:':11}{cdatalayout.q3.split(':')[0]}
{'':11}{cdatalayout.q3.split(':')[1]}
"""
    pyperclip.copy(clipboard_str)


def create_pdf():
    pass