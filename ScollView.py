root = 'C:/Users/lenovo/Desktop/study/Pythonhigh/kivy/kivy_venv/my/picture'

import os 
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.list import OneLineIconListItem,ImageLeftWidget

# kivy lang
list_helper = """
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        ScrollView:
            MDList:
                id: container
        MDLabel:
            id: imgname
            text: 'Pick Image!'
            font_size: 32
            halign: 'center'
            font_style: 'H2'
            
        
        MDFillRoundFlatButton:
            text: 'PICK!'
            padding: '10px'
            on_press: print('a'),exit()
"""


class DemoApp(MDApp):

    def build(self):
        screen = Builder.load_string(list_helper)
        return screen

    def on_start(self):
        
        # file_path ---> list
        path_dir = root
        file_lists = os.listdir(path_dir)
        
        # icon list 
        for file_list in file_lists:
            image = ImageLeftWidget(source=root+'/'+file_list)
            items = OneLineIconListItem(text=file_list,on_press=lambda x, item=file_list: print(item))
            items.add_widget(image)
            self.root.ids.container.add_widget(items)
        
if __name__ == '__main__':
    DemoApp().run()