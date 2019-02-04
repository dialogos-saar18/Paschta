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

# ausschreiben abgekürzter Einheiten, da zum Erstellen der Grammatik benötigt
def e_ausschreiben(einheit):
    if einheit == u'EL, gestr.':
        e = u'EL, gestrichen'
    elif einheit == u'EL, gehäuft':
        e = u'Esslöffel, gehäuft'
    elif einheit == u'EL':
        e = u'Esslöffel'
    elif einheit == u'TL, gestr.':
        e = u'TL, gestrichen'
    elif einheit == u'gr. Dose/n':
        e = u'große Dose/n'
    elif einheit == u'gr. Flasche(n)':
        e = u'große Flasche(n)'
    elif einheit == u'gr. Gläser':
        e = u'große Gläser'
    elif einheit == u'gr. Glas':
        e = u'großes Glas'
    elif einheit == u'gr. Kopf':
        e = u'großer Kopf'
    elif einheit == u'gr. Scheiben':
        e = u'große Scheiben'
    elif einheit == u'm.-große':
        e = u'mittelgroße'
    elif einheit == u'm.-großer':
        e = u'mittelgroßer'
    elif einheit == u'm.-großes':
        e = u'mittelgroßes'
    elif einheit == u'Msp.':
        e = u'Messerspitze'
    elif einheit == u'n. B.':
        e = u'nach Belieben'
    elif einheit == u'Pck.':
        e = u'Päckchen'
    elif einheit == u'Pkt.':
        e = u'Päckchen'
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

    
