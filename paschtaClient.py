# -*- coding: cp1252 -*-
#jython -Dpython.path=ClientInterface-2.0.4.jar cookclient_url.py

from com.clt.dialog.client import Client
from com.clt.script.exp import Value
import java.lang.Object

# eigene Klasse
from rezept_class import *

# Java Swing für GUI
from java.awt import BorderLayout, Color
from javax.swing import JPanel, JFrame, JTextArea, JButton, BoxLayout, Box, JTextField
from javax.swing import JLabel
from javax.swing import ImageIcon
from java.awt import Color
from java.awt import Dimension
from java.lang import Class



class Main(Client):
    def __init__(self):
        self.recipe = None

    def stateChanged(self, cs):
        print "new state: " + str(cs)

    def sessionStarted(self):
        print "session started"

    def reset(self):
        print "reset"

    # "URL"
    # "ingredients"
    # "exists_zutat" Bezeichnung
    # "Zutaten" Bezeichnung Mengenangabe (Einheit | 0)
    # "zutaten" ("all" | Bezeichnung)
    # "eigenschaft" ("Arbeitszeit" | "Ruhezeit" | "Koch-/Backzeit" | "Gesamtzeit" | "Schwierigkeitsgrad" | "Kalorien")
    # "anleitung" ("first" | "next" | "previous" | "repeat" | "last" | "all")
    # "titel"
    # "einheiten"
    # "einkaufszettel"
    # "Zettel" Text
    # "portionen" "wert"
    # "Personen" Anzahl
    def output(self, value):
        value = list(value)# value hat jetzt den Typ Value list
        # das erste Element von value zeigt an, was passieren soll
        category = value[0].getString().strip('"')

        # Quelltext für Rezept abfragen
        if category == "URL":
            self.gui()

        # erstellt Liste mit allen Zutaten (ohne Mengenangaben)
        elif category == "ingredients":
            self.send(self.recipe.ingredients())
            
        # erstellt Liste mit allen Einheiten
        elif category == "einheiten":
            self.send(self.recipe.einheiten())
                
        # fragt den Titel des Rezepts ab
        elif category == "titel":
            self.send(self.recipe.get_title())

        # kompletten Einkaufszettel schreiben
        elif category == "einkaufszettel":
            self.send(self.recipe.einkaufszettel("all"))
            # TODO: what does this send?

        # einzelne Zutat auf Einkaufszettel (keine Rückmeldung an den Dialog)
        elif category == "Zettel":
            self.recipe.einkaufszettel(value[1].getString().strip('"'))

        # gibt Text-Antwort zurück, ob eine Zutat gebraucht wird
        elif category == "exists_zutat":
            self.send(self.recipe.contains(value[1].getString().strip('"')))
            
        # gibt zurück, für wie viele Personen das Rezept kalkuliert ist
        elif category == "portionen":
            self.send(str(self.recipe.get_portions()))

        # fürs Umrechnen nach Personen
        elif category  == "Personen":
            self.send(self.recipe.umrechnen(value[1].getString().strip('"'), u'Personen'))
        # fürs Umrechnen nach Zutaten
        elif category == "Zutaten":
            z = value[1].getString().strip('"')
            m = value[2].getString().strip('"')
            e = str(value[3]).strip('"') # hier str() und nicht getString(), weil value[3] ein IntValue ist
            self.send(self.recipe.umrechnen([m,e], z))

        # gibt die komplette Anleitung oder einen Schritt zurück
        elif category == "anleitung":
            # Funktionsargument aus {"first","next","previous","repeat","last","all"}
            self.send(self.recipe.get_schritt(value[1].getString().strip('"')))
        
        # gibt alle Zutaten oder einzelne Zutaten zurück (mit Mengenangaben, falls vorhanden)
        elif category == "zutaten": 
            self.send(self.recipe.get_zutat(value[1].getString().strip('"')))
        
        # auslesen der Eigenschaften wie Arbeitszeit, Schwierigkeitsgrad etc.
        elif category == "eigenschaft":
            self.send(self.recipe.get_property(value[1].getString().strip('"')))
        
        else:
            print("Fehler in call; Kategorie '" + category + "' ist ungültig")
            self.send("Fehler")
            # TODO: raise Error!

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
            print("created recipe for " + self.recipe.get_title())
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


