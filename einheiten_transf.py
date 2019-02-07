# -*- coding: cp1252 -*-
# umrechnen z.B. von Gramm auf Kilogramm etc.
def e_umrechnen(einheit_alt, einheit_neu, menge):
    if einheit_alt == einheit_neu:
        m = menge
    elif einheit_alt == u'Gramm' and einheit_neu == u'Kilogramm':
        m = menge/1000.0
    elif einheit_alt == u'Gramm' and einheit_neu == u'Milligramm':
        m = menge * 1000.0
    elif einheit_alt == u'Kilogramm' and einheit_neu == u'Gramm':
        m = menge * 1000.0
    elif einheit_alt == u'Kilogramm' and einheit_neu == u'Milligramm':
        m = menge * 1000.0 * 1000.0
    elif einheit_alt == u'Milligramm' and einheit_neu == u'Gramm':
        m = menge / 1000.0
    elif einheit_alt == u'Milligramm' and einheit_neu == u'Kilogramm':
        m = menge / 1000.0 / 1000.0
    elif einheit_alt == u'Liter' and einheit_neu == u'Milliliter':
        m = menge * 1000.0
    elif einheit_alt == u'Liter' and einheit_neu == u'Zentiliter':
        m = menge * 100.0
    elif einheit_alt == u'Liter' and einheit_neu == u'Deziliter':
        m = menge * 10.0
    elif einheit_alt == u'Milliliter' and einheit_neu == u'Liter':
        m = menge / 1000.0
    elif einheit_alt == u'Milliliter' and einheit_neu == u'Zentiliter':
        m = menge / 10.0
    elif einheit_alt == u'Milliliter' and einheit_neu == u'Deziliter':
        m = menge / 100.0
    elif einheit_alt == u'Zentiliter' and einheit_neu == u'Liter':
        m = menge / 100.0
    elif einheit_alt == u'Zentiliter' and einheit_neu == u'Deziliter':
        m = menge / 10.0
    elif einheit_alt == u'Zentiliter' and einheit_neu == u'Milliliter':
        m = menge * 10.0
    elif einheit_alt == u'Deziliter' and einheit_neu == u'Liter':
        m = menge / 10.0
    elif einheit_alt == u'Deziliter' and einheit_neu == u'Zentiliter':
        m = menge * 10.0
    elif einheit_alt == u'Deziliter' and einheit_neu == u'Milliliter':
        m = menge * 100.0
    else:
        m = ""
    return m    

# ausschreiben abgek�rzter Einheiten, da zum Erstellen der Grammatik ben�tigt
def e_ausschreiben(einheit):
    if einheit == u'EL, gestr.':
        e = u'EL, gestrichen'
    elif einheit == u'EL, geh�uft':
        e = u'Essl�ffel, geh�uft'
    elif einheit == u'EL':
        e = u'Essl�ffel'
    elif einheit == u'TL, gestr.':
        e = u'TL, gestrichen'
    elif einheit == u'gr. Dose/n':
        e = u'gro�e Dose/n'
    elif einheit == u'gr. Flasche(n)':
        e = u'gro�e Flasche(n)'
    elif einheit == u'gr. Gl�ser':
        e = u'gro�e Gl�ser'
    elif einheit == u'gr. Glas':
        e = u'gro�es Glas'
    elif einheit == u'gr. Kopf':
        e = u'gro�er Kopf'
    elif einheit == u'gr. Scheiben':
        e = u'gro�e Scheiben'
    elif einheit == u'm.-gro�e':
        e = u'mittelgro�e'
    elif einheit == u'm.-gro�er':
        e = u'mittelgro�er'
    elif einheit == u'm.-gro�es':
        e = u'mittelgro�es'
    elif einheit == u'Msp.':
        e = u'Messerspitze'
    elif einheit == u'n. B.':
        e = u'nach Belieben'
    elif einheit == u'Pck.':
        e = u'P�ckchen'
    elif einheit == u'Pkt.':
        e = u'P�ckchen'
    elif einheit == u'cl':
        e = u'Zentiliter'
    elif einheit == u'cm':
        e = u'Zentimeter'
    elif einheit == u'dl':
        e = u'Deziliter'
    elif einheit == u'g':
        e = u'Gramm'
    elif einheit == u'kg':
        e = u'Kilogramm'
    elif einheit == u'mg':
        e = u'Milligramm'
    elif einheit == u'ml':
        e = u'Milliliter'
    elif einheit == u'Port.':
        e = u'Portion'
    else:
        e = einheit
    return e

    
