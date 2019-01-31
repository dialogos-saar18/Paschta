# -*- coding: cp1252 -*-
#jython -Dpython.path=ClientInterface-2.0.4.jar cookclient_url.py
from com.clt.dialog.client import Client
from com.clt.script.exp import Value
#from testmodule import *
import java.lang.Object
from rezept_class_url import *

from java.awt import BorderLayout, Color
from javax.swing import JPanel, JFrame, JTextArea, JButton, BoxLayout, Box, JTextField
from javax.swing import JLabel
from javax.swing import ImageIcon
from java.awt import Color
from java.awt import Dimension
from java.lang import Class


def call(category, term, recipe):
    #ruft die Methoden auf, die die Informationen auslesen
    if category == "anleitung": # gibt die komplette Anleitung oder einen Schritt zurück
        return(recipe.get_schritt(term)) # term Element von {"first","next","repeat","all","previous", "last"}
    elif category == "zutaten": # gibt alle Zutaten oder einzelne Zutaten zurück
        return(recipe.get_zutat(term)) 
    elif category == "eigenschaft":# auslesen der Eigenschaften wie Arbeitszeit, Schwierigkeitsgrad etc.
        return(recipe.get_property(term))
    else:#works
        print("Fehler in call; Kategorie " + category + " ist ungültig")
        return ("ungültig")
        ##raise Error! 



class Main(Client):
    def __init__(self):
        pass    

    def stateChanged(self, cs):
        print "new state: " + str(cs)

    def sessionStarted(self):
        print "session started"

    def reset(self):
        print "reset"

    #value has type string list (from the Value class)
    #die rezept-referenz ist ein int-Value
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

        #Quelltext für Rezept abfragen
        if value[0].getString().strip('"') == "URL":
            self.gui()
            #recipe = Recipe('https://www.chefkoch.de/rezepte/785281181805506/Spinat-Cannelloni-al-Forno.html')
            #self.recipes=[recipe]
            print("created recipe")            

        #erstellt Liste mit allen Zutaten 
        elif value[0].getString().strip('"')=="ingredients":
            if len(value)==1:
                self.send(self.recipes[0].ingredients())
            else:
                self.send(self.recipes[int(value[-1].getString())].ingredients())
        #erstellt Liste mit allen Einheiten
        elif value[0].getString().strip('"')=="einheiten":
            if len(value)==1:
                self.send(self.recipes[0].einheiten())
            else:
                self.send(self.recipes[int(value[-1].getString())].einheiten())
        #fragt den Titel des Rezepts ab
        elif value[0].getString().strip('"')=="titel":
            if len(value)==1:
                self.send(self.recipes[0].get_title())
            else:
                self.send(self.recipes[int(value[-1].getString())].get_title())

        #kompletten Einkaufszettel schreiben
        elif value[0].getString().strip('"')=="einkaufszettel":
            if len(value)==1:
                self.send(self.recipes[0].einkaufszettel("all"))
            else:
                self.send(self.recipes[int(value[-1].getString())].einkaufszettel())

        #einzelne Zutat auf Einkaufszettel
        elif value[0].getString().strip('"')=="Zettel":
            self.recipes[0].einkaufszettel(value[1].getString().strip('"'))

        #gibt Antwort zurück, ob eine Zutat gebraucht wird
        elif value[0].getString().strip('"')=="exists_zutat":
            #if len(value)==1:
            
            self.send(self.recipes[0].contains(value[1].getString().strip('"')))
            #else:
             #   self.send(self.recipes[int(str(value[-1]))].einkaufszettel())

        #
        elif value[0].getString().strip('"')=="zutaten":
            self.send(self.recipes[0].get_zutat(value[1].getString().strip('"')))
        #gibt zurück, für wie viele Personen das Rezept gebraucht wird
        elif value[0].getString().strip('"')=="portionen":
            #if len(value)==1:
            if value[1].getString().strip('"')== "wert":
                self.send(str(self.recipes[0].get_portions()))
            #else:
                #self.send(self.recipes[int(str(value[-1]))].einkaufszettel())

        #fürs umrechnen nach Personen
        elif value[0].getString().strip('"') == "Personen":
            self.send(self.recipes[0].umrechnen(value[1].getString().strip('"'),u'Personen'))
        #fürs umrechnen nach Zutaten
        elif value[0].getString().strip('"')=="Zutaten":
            z = value[1].getString().strip('"')
            m = value[2].getString().strip('"')
            e = value[3].getString().strip('"')
            self.send(self.recipes[0].umrechnen([m,e],z))

        elif value[0].getString().strip('"') == "ende":
            self.recipes[0].schritt = 0

        elif len(value)==3:
            self.send(call(value[0].getString().strip('"'), value[1].getString().strip('"'), self.recipes[int(str(value[-1]))]))
        else:
            self.send(call(value[0].getString().strip('"'), value[1].getString().strip('"'), self.recipes[0]))
            
        print "output: " + "done"

    def getName(self):
        return "Jython demo client"

    def error(self, throwable):
        print "error"


    def gui(self):#returns URL in unicode
        frame = JFrame('URL eingeben',
                defaultCloseOperation = JFrame.EXIT_ON_CLOSE,
                size = (480,200),
                       )
        frame.setLayout(None)
        
        def testact(event):
            frame.setVisible(False)
            url = field.getText()
            recipe = Recipe(url)
            self.recipes=[recipe]
            self.send("continue")

         
        fieldlabel = JLabel()
        fieldlabel.setText("<html><font size=+1>Geben Sie die Internetadresse des Rezepts ein</font></html>")
        fieldlabel.setBounds(20,20,500,40)
        frame.add(fieldlabel)

        field = JTextField()
        field.setText("https://www.chefkoch.de/rezepte/...")
        field.setBounds(20,60,411,40)
        frame.add(field)
        
        button = JButton("Los!",actionPerformed=testact)
        button.setBounds(155,100,150,30)
        frame.add(button)
        
        frame.setVisible(True)


m = Main()
m.open(8880)


