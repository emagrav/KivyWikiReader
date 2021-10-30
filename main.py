# importiamo classe MDApp
from kivymd.app import MDApp
from kivy.lang import Builder

KV = """
Screen:

     # https://kivy.org/doc/stable/guide/widgets.html#organize-with-layouts
    GridLayout:
        rows: 2

        ScrollView:
            # https://kivymd.readthedocs.io/en/latest/components/label/
            MDLabel:
                id: mdlab
                text: "Benvenuti su Wikipedia Reader"
                # font_style: "H1"
                # padding_x: 30
                size_hint_y: None
                height: self.texture_size[1]
                # la grandezza del testo avrà come larghezza del widget stesso (MDLabel)
                # nel senso che andrà ad espandersi per tutta la larghezza della label
                # mentre l'altezza sarà None (non definita) e quindi illimitata. Ciò ci
                # consentirà di effettuare lo scrolling dal momento che questa label ha
                # come genitore Scroll View
                text_size: self.width, None

        # https://kivymd.readthedocs.io/en/latest/components/button/#mdraisedbutton
        MDRaisedButton:
            id: mdbu
            text: "PREMI QUESTO TASTO!"
            # https://kivy.org/doc/stable/api-kivy.uix.widget.html?highlight=size_hint_x#kivy.uix.widget.Widget.size_hint_x
            # size_hint_x:1 equivale al 100% della larghezza del genitore e quindi, 
            # in questo caso, della schermata
            # 0.5 equivale al 50%
            size_hint_x: 1 # 0.0 - 1.0
            on_press: app.tasto_ricerca_casuale_premuto()
"""

class WikiReaderApp(MDApp):
    
    def build(self):
        self.title = "WikipediaReader"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.primary_hue = "200" # la saturazione (rispetto ad es. a 400 abbiamo un indigo più chiaro)
        return Builder.load_string(KV)

    def tasto_ricerca_casuale_premuto(self):
        # dizionario dei widget presenti nell'app dove usando come chiave l'id del widget
        # otteniamo come valore l'oggetto widget stesso
        self.root.ids["mdlab"].text = "Tasto ricerca casuale premuto"
        # per curiosità stampo questo dizionario per vedere cosa contiene
        print(self.root.ids)

WikiReaderApp().run()

