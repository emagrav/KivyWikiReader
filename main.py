# importiamo classe MDApp
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
import certifi

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
            text: " CERCA ARTICOLO CASUALE!"
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
        self.theme_cls.primary_palette = "Indigo" # "Teal"
        self.theme_cls.primary_hue = "200" # la saturazione (rispetto ad es. a 400 abbiamo un indigo più chiaro)
        return Builder.load_string(KV)

    def tasto_ricerca_casuale_premuto(self):
        endpoint = "https://it.wikipedia.org/w/api.php?action=query&list=random&rnlimit=1&rnnamespace=0&format=json"
        # dizionario dei widget presenti nell'app dove usando come chiave l'id del widget
        # otteniamo come valore l'oggetto widget stesso
        self.root.ids["mdlab"].text = "Caricamento in corso..."

        # per curiosità stampo questo dizionario per vedere cosa contiene
        print(self.root.ids)

        self.rs_request = UrlRequest(endpoint, 
                                    on_success=self.get_data,
                                    ca_file=certifi.where()
                                    )
    
    def get_data(self, request, response):
        print(response)
        # es: {..., 'query': {'random': [{'id': 6442725, 'ns': 0
        # , 'title': 'Collegio elettorale di Como II (Regno di Sardegna)'}]}}
        
        # il primo e unico elemento della lista è un dizionario
        random_article = response["query"]["random"][0]
        random_title = random_article["title"]
        #self.root.ids["mdlab"].text = random_title
        # vado a sostituire gli spazi con %20 per gli url
        endpoint = f"https://it.wikipedia.org/w/api.php?prop=extracts&explaintext&exintro&format=json&action=query&titles={random_title.replace(' ', '%20')}"
        
        self.data_request = UrlRequest(endpoint, 
                                    on_success=self.set_textarea,
                                    ca_file=certifi.where()
                                    )
    def set_textarea(self, request, response):
        print(response)
        # es: {..., 'query': {'pages': {'8768111': {'pageid': 8768111, 'ns': 0
        # , 'title': 'Harry Clarke', 'extract': "Henry Patrick Clarke (Dublino, 
        # 17 marzo 1889 – Coira, 6 gennaio 1931) è stato un artista e illustratore 
        # di libri irlandese.\nÈ stato una figura di spicco nell'Irish Arts and 
        # Crafts Movement.\nIl suo lavoro è stato influenzato sia dal movimento 
        # Art Nouveau che da quello Art Deco. Il suo vetro colorato è stato 
        # particolarmente informato dal movimento simbolista francese"}}}}}
        page_info = response["query"]["pages"]
        
        # dal momento che non possiamo conoscere a priori il pageid dell'articolo,
        # iteriamo e prendiamo il primo (la prima chiave del dizionario ottenuto)
        # grazie a next dell'oggetto iterabile
        page_id = next(iter(page_info)) 
        
        print(page_id)
        
        page_title = page_info[page_id]["title"]
        page_extract = page_info[page_id]["extract"]
        
        print(page_title)
        print(page_extract)

        self.root.ids["mdlab"].text = f"{page_title}\n\n{page_extract}"
# nota che ovviamente bisogna aggiungere dentro buildozer.spec 
# il modulo certifi dopo kivymd
# ed inoltre siccome la nostra app ha bisogno di una connessione
# internet per funzionare, andra decommentato l'istruzione
#   android.permissions = INTERNET
# come consiglia un video (https://www.youtube.com/watch?v=T3rOvpDzEOY&ab_channel=kenechukwuAkubue), 
# ho messo la versione ==2.0.0 a kivy
# e poi aggiunto pillow (che da quando l'ho messo ha funzionato!)
# decommentato anche
#   android.logcat_filters = *:S python:D
# e poi infine lanciato la build con questi parametri
#    buildozer android debug deploy run logcat
# ma deploy serve se si attacca al pc il cell android a cui 
# viene immediatamente deployata e installata l'app
# run penso che lo faccia avviare subito mentre logcat genera
# dei log che possono essere visionati con adb quando si usa
# l'app sul cell attaccato al pc
# pertanto è sufficiente
#       buildozer android debug
# nel caso ci fossero problemi che non vengono visualizzate
# correttamente le icone, dice di aggiungere 
#       sdl2_ttf==2.0.15 
# perché quello che usa buildozer di default
# non è quella corretta
# ora fai un tentativo alla volta con kivi_introduction e 
# cerca di raffinare questa soluzione trovata


WikiReaderApp().run()

