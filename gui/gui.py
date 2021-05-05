import kivy
from kivy.core.text import markup
from kivy.uix.layout import Layout
from kivy.uix.scrollview import ScrollView
from search_engine.Searcher import Searcher
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
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
import webbrowser

class KApp(MDApp):
    result = None
    
    def build(self):
        Window.clearcolor=hex('#f6f6f6')
        self.layout = FloatLayout()
        
        self.searcher = Searcher()
        self.textQ = MDTextField(pos_hint={"x": 0.2, "top": 0.89}, size_hint=(0.4, 0.05), text="search...")
        self.courseQ = MDTextField(pos_hint={"x": 0.62, "top": 0.89}, size_hint=(0.1, 0.05), text="code")
        self.logo = Image(pos_hint={"x": 0, "top": 1}, size_hint=(0.2, 0.2), source='gui/logo.png')
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
        
        self.result = self.searcher.search(self.textQ.text, self.courseQ.text)
        self.create_datatable()
        self.add_widgets()
        
        
    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''
        row_nr = self.data_tables.table_data._rows_number
        per_row = self.data_tables.table_data.rows_num
        
        idx = int(instance_row.index/6) + row_nr*per_row
        def openlink(self,link):
            webbrowser.open(url)

        
        code = self.result[idx]['_source']['function_code']
        url = self.result[idx]['_source']['repo_url']
        content = RelativeLayout()
        url_view = ScrollView(pos_hint={"x":0.0, "y": .45}, size_hint=(1,1))
        url_content = Label(pos_hint={"x": 0.0, "top": 0},text="[u][ref=link]{}[/ref][/u]".format(url),markup=True, color=[0,0,1,1], size_hint_x= None)
        url_content.bind(texture_size=url_content.setter('size'))
        url_content.bind(size_hint_min_x=url_content.setter('width'))
        url_content.bind(on_ref_press=openlink)
        url_view.add_widget(url_content)
        content.add_widget(url_view)

        code_view = ScrollView(pos_hint={"x":0.0, "y": 0.0}, size_hint=(1,0.9))
        code_content = Label(text=code, markup=True, color=[0,0,0,1], size_hint_x= None, size_hint_y=None)
        code_content.bind(texture_size=code_content.setter('size'))
        code_content.bind(size_hint_min_x=code_content.setter('width'))
        code_content.bind(size_hint_min_y=code_content.setter('height'))
        code_view.add_widget(code_content)

        content.add_widget(code_view)
        popup = Popup(title=self.result[idx]['_source']['function_name'],
                        content=content, 
                        size_hint=(.8, .8),
                        background_color=[255,255,255,1],
                        title_color=[0,0,0,1])
        popup.open()
        



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
