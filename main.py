import socket
from threading import Thread

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

HOTE = '127.0.0.1'
PORT = 5000


class FanasinaChatApp(App):

  def build(self):
    self.title = 'Fanasina'

    layout_principal = BoxLayout(orientation='vertical', padding=10, spacing=10)

    header = Label(
        text='[b]FANASINA CHAT[/b]',
        markup=True,
        size_hint_y=None,
        height=40,
        color=(0, 0.8, 0.4, 1),
    )
    layout_principal.add_widget(header)

    self.scroll = ScrollView(size_hint=(1, 1))
    self.zone_messages = BoxLayout(
        orientation='vertical', size_hint_y=None, spacing=5
    )
    self.zone_messages.bind(
        minimum_height=self.zone_messages.setter('height')
    )
    self.scroll.add_widget(self.zone_messages)
    layout_principal.add_widget(self.scroll)

    layout_saisie = BoxLayout(
        orientation='horizontal', size_hint_y=None, height=50, spacing=5
    )

    self.input_message = TextInput(
        hint_text='Écrivez votre message...', multiline=False
    )
    self.input_message.bind(on_text_validate=self.envoyer_message)
    layout_saisie.add_widget(self.input_message)

    btn_envoyer = Button(
        text='Envoyer', size_hint_x=None, width=100, background_color=(0, 0.7, 1, 1)
    )
    btn_envoyer.bind(on_press=self.envoyer_message)
    layout_saisie.add_widget(btn_envoyer)

    layout_principal.add_widget(layout_saisie)

    self.connecter_au_serveur()

    return layout_principal

  def ajouter_message(self, texte, alignement='left'):
    lbl = Label(
        text=texte,
        size_hint_y=None,
        height=30,
        halign=alignement,
        valign='middle',
    )
    lbl.bind(size=lbl.setter('text_size'))
    self.zone_messages.add_widget(lbl)
    self.scroll.scroll_y = 0

  def connecter_au_serveur(self):
    try:
      self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.client.connect((HOTE, PORT))
      self.ajouter_message('[ Système ] : Connecté à Fanasina !')
      Thread(target=self.recevoir_messages, daemon=True).start()
    except Exception:
      self.ajouter_message('[ Erreur ] : Service non disponible.')

  def envoyer_message(self, instance):
    texte = self.input_message.text.strip()
    if texte:
      try:
        self.client.send(texte.encode())
        self.ajouter_message(f'Moi : {texte}', alignement='right')
        self.input_message.text = ''
      except Exception:
        self.ajouter_message('[ Erreur ] : Échec envoi.')

  def recevoir_messages(self):
    while True:
      try:
        msg = self.client.recv(1024).decode()
        if msg:
          Clock.schedule_once(
              lambda dt, m=msg: self.ajouter_message(
                  f'Ami : {m}', alignement='left'
              )
          )
        else:
          break
      except Exception:
        break


if __name__ == '__main__':
  FanasinaChatApp().run()
