from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine

from tools.py_files.widgets.zequentlabel import ZequentLabel

class ZequentExpansionPanel(MDExpansionPanel):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    
    def build(self):
        pass