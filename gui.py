import kivy
from kivy.uix.layout import Layout
import Searcher
kivy.require('2.0.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
#from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton as Button



class KApp(MDApp):
    result = None
    
    def build(self):
        Window.clearcolor=hex('#f6f6f6')
        self.layout = FloatLayout()
        
        self.searcher = Searcher.Searcher()
        self.textQ = MDTextField(pos_hint={"x": 0.2, "top": 0.89}, size_hint=(0.4, 0.05), text="search...")
        self.courseQ = MDTextField(pos_hint={"x": 0.62, "top": 0.89}, size_hint=(0.1, 0.05), text="code")
        self.logo = Image(pos_hint={"x": 0, "top": 1}, size_hint=(0.2, 0.2), source='logo.png')
        self.submit_button = Button(pos_hint={"x": 0.74, "top": 0.88}, size_hint=(0.2, 0.05), text='search', text_color=hex('#fffff'), md_bg_color=hex('#00579d'), on_press=self.submit)
        
        #label = Label(text='search', font_size=20, pos_hint={"x": -0.05, "y": 0.47}, color=hex("#000000"))
        #layout.add_widget(label)

        self.create_datatable()
        self.add_widgets()
        
        return self.layout

    def add_widgets(self):
        self.layout.add_widget(self.data_tables)
        self.layout.add_widget(self.textQ)
        self.layout.add_widget(self.courseQ)
        self.layout.add_widget(self.logo)
        self.layout.add_widget(self.submit_button)

    def submit(self, obj):
        
        self.layout.clear_widgets()
        print("Searching for ", self.textQ.text, self.courseQ.text)
        self.result = self.searcher.search(self.textQ.text, self.courseQ.text)
        self.create_datatable()
        self.add_widgets()
        print(self.result)
        
    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''
        print(self.result[int(instance_row.index/5)]['_source']['function_code'])
        #print(instance_table, instance_row)


    def create_datatable(self):
        if self.result != None:
            row_data=[
                (
                    f"{i + 1}",
                    f"{self.result[i]['_source']['function_name']}",
                    f"{self.result[i]['_source']['repo_name']}",
                    f"{self.isKth(self.result[i]['_source']['isKth'])}",
                    f"{self.getCourseCode(self.result[i]['_source']['kth_course_code'])}",
                    f"{self.result[i]['_score']:.3f}",
                )
                for i in range(len(self.result))
            ]
            if(len(self.result)%5 == 1):
                row_data.append(("","","","","",""))
            
        else:
            row_data=[
               # ("","","","","",)
            ]
        self.data_tables = MDDataTable(
            pos_hint={"x": 0.075, "top": 0.75},
            size_hint=(0.85, 0.62),
            use_pagination=True,
            #agination_menu_height='0',
            rows_num=5,
            # name column, width column, sorting function column(optional)
            column_data=[
                ("#", dp(7)),
                ("Name", dp(55)),
                ("Repo", dp(30)),
                ("", dp(7)),
                ("Course", dp(15)),
                ("Score", dp(15))
            ],
            row_data=row_data,
        )
        self.data_tables.bind(on_row_press=self.on_row_press)
    
    def isKth(self,bool):
        return "K" if bool else ""

    def getCourseCode(self, code):
        return code if code is not None else ""

if __name__ == '__main__':
    KApp().run()
