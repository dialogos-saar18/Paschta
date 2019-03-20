# -*- coding:cp1252 -*-

# HTML Parser
from bs4 import BeautifulSoup as bs
# eigene Klasse
from einheiten_transf import *

import re

#HTTP
from array import zeros
from java.net import URL
from java.io import InputStreamReader
from java.lang import StringBuilder



class Recipe:
    
    def __init__(self, url):
        
        # Hilfsfunktion: Liest den kompletten Inhalt des gegebenen Readers
        # und speichert ihn in einem String ab.
        def read_all(reader):
            arrsize = 8*1024
            arr = zeros('c', arrsize)
            buffer = StringBuilder()
            numCharsRead = 0

            while numCharsRead != -1:
                numCharsRead = reader.read(arr, 0, arrsize)
                if numCharsRead != -1:
                    buffer.append(arr, 0, numCharsRead);

            return buffer.toString()
        
        #Easter egg
        if url == "Ich bin Informatiker":
            self.title = u'Tiefk\xfchlpizza von bonita sopa'
            self.anleitung = [u'1. Backofen vorheizen: Auf Ober- und Unterhitze ca. 220 Grad, mit Hei\xdfluft ca. 200 Grad oder im Gasofen auf Stufe 5 bis 6. Wenn das L\xe4mpchen nicht mehr leuchtet, ist das Vorheizen beendet.', u'2. Die noch gefrorene Pizza aus dem Karton nehmen und die Folie entfernen.', u'3. Die Pizza auf den Rost legen. Wer weniger putzen mag, legt noch Backpapier dazwischen.', u'4. Die Pizza auf mittlerer Einschubleiste 10 bis 12 Minuten backen.', u'5. Sobald der K\xe4se geschmolzen ist, kann man die Pizza genie\xdfen.', u'6. Am besten schmeckt dazu eine Club Mate.']
            self.schritt = 0
            self.zutaten = {u'Tiefk\xfchlpizza': {u'menge': 1, u'einheit': u''}, u'eventuell Backpapier': {u'menge': 1, u'einheit': u'Bogen'}}
            self.portionen = 1
            self.eigenschaften = {u'Kalorien p. P.': u'ca. 874 kcal', u'Portionen': 1, u'Schwierigkeitsgrad': u'fordernd', u'Gesamtzeit': 'ca. 20 Min.', u'Arbeitszeit': u'ca. 10 Min.', u'Koch-/Backzeit': '12 Min.', u'Titel': u'Tiefk\xfchlpizza von bonita sopa'}

        else:
            # Quelltext holen
            url = URL(url)
            urlCon = url.openConnection()
            reader = InputStreamReader(urlCon.getInputStream(), "UTF-8")
            html = read_all(reader)
            reader.close()

            # Quelltext parsen
            soup = bs(html,features="html.parser")

            # Objektattribute initialisieren
            self.title = self.init_titel(soup) # String
            self.anleitung = self.init_anleitung(soup) # String list
            self.schritt = 0
            self.zutaten = self.init_zutaten(soup) # dict dict
            #self.zutatenliste = None
            self.portionen = self.init_portionen(soup)# int
            self.eigenschaften = self.init_properties(soup) # dict
        
    #returns string
    def get_schritt(self, argument): 
        
        if argument == u'first':
            return u'Lass uns loslegen: ' + self.anleitung[0]
        
        elif argument == u'next':
            try:
                self.schritt += 1
                antwort = u'Dein nächster Schritt lautet: ' + self.anleitung[self.schritt]
                if self.schritt == len(self.anleitung)-1:
                    antwort = antwort + u' Das war dein letzter Schritt'
                return antwort
            except:
                return u'Du bist fertig'
            
        elif argument == u'repeat':
            return u'Ich wiederhole: ' + self.anleitung[self.schritt]
        
        elif argument == u'previous':
            try:
                self.schritt -= 1
                return u'Der vorherige Schritt war: ' + self.anleitung[self.schritt]
            except:
                self.schritt = 0
                return u'Dein erster Schritt lautet: ' + self.anleitung[0]
            
        elif argument == u'last':
            self.schritt = len(self.anleitung - 1)
            return u'Der letzte Schritt lautet: ' + self.anleitung[self.schritt] + u' Das war der letzte Schritt'
        
        elif argument == u'all':
            r = u''
            for i in range(len(self.anleitung)):
                r += self.anleitung[i] + u'  '
            return r
        
        else:
            print (u'Unerwartetes Argument '+str(argument)+u' in get_schritt')
            return ("Fehler")
            
        
    #option: entweder "all" oder Text, der auf die Einkaufsliste soll
    def einkaufszettel(self,option):
        datei = "Einkaufszettel_" + self.title + ".txt"
        if option == "all":
            with open(datei, "w") as f:
                for z in self.zutaten:
                    m = self.zutaten[z][u'menge']
                    if m == 0:
                        m = u''
                    else:
                        m = str(m)
                    e = self.zutaten[z][u'einheit']
                    s = m + u' ' + e
                    f.write(s.encode('cp1252'))
                    f.write("\t")
                    f.write(z.encode('cp1252'))
                    f.write("\n")
        else:
            with open(datei, "a") as f:
                zutat = option
                f.write(zutat.encode('cp1252'))
                f.write("\n")

    # wie viel man von was braucht
    # Rückgabe für einzelne Zutaten: String
    # Rückgabe für Argument "all": Liste
    def get_zutat(self,bezeichnung): 
        if bezeichnung == "all":
            liste = []
            for z in self.zutaten:
                m = self.zutaten[z][u'menge']
                if m == 0:
                    m = u''
                else:
                    m = str(m)
                e = self.zutaten[z][u'einheit']
                #s = s + u' ' + m + u' ' + e + u' ' + z + u' '
                s = u' ' + m + u' ' + e + u' ' + z + u' '
                liste.append(s)
            return liste

        else:
            try:
                #überprüfen, ob Zutat vorkommt
                me = self.zutaten[bezeichnung][u'menge']
                if me == 0:
                    me = u''
                else:
                    me = str(me)
                ei = self.zutaten[bezeichnung][u'einheit']
                return me + u' ' + ei + u' ' + bezeichnung
            except:
                l = []
                for i in self.zutaten:
                    # überprüfen, Teilstring der Zutat in der Zutatenliste vorkommt
                    if re.search(bezeichnung, i):
                        me = self.zutaten[i][u'menge']
                        ei = self.zutaten[i][u'einheit']
                        l.append(me)
                        l.append(ei)
                        l.append(i)
                try:
                    if l[0] == 0:
                        l0 = u''
                    else:
                        l0 = str(l[0])
                    s = l0 + u' ' + l[1] + u' ' + l[2]
                    i = 3
                    # wenn mehrere Treffer gefunden worden (z.B. brauner Zucker und weißer Zucker)
                    while i < len(l):
                        if i%3 == 0:
                            s = s + u' und'
                        if l[i] == 0:
                            li = u''
                        else:
                            li = str(l[i])
                        s = s + u' ' + li
                        i = i + 1
                    return s
                        
                except:
                    #l ist leer -> keine Zutat gefunden
                    return u'Zutat wird nicht benötigt'

    #returns string
    def get_property(self,key):
        #key error / übersicht über die einzelnen Zeiten / Kalorien / Schwierigkeitsgrad
        try:        
            return self.eigenschaften[key]
        except:
            return "Im Rezept gibt es keine Angaben zu " + key

    def get_title(self):
        return self.title

    # Angabe, für wie viele Portionen das Rezept kalkuliert ist
    def get_portions(self):
        return self.portionen

    # Liste aller Zutaten (ohne Mengenangaben)
    def ingredients(self):
        return self.zutaten.keys()

    # alle Einheitenbezeichnungen, die im Rezept verwendet werden
    def einheiten(self):
        einheiten = set()
        for z in self.zutaten:
            e = self.zutaten[z][u'einheit']
            if e != u'':
                einheiten.add(e)
        einheiten = list(einheiten)
        return einheiten


    # return value: String, ob die Umrechnung erfolgreich war
    # angabe: "Personen" oder eine Zutat
    # anzahl: liste: [menge, einheit] zum umrechnen oder die Anzahl der Portionen
    def umrechnen(self, anzahl, angabe):
        # umrechnen nach Personen
        if angabe == u'Personen':
            anzahl = float(anzahl)
            factor = anzahl / self.get_property(u'Portionen')
            self.eigenschaften[u'Portionen'] = anzahl
        # umrechnen nach Zutat ohne Einheit 
        elif anzahl[1] == "0":
            menge_alt = self.zutaten[angabe][u'menge']
            zahl = anzahl[0]
            zahl = zahl.replace("komma", ".")
            factor = float(zahl) / menge_alt
        # umrechnen nach Zutat mit Menge und Einheit
        else:
            zahl = anzahl[0]
            zahl = zahl.replace("komma", ".")
            zahl = float(zahl)
            einheit_alt = self.zutaten[angabe][u'einheit']
            einheit_neu = anzahl[1]
            menge_alteeinheit = self.zutaten[angabe][u'menge']
            # e_umrechnen aus einheiten_transf.py
            menge_neueeinheit = e_umrechnen(einheit_alt, einheit_neu, menge_alteeinheit)
            if type(menge_neueeinheit) == str:
                s = u'Die Umrechnung ist fehlgeschlagen. Einheit ' + einheit_alt + u' lässt sich nicht in ' + einheit_neu + u' umrechnen'
                return s
            factor = zahl / menge_neueeinheit
        for z in self.zutaten:
            d = self.zutaten[z]
            d[u'menge'] = round(d[u'menge'] * factor, 2)
            self.eigenschaften[u'Portionen'] = self.get_property(u'Portionen') * factor
        return "Die Mengenangaben wurden umgerechnet"

    # gibt zurück ob die Zutat gebraucht wird oder nicht
    # Problem: mehrere Sorten der gleichen Zutat
    def contains(self, zutat):
        zutat = zutat.lower()
        if zutat in self.zutaten.keys():
            return u'Ja, du brauchst ' + zutat
        else:
            for i in self.zutaten.keys():
                if re.search(zutat, i):
                    return u'Du brauchst ' + i
            return u'Nein, ' + zutat + u' brauchst du nicht'



 # Funktionen zum Initialisieren der Attribute eines Recipe Objekts
 # (Aulesen der Informationen aus dem Quelltext des gewünschten Rezepts)

    def init_titel(self, beautifuls):
        t = beautifuls.find(u'title')
        t = t.contents[0]
        return t[:-14]

    # returns liste: [u'Die Zwiebeln fein...', u'Das Tomatenmark...',...]
    def init_anleitung(self, beautifuls):
        schritte = []
        zubereitung = beautifuls.find(id=u'rezept-zubereitung')
        i = 1
        for string in zubereitung.stripped_strings:
            string = str(i) + u'. ' + string
            schritte.append(string)
            i = i+ 1
        return schritte

    # return dict: {u'Zwiebel(n)': {u'menge': 1, u'einheit': u'm.-gro\xdfe'}, u'Zucker':...}
    # liest Zutaten + Mengenangaben + Einheiten aus Quelltext aus
    def init_zutaten(self, beautifuls):
        zutaten = {}
        # springt zur Zutatenauflistung im Quelltext
        incr = beautifuls.find(u'table', {u'class': u'incredients'})
        stripped2 = incr.stripped_strings
        strings = incr.strings
        l = []
        angaben_m = []
        angaben_z = []
        for i in incr.contents:
            if str(type(i)) == "<class 'bs4.element.NavigableString'>":
                pass
            else:
                # liest Zutatennamen und Mengenangaben aus Quelltext aus und formatiert sie
                li = i.findAll(u'td')
                menge = li[0].contents
                mengen_angabe= menge[0]
                mengen_angabe = mengen_angabe.strip()
                mengen_angabe = mengen_angabe.replace(u'\xa0', u' ')
                mengen_angabe = mengen_angabe.strip()
                angaben_m.append(mengen_angabe)
                    
                zutat = li[1].contents
                if len(zutat) == 1:
                    zutat_angabe = zutat[0]
                else:
                    zutat_angabe = zutat[1].contents[0]
                angaben_z.append(zutat_angabe.strip().lower())
        i = 0
        while i < len(angaben_m):
            # Zeichen, die in Grammatik Probleme verursachen ersetzen
            m = angaben_m[i]
            z = angaben_z[i]
            z = z.replace(u'(', u'')
            z = z.replace(u')', u'')
            z = z.replace(u'/', u'')
            z = z.replace(u',', u'')
            z = z.replace(u'.', u'')
            te = [m]
            d = {}
            # wenn weder Mengenangabe noch Einheit (z.B. Salz und Pfeffer)
            if m == u'':
                d[u'menge'] = 0
                d[u'einheit'] = u''
            else:
                spl = m.split()
                zahl = spl[0]
                if len(spl) == 2:
                    einheit = m.split()[1]
                else:
                    einheit = u''
                # e_ausschreiben aus einheiten_transf.py
                einheit = e_ausschreiben(einheit)
                einheit = einheit.replace(u'/', u'')
                einheit = einheit.replace(u'.', u'')
                try:
                    d[u'menge'] = int(zahl)
                    d[u'einheit'] = einheit
                # wenn Mengenangabe, aber keine Einheit (z.B. 1 Zwiebel)
                except:
                    d[u'menge'] = 0
                    d[u'einheit'] = zahl
            zutaten[z] = d
            i = i+1
        return zutaten

    # returns int
    # liest Anzahl der Portionen aus Quelltext aus
    def init_portionen(self, beautifuls):
        p = beautifuls.find(u'input', {u'name': u'portionen'})
        p = p[u'value']
        return int(p)

    #returns dict: {u'schwierigkeitsgrad': u'simpel', ...}
    # liest Informationen über Zeiten, Kalorien und Schwierigkeitsgrad aus Quelltext aus
    def init_properties(self, beautifuls):
        preparation = {}
        prep = beautifuls.find(id=u'preparation-info')
        l = []
        # generator object
        stripped = prep.stripped_strings
        i = 0
        # iterieren über Informationen
        for s in stripped:
            # Arbeitszeit, Schwierigkeitsgrad etc.
            if i % 2 == 0:
                key = s
                key = s.replace(u':', u'')
            # Werte 
            else:
                val = u''
                for n in s:
                    if n == u'/':
                        break
                    else:
                        val = val + n
                val = val.strip()
                if key == u'Arbeitszeit' or key == u'Ruhezeit' or key == u'Koch-/Backzeit':
                    val = val[4:]
                    lis = val.split(" ")
                    if len(lis) == 4:
                        k = int(lis[0]) * 24 + int(lis[2])
                        v = lis[3]
                    else:
                        k = int(lis[0])
                        v = lis[1]
                    val = u'ca. ' + str(k) + u' ' + v

                                    
                preparation[key] = val

            i = i + 1

        # Liste aller vorkommenden Zeiteinheiten erstellen
        ges = 0
        einheiten = []
        try:
            aze = preparation[u'Arbeitszeit'][u'einheit']
            einheiten.append(aze)
        except:
            pass
        try:
            rze = preparation[u'Ruhezeit'][u'einheit']
            einheiten.append(rze)
        except:
            pass
        try:
            kze = preparation[u'Koch-/Backzeit'][u'einheit']
            einheiten.append(kze)
        except:
            pass
        umr = False

        # wenn nicht alle Einheiten in Minuten sind, alles einheitlich umrechnen
        # notwendig, um Gesamtzeit (ges) auszurechnen
        for e in einheiten:
            if e != u'Min.':
                umr = True
        if u'Arbeitszeit' in preparation:
            zeit = preparation[u'Arbeitszeit'][4:].split(" ")[0]
            zeit = int(zeit)
            if umr:
                if aze == u'Std.':
                    zeit = zeit * 60
            ges = ges + zeit
        if u'Ruhezeit' in preparation:
            zeit = preparation[u'Ruhezeit'][4:].split(" ")[0]
            zeit = int(zeit)
            if umr:
                if rze == u'Std.':
                    zeit = zeit * 60
            ges = ges + zeit
        if u'Koch-/Backzeit' in preparation:
            zeit = preparation[u'Koch-/Backzeit'][4:].split(" ")[0]
            zeit = int(zeit)
            if umr:
                if kze == u'Std.':
                    zeit = zeit * 60
            ges = ges + zeit  

        e = u'Min.'
        # wenn Gesamtzeit in Minuten zu groß, dann in Stunden umrechnen
        if ges > 300:
            ges = float(ges) / 60
            e = u'Std.'

        # Gesamtzeit, Titel und Portionen zu eigenschaften dict hinzufügen
        preparation[u'Gesamtzeit'] = u'ca. ' + str(ges) + u' ' + e
        ti = self.init_titel(beautifuls)
        pi = self.init_portionen(beautifuls)
        preparation[u'Titel'] = ti
        preparation[u'Portionen'] = pi
        return preparation




                                             
