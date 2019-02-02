## Paschta

Paschta ist ein interaktiver Dialog, der dem Benutzer das Kochen erleichtern soll. Dazu wählt man einfach ein Rezept auf ```Chefkoch.de```. Dann kann man alle Informationen aus dem Rezept ganz leicht per Sprachbefehl erlangen, ohne dass man mit schmutzigen Koch-Fingern auf Displays herumwischen muss.

### DialogOs installieren
- Voraussetzung Java und JRE; Download beispielsweise <a href="https://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html">hier</a>.
<br>Falls nicht die aktuelle Java-Version installiert ist, muss Java möglicherweise neu installiert werden. Ein Update ist scheinbar nicht genug.
- <a href= "https://www.dialogos.app/de/index.html">Hier</a> kann man DialogOS herunterladen.
- Bei „Select Components“ alles anwählen.

### Den Client starten
- Der _Paschta_-Ordner muss sich in einem Unterverzeichnis von C:\ befinden.
- In der Kommandozeile in den Ordner navigieren (dafür auf Windows cmd.exe verwenden oder in der PowerShell zuerst ```cmd``` eingeben).
- ```gradlew runClient``` eingeben und die ```Enter```-Taste drücken.
- Warten, bis ```new state: CONNECTING```angezeigt wird.

### Navigation auf der Kommandozeile
-	cmd.exe (einfach in die Suche eingeben)
- Jede Befehlszeile beginnt mit dem Pfad zu dem Ordner, in dem man sich gerade befindet. Dahinter kann man einen Befehl eintippen und mit der Entertaste bestätigen.
-	Mit ```dir``` kann man sich den Inhalt des aktuellen Ordners anzeigen lassen.
-	Mit ```cd```, dann _Leerzeichen_ und _Ordnername_ kannst du in einen Unterordner wechseln.
-	Mit ```cd```, dann _Leerzeichen_ und einem Pfad kann man direkt in den gewünschten Ordner wechseln.
-	Mit ```cd..``` kann man eine Ordnerebene höher wechseln.

Beispiel:<br>
![kommandozeile](https://user-images.githubusercontent.com/36304889/52163374-64abf980-26e1-11e9-9c77-4f097fdb6837.JPG)

### Den Dialog starten
- Den Dialog im Ordner ```Dialoge``` auswählen und mit Doppelklick öffnen. (Wir empfehlen ```kochbuch_ohne_liste.dos```, da ```kochbuch_mit_liste.dos``` momentan nur im _Stillen Modus_ von DialogOS funktioniert.)
<br>Alternativ kann man zunächst DialogOS starten und dann im Programm den Dialog öffnen.
- Im oberen Bereich des Fensters auf ```Ausführen``` klicken, um den Dialog zu starten.<br>
![ausfuhren](https://user-images.githubusercontent.com/36304889/52163474-cde03c80-26e2-11e9-8038-39111c5a537e.JPG)
- Wir empfehlen, ein Blootooth-Headset zu benutzten, um den Dialog optimal zu benutzen.
- In ```kochbuch_mit_liste.dos```muss im Scriptknoten (hellblau, markiert mit einer roten Notiz) _"Zutatenliste einlesen"_ der Dateipfad für die Datein ```Zutatenliste.txt``` in der ersten Zeile ausgebessert werden. Dabei müssen Slashes (```/```), keine Backslashes (```\```) verwendet werden!

### Feedback geben
-	Probleme, Wünsche, Anregungen, Fragen! Es soll Spaß machen, mit dem Dialog zu kochen. Es soll einfach und intuitiv sein.
-	Sei gnadenlos! Je mehr Input wir bekommen, desto mehr Potential hat das Gesamtergebnis.
