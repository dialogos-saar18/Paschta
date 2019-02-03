# -*- coding: cp1252 -*-
#jython -Dpython.path=ClientInterface-2.0.4.jar cookclient_url.py
from com.clt.dialog.client import Client
from com.clt.script.exp import Value
#from testmodule import *
import java.lang.Object
from rezept_class import *

from java.awt import BorderLayout, Color
from javax.swing import JPanel, JFrame, JTextArea, JButton, BoxLayout, Box, JTextField
from javax.swing import JLabel
from javax.swing import ImageIcon
from java.awt import Color
from java.awt import Dimension
from java.lang import Class

# Hilfsfunktion; ruft die Methoden auf, die die Informationen auslesen
def call(category, term, recipe):
    # gibt die komplette Anleitung oder einen Schritt zurück
    if category == "anleitung":
        # term Element von {"first","next","repeat","all","previous", "last"}
        return(recipe.get_schritt(term))
    # gibt alle Zutaten oder einzelne Zutaten zurück
    elif category == "zutaten": 
        return(recipe.get_zutat(term))
    # auslesen der Eigenschaften wie Arbeitszeit, Schwierigkeitsgrad etc.
    elif category == "eigenschaft":
        return(recipe.get_property(term))
    else:
        print("Fehler in call; Kategorie " + category + " ist ungültig")
        return ("ungültig")
        # TODO: raise Error! 

# TODO: Leerzeichen

class Main(Client):
    def __init__(self):
        self.recipe = None
        pass    

    def stateChanged(self, cs):
        print "new state: " + str(cs)

    def sessionStarted(self):
        print "session started"

    def reset(self):
        print "reset"

    # "URL"
    # "ingredients"
    # "ingredients" rezept
    # "title"
    # "title" rezept
    # "einkaufszettel"
    # "einkaufszettel" rezept
    # "anleitung"/"zutat"/"eigenschaft" suchbegriff
    # "anleitung"/"zutat"/"eigenschaft" suchbegriff rezept
    # "portionen" "wert"
    # "exists_zutat" suchbegriff
    def output(self, value):
        value = list(value)
        # value hat jetzt den Typ Value list
        # TODO: key = value[0].getString().strip('"')

        # Quelltext für Rezept abfragen
        if value[0].getString().strip('"') == "URL":
            self.gui()
            print("created recipe")
            # TODO: print title

        # erstellt Liste mit allen Zutaten 
        elif value[0].getString().strip('"')=="ingredients":
            self.send(self.recipe.ingredients())
            
        # erstellt Liste mit allen Einheiten
        elif value[0].getString().strip('"')=="einheiten":
            self.send(self.recipe.einheiten())
                
        # fragt den Titel des Rezepts ab
        elif value[0].getString().strip('"')=="titel":
            self.send(self.recipe.get_title())

        # kompletten Einkaufszettel schreiben
        elif value[0].getString().strip('"')=="einkaufszettel":
            self.send(self.recipe.einkaufszettel("all"))
            # TODO: what does this send?

        # einzelne Zutat auf Einkaufszettel (keine Rückmeldung an den Dialog)
        elif value[0].getString().strip('"')=="Zettel":
            self.recipe.einkaufszettel(value[1].getString().strip('"'))

        # gibt Antwort zurück, ob eine Zutat gebraucht wird
        elif value[0].getString().strip('"')=="exists_zutat":
            self.send(self.recipe.contains(value[1].getString().strip('"')))

        # TODO
        elif value[0].getString().strip('"')=="zutaten":
            self.send(self.recipe.get_zutat(value[1].getString().strip('"')))
            
        # gibt zurück, für wie viele Personen das Rezept kalkuliert ist
        elif value[0].getString().strip('"')=="portionen":
            if value[1].getString().strip('"')== "wert":
                self.send(str(self.recipe.get_portions()))
            # TODO: else

        # fürs Umrechnen nach Personen
        elif value[0].getString().strip('"') == "Personen":
            self.send(self.recipe.umrechnen(value[1].getString().strip('"'),u'Personen'))
        # fürs Umrechnen nach Zutaten
        elif value[0].getString().strip('"')=="Zutaten":
            z = value[1].getString().strip('"')
            m = value[2].getString().strip('"')
            e = value[3].getString().strip('"')
            self.send(self.recipe.umrechnen([m,e],z))

        # reset Schrittindex (wenn <TODO>)
        elif value[0].getString().strip('"') == "ende":
            self.recipe.schritt = 0

        # TODO: what does it do and what it the first element? (make this an elif and throw error if not match
        else:
            self.send(call(value[0].getString().strip('"'), value[1].getString().strip('"'), self.recipe))

        # TODO: test
        print "output: " + "done (" + str(value) + ")"

    def getName(self):
        return "Paschta Client"

    def error(self, throwable):
        print "error"

    # öffnet eine GUI, in der man eine URL eintippen kann
    # erstellt ein Rezeptobjekt anhand der URL
    def gui(self):

        # Hilfsfunktion für event  
        # erstellt ein Rezeptobjekt anhand einer URL
        # schließt die GUI
        def create(event):
            url = field.getText()
            self.recipe = Recipe(url)
            frame.dispose()
            # der Dialog wartet, bis "continue" gesendet wird
            self.send("continue")

        # Frame erstellen
        frame = JFrame('URL eingeben',
                defaultCloseOperation = JFrame.EXIT_ON_CLOSE,
                size = (480,200),
                       )
        frame.setLayout(None)
        
        # Text im Frame
        fieldlabel = JLabel()
        fieldlabel.setText("<html><font size=+1>Geben Sie die Internetadresse des Rezepts ein</font></html>")
        fieldlabel.setBounds(20,20,500,40)
        frame.add(fieldlabel)

        # Textfeld im Frame
        field = JTextField()
        field.setText("https://www.chefkoch.de/rezepte/...")
        field.setBounds(20,60,411,40)
        frame.add(field)

        # Button im Frame
        # ruft Hilfsfunktion create auf
        button = JButton("Los!", actionPerformed = create)
        button.setBounds(155,100,150,30)
        frame.add(button)

        #Frame anzeigen
        frame.setVisible(True)


m = Main()
m.open(8880)


