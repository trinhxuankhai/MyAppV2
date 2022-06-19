from bs4 import BeautifulSoup
import requests
import random
import webbrowser
import threading
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock, mainthread
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.metrics import dp
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivy.factory import Factory
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineListItem
from kivy.utils import get_color_from_hex 
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivymd.uix.taptargetview import MDTapTargetView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.imagelist.imagelist import MDSmartTile
from kivy.core.window import Window
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


datas = []
random_data = []
clear_status = True
set_url = ""
district_dict = {'1':[False, '1'], '2':[False, '4'], '3':[False, '5'], '4':[False, '6'],
            '5':[False, '7'], '6':[False, '8'], '7':[False, '9'], '8':[False, '10'],
            '9':[False, '11'],  '10':[False, '12'], '11': [False, '13'], '12': [False, '14'],
            '13':[False, '15'], '14':[False, '16'], '15':[False, '17'], '16':[False, '19'],
            '17':[False, '2'], '18':[False, '18']}


def clear(instance):
  global clear_status
  if clear_status:
    for key in district_dict:
      district_dict[key][0] = False

Builder.load_file('navigate.kv')
Builder.load_file('mybottomsheet.kv')
Builder.load_file('windowmanager.kv')
Builder.load_file('result.kv')

class WindowManager(ScreenManager):
  pass
class Navigation(MDScreen):
  pass
class Waiting(MDScreen):
  pass
class Random(MDScreen):
  pass
class CircleLabel(MDFloatLayout):
    overallscore = StringProperty()
class MD2Card(MDCard):
    img_url = StringProperty()
class MD1Card(MDCard, RoundedRectangularElevationBehavior):
  pass
class ResultScreen(MDScreen):
  pass

class MD4Card(MDSmartTile, ButtonBehavior):
  text = StringProperty()
  source = StringProperty()
  url = StringProperty()



class MD3Card(MDCard):
  text = StringProperty()
  source = StringProperty()
  url = StringProperty()
class PersonalApp(MDApp):
    custom_sheet = None

    @mainthread
    def get_data(self):
      global set_url
      list_temp = random.choice(datas)
      url = list_temp[1]
      set_url = url
      # open url
      score = []
      session = requests.Session()
      retry = Retry(connect=3, backoff_factor=0.5)
      adapter = HTTPAdapter(max_retries=retry)
      session.mount('http://', adapter)
      session.mount('https://', adapter)
      html_text = session.get(url).text
      soup = BeautifulSoup(html_text, "html.parser")
      #Getting score
      temp = soup.find('div', {"id" : "res-summary-point"})
      score.append(temp.find('div', class_ = "microsite-point-avg").text.strip())
      points_group = temp.find_all('div', class_ = "microsite-top-points")
      for point in points_group:
        score.append(point.find('span').text)
      #Getting address
      temp = soup.find('div', class_="res-common-add")
      streetaddress = temp.find("span", {'itemprop': "streetAddress"}).text
      district = temp.find("span", {'itemprop': "addressLocality"}).text
      region = temp.find("span", {'itemprop': "addressRegion"}).text
      address = f"{streetaddress}, {district}, {region}"
      #Get time
      temp = soup.find('div', class_="res-common-price")
      time = temp.find_all('span')[2].text.strip()
      #Label Process
      label = ""
      if (len(list_temp[0]) > 18):
        label = list_temp[0][0:18] + "..."
      #Get image url:
      temp = soup.find('div', class_="microsite-box-popular-pic")
      images = temp.find_all('div', class_="micro-home-album")
      img_url_dict = []
      for image in images:
        img_url_dict.append(image.find('img')['src'])
      #Set
      temp = self.root.get_screen("random").ids
      temp.im_sync_1.source = list_temp[2]
      temp['card'].ids.label1.text = label
      temp['card'].ids.address.text = address
      temp['card'].ids.clock.text = time
      temp['card'].ids.score1.text = score[1]
      temp['card'].ids.score2.text = score[2]
      temp['card'].ids.score3.text = score[3]
      temp['card'].ids.score4.text = score[4]
      temp['card'].ids.overallscore.text = score[0]

      temp = self.root.get_screen("random").ids.card.ids.container3
      temp_dict = temp.ids
      for key in temp_dict:
        temp.remove_widget(temp_dict[key])
      for i in range(0, len(img_url_dict)):
        item = MD2Card(img_url = img_url_dict[i])
        temp.add_widget(item)
        temp.ids[f"item{i}"] = item
      
      self.ChangeScene("random")



    @mainthread
    def RandomStore(self):
      self.ChangeScene("wait")
      Clock.schedule_once(self.background_start_collect, 2)
      
      

    def Continue(self):
      self.ChangeScene("main")
    def ReRandom(self):
      self.RandomStore()
    def GoToNext(self):
      global set_url
      webbrowser.open(set_url)
      set_url = ""

    def district_search(self):
      district = ""
      datas.clear()
      for key in district_dict:
        if district_dict[key][0]:
          if(district == ""):
            district = district + district_dict[key][1]
          else:
            district = district + ',' + district_dict[key][1]
          district_dict[key][0] = False
      if(district == ""):
        self.ChangeScene("main")
        return
      else:
        self.get_district(district)
    def get_district(self, str):
      # open url
      url = f'https://www.foody.vn/ho-chi-minh/dia-diem?CategoryGroup=food&dtids={str}'
      new_url = ''
      index = 1
      while True:
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        html_text = session.get(url).text
        soup = BeautifulSoup(html_text, "html.parser")
        temps = soup.find_all('div', class_ = "row-item filter-result-item")
        for temp in temps:
          store = temp.find('a')
          img = store.find('img')
          store_name = store['title'].strip()
          store_info = 'https://www.foody.vn' + store['href']
          datas.append((store_name, store_info, img['src']))
        # Get next page
        next_page = soup.find('div', {'id' : 'scrollLoadingPage'})
        new_url = next_page.find('a')['href']
        if(new_url == url):
          break
        else:
          url = new_url
      print('Finished!!')
      self.Draw()
      
    def build(self):
      self.sm = WindowManager()
      return self.sm
    
    def bottom_sheet(self):
      self.custom_sheet = MDCustomBottomSheet(screen=Factory.ContentCustomSheet())
      self.custom_sheet.bind(on_dismiss = clear) 
      self.custom_sheet.open()
      
    def check_box(self, checkbox, value):
      if checkbox.md_bg_color == get_color_from_hex("#ffffff"):
        checkbox.md_bg_color = get_color_from_hex("#A478C6")
        checkbox.text_color = get_color_from_hex("#ffffff")
        district_dict[value][0] = True
      else:
        checkbox.md_bg_color = get_color_from_hex("#ffffff")
        checkbox.text_color = get_color_from_hex("#A478C6")
        district_dict[value][0] = False
      #print(district_dict)
    
    def run_url(self, url):
      webbrowser.open(url)

    @mainthread
    def ChangeScene(self, str): 
      self.sm.current = str

    @mainthread
    def Draw(self):
      global clear_status
      temp = self.root.get_screen("main").ids.container2
      temp_dict = temp.ids
      for key in temp_dict:
        temp.remove_widget(temp_dict[key])
      for i in range(0, len(datas)):
        item = MD4Card(text = datas[i][0],url = datas[i][1], source = datas[i][2])
        temp.add_widget(item)
        temp.ids[f"item{i}"] = item
      clear_status = True     
      self.RandomStore()

    def background_start(self, dt):
      t = threading.Thread(target=self.district_search)
      t.daemon = True
      t.start()

    def background_start_collect(self, dt):
      t = threading.Thread(target=self.get_data)
      t.daemon = True
      t.start()
        

    def callback(self):
      global clear_status
      clear_status = False
      self.custom_sheet.dismiss()
      self.ChangeScene("wait")
      Clock.schedule_once(self.background_start, 2)
      
    


if __name__ == '__main__':
  PersonalApp().run()
 
