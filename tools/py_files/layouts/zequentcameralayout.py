from tools.py_files.layouts.casuals.zequentfloatlayout import *
from kivy.uix.button import Button

class ZequentCameraLayout(ZequentFloatLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def test(self,button:Button, *args):
        
        popIndex = 0
        buttonCopy = 0
        for child in self.children:
            if not button.__eq__(child) and not str(child.size_hint).__contains__('0.25'):
                child.size_hint = 0.25,0.25
                copy = child
                self.remove_widget(child)
                self.add_widget(copy, index=0)
            elif not button.__eq__(child) and str(child.size_hint).__contains__('0.25'):
                child.size_hint = 1,1
            elif button.__eq__(child):
                buttonCopy = child
            popIndex += popIndex +1

        self.remove_widget(buttonCopy)
        self.add_widget(buttonCopy)
        copy.bind(on_press=self.test)
       
        
        
    def build(self):
        pass