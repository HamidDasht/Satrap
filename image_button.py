from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.metrics import dp

class HoverBehavior(object):
    """Hover behavior.
    :Events:
        `on_enter`
            Fired when mouse enter the bbox of the widget.
        `on_leave`
            Fired when the mouse exit the widget 
    """

    hovered = BooleanProperty(False)
    border_point= ObjectProperty(None)
    '''Contains the last relevant point received by the Hoverable. This can
    be used in `on_enter` or `on_leave` in order to know where was dispatched the event.
    '''

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return # do proceed if I'm not displayed <=> If have no parent
        pos = args[1]
        #Next line to_widget allow to compensate for relative layout
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            #We have already done what was needed
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_enter(self):
        pass

    def on_leave(self):
        pass

class ImageButton(ButtonBehavior, Image, HoverBehavior):
    hover_image = StringProperty()

    def on_enter(self):
        self.leave_img = self.source
        self.source = self.hover_image
    
    def on_leave(self):
        self.source = self.leave_img
    
    def more_info_pressed(self):
        cdatalayout = self.parent
        info_popup = Popup( size_hint=(0.5, 0.5), auto_dismiss=False)
        info_popup.title = cdatalayout.name

        info_boxlayout = BoxLayout(orientation="vertical")
        info_boxlayout.add_widget(Label(text=cdatalayout.q1))
        info_boxlayout.add_widget(Label(text=cdatalayout.q2))
        info_boxlayout.add_widget(Label(text=cdatalayout.q3))
        info_boxlayout.add_widget(Button(text="Close", on_release=info_popup.dismiss))
        
        info_popup.add_widget(info_boxlayout)
        info_popup.open()

    def delete_pressed(self):
        cdatalayout = self.parent
        delete_popup = Popup( size_hint=(0.5, 0.5), auto_dismiss=False)
        delete_popup.title = cdatalayout.name

        delete_outer_boxlayout = BoxLayout(orientation="vertical")
        delete_outer_boxlayout.add_widget(Label(text="Sure?"))
        
        delete_inner_boxlayout = BoxLayout(orientation="horizontal", size_hint=(1,None), height=dp(40))
        delete_inner_boxlayout.add_widget(Button(text="Yes"))
        delete_inner_boxlayout.add_widget(Button(text="No", on_release=delete_popup.dismiss))

        delete_outer_boxlayout.add_widget(delete_inner_boxlayout)

        delete_popup.add_widget(delete_outer_boxlayout)
        delete_popup.open()

    def copy_print_pressed(self):
        cdatalayout = self.parent


    def on_press(self):

        if self.text == "O":
            self.more_info_pressed()
        elif self.text == "D":
            self.delete_pressed()
        elif self.text == "C":
            self.copy_print_pressed()

        return super().on_press()
