from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.utils import get_color_from_hex
from kivymd.uix.floatlayout import MDFloatLayout

from kivymd.app import MDApp
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.card import MDCard
from kivymd.app import MDApp
from kivy.core.window import Window
Window.size = (360, 740)

Builder.load_file('result.kv')

class CircleLabel(MDFloatLayout):
    overallscore = StringProperty()
class MD2Card(MDCard):
    img_url = StringProperty()
class MD1Card(MDCard, RoundedRectangularElevationBehavior):
    '''Implements a material design v3 card.'''
    label1 = StringProperty()
    address = StringProperty()
    clock = StringProperty()
    score1 = StringProperty()
    score2 = StringProperty()
    score3 = StringProperty()
    score4 = StringProperty()
    overallscore = StringProperty()
class ResultScreen(MDScreen):
  pass


class Test(MDApp):

    def build(self):
        return ResultScreen()


Test().run()