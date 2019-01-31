# -*- coding:cp1252 -*-
from bs4 import BeautifulSoup as bs
from einheiten_transf import *
import urllib2
import re

class Recipe:
    
    def __init__(self, url):
        # Liest den kompletten Inhalt des gegebenen Readers
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


        url = URL(url)
        urlCon = url.openConnection()
        reader = InputStreamReader(urlCon.getInputStream())

        html = read_all(reader)

        reader.close()

        soup = bs(html,features="html.parser")
        
        self.title = self.init_titel(soup)
        self.anleitung = self.init_anleitung(soup)
        self.schritt = 0
        self.zutaten = self.init_zutaten(soup)
        self.zutatenliste = None
        self.portionen = self.init_portionen(soup)#int
        #eigenschaften: dict; available keys:
        #zubereitungszeit ebenfalls evtl. in Größe und Einheit unterteilen
            #-> an den jeweiligen Nutzer anpassen
        self.eigenschaften = self.init_properties(soup)

    def get_schritt(self, argument): #returns string
        
        if argument == u'first':
            return u'Lass uns loslegen: ' + self.anleitung[self.schritt]
        elif argument == u'next':
            try:
                self.schritt += 1
                return u'Dein nächster Schritt lautet: ' + self.anleitung[self.schritt]
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
            return u'Der letzte Schritt lautet: ' + self.anleitung[self.schritt]
        elif argument == u'all':
            r = u''
            for i in range(len(self.anleitung)):
                r += str(i+1) + u'. ' + self.anleitung[i] + u'  '
            return r
        else:
            print (u'Unerwartetes Argument '+str(argument)+u' in get_schritt')
            ###raise Error


    #option: entweder "all" oder die der Index der Zutat, die aufgeschrieben werden soll
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
                #o = int(option)
                zutat = option
                f.write(zutat.encode('cp1252'))
                f.write("\n")


    def get_zutat(self,bezeichnung): #returns string
        if bezeichnung == "all":
            liste = []
            s = u'Du brauchst '
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
            #return s
            
        try:
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
                while i < len(l):
                    print(i)
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
                return u'Zutat wird nicht benötigt'

    def get_property(self,key): #returns string
        #key error / "all"=> gesamtzeit / übersicht über die einzelnen Zeiten
        try:        
            return self.eigenschaften[key]
        except:
            return "Im Rezept gibt es keine Angaben zu " + key

    def get_title(self):
        return self.title

    def get_portions(self):
        return self.portionen

    def ingredients(self):
        return self.zutaten.keys()

    def einheiten(self):
        einheiten = set()
        for z in self.zutaten:
            e = self.zutaten[z][u'einheit']
            if e != u'':
                einheiten.add(e)
        einheiten = list(einheiten)
        return einheiten


    # no return value, only changes incredients
    # angabe: "Personen" oder eine Zutat
    # anzahl: liste: [menge, einheit] zum umrechnen oder die Anzahl der Portionen
    # to do: argumente anpassen an client, evtl menge in int umrechnen
    def umrechnen(self, anzahl, angabe):
        if angabe == u'Personen':
            anzahl = float(anzahl)
            factor = anzahl / self.get_property(u'Portionen')
            self.eigenschaften[u'Portionen'] = anzahl
        elif anzahl[1] == "0":
            menge_alt = self.zutaten[angabe][u'menge']
            zahl = anzahl[0]
            zahl = zahl.replace("komma", ".")
            factor = float(zahl) / menge_alt
        else:
            zahl = anzahl[0]
            zahl = zahl.replace("komma", ".")
            zahl = float(zahl)
            einheit_alt = self.zutaten[angabe][u'einheit']
            einheit_neu = anzahl[1]
            menge_alteeinheit = self.zutaten[angabe][u'menge']
            #print(einheit_alt, einheit_neu, menge_alteeinheit)
            menge_neueeinheit = e_umrechnen(einheit_alt, einheit_neu, menge_alteeinheit)
            #print(menge_neueeinheit)
            factor = zahl / menge_neueeinheit
        for z in self.zutaten:
            d = self.zutaten[z]
            d[u'menge'] = round(d[u'menge'] * factor, 2)
            self.eigenschaften[u'Portionen'] = self.get_property(u'Portionen') * factor

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
    def init_zutaten(self, beautifuls):
        zutaten = {}
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
            m = angaben_m[i]
            z = angaben_z[i]
            z = z.replace(u'(', u'')
            z = z.replace(u')', u'')
            z = z.replace(u'/', u'')
            z = z.replace(u',', u'')
            z = z.replace(u'.', u'')
            te = [m]
            d = {}
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
                einheit = e_ausschreiben(einheit)
                try:
                    d[u'menge'] = int(zahl)
                    d[u'einheit'] = einheit
                except:
                    d[u'menge'] = 0
                    d[u'einheit'] = zahl
            zutaten[z] = d
            i = i+1
        return zutaten

    # returns int
    def init_portionen(self, beautifuls):
        p = beautifuls.find(u'input', {u'name': u'portionen'})
        p = p[u'value']
        return int(p)

    #returns dict: {u'schwierigkeitsgrad': u'simpel', ...}
    def init_properties(self, beautifuls):
        preparation = {}
        prep = beautifuls.find(id=u'preparation-info')
        l = []
        stripped = prep.stripped_strings
        i = 0
        for s in stripped:
            if i % 2 == 0:
                key = s
                key = s.replace(u':', u'')
            else:
                val = u''
                for n in s:
                    if n == u'/':
                        break
                    else:
                        val = val + n
                val = val.strip()
                if key == u'Arbeitszeit:' or key == u'Ruhezeit:' or key == u'Koch-/Backzeit:':
                    d = {}
                    val = val[4:]
                    lis = val.split(" ")
                    if len(lis) == 4:
                        k = int(lis[0]) * 24 + int(lis[2])
                        v = lis[3]
                    else:
                        k = int(lis[0])
                        v = lis[1]
                    d[u'dauer'] = k
                    d[u'einheit'] = v
                    val = d
                                    
                preparation[key] = val
            i = i + 1
        ges = 0
        einheiten = []
        try:
            aze = preparation[u'Arbeitszeit:'][u'einheit']
            einheiten.append(aze)
        except:
            pass
        try:
            rze = preparation[u'Ruhezeit:'][u'einheit']
            einheiten.append(rze)
        except:
            pass
        try:
            kze = preparation[u'Koch-/Backzeit:'][u'einheit']
            einheiten.append(kze)
        except:
            pass
        umr = False
        for e in einheiten:
            if e != u'Min.':
                umr = True
        if u'Arbeitszeit:' in preparation:
            zeit = preparation[u'Arbeitszeit:'][u'dauer']
            if umr:
                if aze == u'Std.':
                    zeit = zeit * 60
            ges = ges + zeit
        if u'Ruhezeit:' in preparation:
            zeit = preparation[u'Ruhezeit:'][u'dauer']
            if umr:
                if rze == u'Std.':
                    zeit = zeit * 60
            ges = ges + zeit
        if u'Koch-/Backzeit:' in preparation:
            zeit = preparation[u'Koch-/Backzeit:'][u'dauer']
            if umr:
                if kze == u'Std.':
                    zeit = zeit * 60
            ges = ges + zeit  
        di = {}
        e = u'Min.'
        if ges > 300:
            ges = float(ges) / 60
            e = u'Std.'
        di[u'dauer'] = ges
        di[u'einheit'] = e
        preparation[u'Gesamtzeit'] = di
        ti = self.init_titel(beautifuls)
        pi = self.init_portionen(beautifuls)
        preparation[u'Titel'] = ti
        preparation[u'Portionen'] = pi
        return preparation




                                             
#rezept = Recipe("https://www.chefkoch.de/rezepte/447611137007614/Paprika-Carbonara.html")
    

'''
class Nutzer:
    def __init__(self, name):
        load_user(name)
        self.handicap #wie viel länger oder kürzer braucht der nutzer (in Prozent)
'''
