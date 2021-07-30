from kivy.animation import Animation
from kivy.lang import Builder
from kivy.utils import get_color_from_hex

from kivymd.app import MDApp
from kivymd.utils.fitimage import FitImage
import os
root = 'C:/Users/lenovo/Desktop/study/Pythonhigh/kivy/kivy_venv/my/picture'
KV = '''
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: app.theme_cls.bg_light

    MDToolbar:
        id: toolbar
        title: "Inbox"
        md_bg_color: app.theme_cls.bg_light
        specific_text_color: 0, 0, 0, 1

    MDBoxLayout:
        padding: "24dp", "8dp", 0, "8dp"
        adaptive_size: True

        MDLabel:
            text: "Today"
            adaptive_size: True

    ScrollView:

        MDSelectionList:
            id: selection_list
            padding: "24dp", 0, "24dp", "24dp"
            cols: 3
            spacing: "12dp"
            overlay_color: app.overlay_color[:-1] + [.2]
            icon_bg_color: app.overlay_color
            progress_round_color: app.progress_round_color
            on_selected: app.on_selected(*args)
            on_unselected: app.on_unselected(*args)
            on_selected_mode: app.set_selection_mode(*args)
'''


class Example(MDApp):
    overlay_color = get_color_from_hex("#6042e4")
    progress_round_color = get_color_from_hex("#ef514b")

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        # file_path ---> list
        path_dir = root
        file_lists = os.listdir(path_dir)
        for file_list in file_lists:
            self.root.ids.selection_list.add_widget(
                FitImage(
                    source=root+'/'+file_list,
                    size_hint_y=None,
                    height="240dp",
                )
            )

    def set_selection_mode(self, instance_selection_list, mode):
        if mode:
            md_bg_color = self.overlay_color
            left_action_items = [
                [
                    "close",
                    lambda x: self.root.ids.selection_list.unselected_all(),
                ]
            ]
            right_action_items = [
                [
                    "ok",lambda x: self.root.ids.selection_list.unselected_all(),
                ]
            ]
        else:
            md_bg_color = (1, 1, 1, 1)
            left_action_items = []
            right_action_items = []
            self.root.ids.toolbar.title = "Gallery"

        Animation(md_bg_color=md_bg_color, d=00.1).start(self.root.ids.toolbar)
        self.root.ids.toolbar.left_action_items = left_action_items
        self.root.ids.toolbar.right_action_items = right_action_items

    def on_selected(self, instance_selection_list, instance_selection_item):
        select_list = []
        self.root.ids.toolbar.title = str(
            len(instance_selection_list.get_selected_list_items())
        )
        # select_list.extend()
        print(select_list)

    def on_unselected(self, instance_selection_list, instance_selection_item):
        if instance_selection_list.get_selected_list_items():
            self.root.ids.toolbar.title = str(
                len(instance_selection_list.get_selected_list_items())
            )


Example().run()