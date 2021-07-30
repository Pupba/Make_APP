from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.popup import Popup
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.uix.button import Button
from kivymd.uix.list import OneLineIconListItem,ImageLeftWidget,MDList
from kivy.uix.scrollview import ScrollView
import os 
import time
from YOLO import Yolo
Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
    Button:
        text: 'Start_Prediction'
        size_hint_y: None
        height: '48dp'
        on_press: root.run()
    Button:
        text: 'Pick_Img'
        size_hint_y: None
        height: '48dp'
        on_press: root.open_popup()
''')
class CameraClick(MDBoxLayout):
    img_name = ''
    root1 = 'C:/Users/lenovo/Desktop/study/Pythonhigh/kivy/kivy_venv/my/picture/'
    root2 = 'C:/Users/lenovo/Desktop/study/Pythonhigh/kivy/kivy_venv/my/picture'
    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        global imgname
        imgname = "IMG_{}.png".format(timestr)
        camera.export_to_png(CameraClick.root1+imgname)
        print("Captured") 

    def run(self):
        start = Yolo()
        start.run(CameraClick.img_name)

    def open_popup(self):
        # Layout
        box = MDBoxLayout(orientation='vertical') 
        # Label
        label_= MDLabel(text='Pick Image!',halign='center',font_style='H4')
        box.add_widget(label_)
        # ScrollList view
        path_dir = CameraClick.root2
        file_lists = os.listdir(path_dir)
        scroll = ScrollView()
        list_view = MDList()
        scroll.add_widget(list_view)

        for file_list in file_lists:
            image = ImageLeftWidget(source=CameraClick.root1+file_list)
            items = OneLineIconListItem(text=file_list,on_press=lambda x,item=file_list : self.text_press(label_,item))
            items.add_widget(image)
            list_view.add_widget(items)
        box.add_widget(scroll)
        # Button
        btn = MDFillRoundFlatButton(text='PICK!')
        box.add_widget(btn)
        #make popup
        the_popup = Popup(title='Test Popup',content=box,size_hint=(None,None),size=(640,500))
        #label_.text = '3' change text
        the_popup.open()
        # close popup
        btn.bind(on_press= lambda x: self.btn_press(the_popup))


    def text_press(self,label,text):
        CameraClick.img_name = text
        label.text = text
    def btn_press(self,popup):
        print(CameraClick.img_name)
        popup.dismiss()
class TestCamera(MDApp):

    def build(self):
        return CameraClick()


TestCamera().run()