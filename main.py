from kivy.core.window import Window
from kivymd.uix.behaviors import backgroundcolor_behavior
Window.size = (400,600)
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.popup import Popup
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivymd.uix.button import MDFillRoundFlatButton,MDRectangleFlatButton
from kivy.uix.button import Button
from kivymd.uix.list import OneLineIconListItem,ImageLeftWidget,MDList,OneLineListItem
from kivy.uix.scrollview import ScrollView
import os 
import time
import webbrowser
from YOLO import Yolo
Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    size_hint: None,None
    size: 400,600
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
        theme_text_color: "Custom"
        font_size: 30
        color: 0,1,0,1
        background_color: 0, 4/255, 250/255
        bold: True
        italic: True
        outline_color: (0,0,0,0.5)
        outline_width: 5
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
        theme_text_color: "Custom"
        font_size: 30
        color: 0,1,0,1
        background_color: 0, 4/255, 250/255
        bold: True
        italic: True
        outline_color: (0,0,0,0.5)
        outline_width: 5
    Button:
        text: 'Pick_Img'
        size_hint_y: None
        height: '48dp'
        on_press: root.open_popup()
        theme_text_color: "Custom"
        font_size: 30
        color: 0,1,0,1
        background_color: 0, 4/255, 250/255
        bold: True
        italic: True
        outline_color: (0,0,0,0.5)
        outline_width: 5
    Button:
        text: 'Explanations'
        size_hint_y: None
        height: '48dp'
        on_press: root.open_html_lists()
        theme_text_color: "Custom"
        font_size: 30
        color: 0,1,0,1
        background_color: 0, 4/255, 250/255
        bold: True
        italic: True
        outline_color: (0,0,0,0.5)
        outline_width: 5
''')
class CameraClick(MDBoxLayout):
    img_name = ''
    root=os.getcwd().replace("\\", "/")
    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        # create folder
        if not os.path.isdir(CameraClick.root+'/picture') == True:
            os.mkdir(CameraClick.root+'/picture')
        global imgname
        imgname = "IMG_{}".format(timestr)
        camera.export_to_png(CameraClick.root+'/picture/'+imgname+'.png')
        os.rename(CameraClick.root+'/picture/'+imgname+'.png',CameraClick.root+'/picture/'+imgname+'.jpg')
        print("Captured") 

    def run(self):
        start = Yolo()
        start.run(CameraClick.img_name)

    def open_popup(self):
        if os.path.isdir(CameraClick.root +'/picture') == False:
            os.mkdir(CameraClick.root+ '/picture')
        # Layout
        box = MDBoxLayout(orientation='vertical')
        # Label
        label_= MDLabel(text='Pick Image!',halign='center',font_style='H4',theme_text_color="Custom"
        ,text_color=(255/255,187/255,0,1))
        box.add_widget(label_)
        # ScrollList view
        path_dir = CameraClick.root + "/picture"
        file_lists = os.listdir(path_dir)
        scroll = ScrollView()
        list_view = MDList()
        scroll.add_widget(list_view)

        for file_list in file_lists:
            image = ImageLeftWidget(source=path_dir+'/'+file_list)
            items = OneLineIconListItem(text=file_list,theme_text_color="Custom",
            text_color=(255/255,0,162/255,1),
            on_press=lambda x,item=file_list : self.text_press(label_,item))
            items.add_widget(image)
            list_view.add_widget(items)
        box.add_widget(scroll)
        # Button
        btn = MDFillRoundFlatButton(text='PICK! & RUN Model')
        box.add_widget(btn)
        #make popup
        the_popup = Popup(title='TEST POPUP',content=box,size_hint=(None,None),size=(350,500),
        background_color=(1,94/255,0,1))
        #label_.text = '3' change text
        the_popup.open()
        # close popup
        btn.bind(on_press= lambda x: self.btn_press(the_popup))


    def text_press(self,label,text):
        CameraClick.img_name = text
        label.text = text
    def btn_press(self,popup):
        print(CameraClick.img_name)
        self.run()
        popup.dismiss()
    def open_html_lists(self):
        if os.path.isdir(CameraClick.root + '/html') == False:
            os.mkdir(CameraClick.root + '/html')
        # Layout
        box = MDBoxLayout(orientation='vertical') 
        # ScrollList view
        path_dir = CameraClick.root + "/html"
        file_lists = os.listdir(path_dir)
        scroll = ScrollView()
        list_view = MDList()
        scroll.add_widget(list_view)
        for file_list in file_lists:
            items = OneLineListItem(text=file_list,theme_text_color="Custom",
            text_color=(255/255,0,162/255,1),on_press=lambda x,item=file_list: self.open_br(item))
            list_view.add_widget(items)
        box.add_widget(scroll)
        # Button
        btn = MDFillRoundFlatButton(text='Close')
        box.add_widget(btn)
        #make popup
        the_popup = Popup(title='HTML_LIST',content=box,size_hint=(None,None),size=(350,500),
        background_color=(252/255,252/255,0,1))
        the_popup.open()
        # close popup
        btn.bind(on_press= lambda x: the_popup.dismiss())
        
    def open_br(self,filename):
        # open html in window
        print(filename)
        url = self.root + '/html/' + filename # in url no hangul
        # browser path
        brave_path = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s'
        webbrowser.get(brave_path).open(url)

class TestCamera(MDApp):

    def build(self):
        return CameraClick()


TestCamera().run()