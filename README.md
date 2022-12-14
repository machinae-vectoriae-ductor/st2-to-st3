# Konvertierung von Zusi 2-Strecken nach Zusi 3
Dieses Programm dient dazu, Zusi 2-Strecken nach Zusi 3 zu konvertieren.
Dazu passt man in der Datei strecken.xml die Pfade an die eigene Installation an, wobei die eingestellten Pfade für eine Standard-Installation stimmen sollten. Zudem entfernt man an den gewünschten Strecken und Fahrplänen die Kommentarzeichen. Danach startet man zusi2to3.py, wobei man mindestens Python 3.9 benötigt.

Dies ist ein unfertiges Projekt mit vielen Einschränkungen, von denen sich manche eventuell niemals beheben lassen.

Folgende Einschränkungen liegen an der Zusi 2-Datenbasis und sind nicht behebbar:
- Die Grafik ist im Vergleich zu den Zusi 3-Projekten sehr einfach. In manchen Strecken sind nur die Bahnanlagen dargestellt und keinerlei Landschaft.

Folgende Einschränkungen lassen sich möglicherweise noch beheben:
- Zusi 2 hat einen großen Fahrzeugpark, der mit den Dateien tfz.xml und wagen.xml auf Zusi3 abgebildet werden soll. Dies ist bisher nur teilweise für die Triebfahrzeuge des 1978er Fahrplans der linken Rheinstrecke geschehen. Wenn das führende Fahrzeug nicht in der Übersetzungstabelle eingetragen ist, wird der Zug nicht in den Fahrplan aufgenommen. Bei Wagen ohne Übersetzung werden die Zusi 2-Modelle konvertiert. Für manche Zusi 2-Fahrzeuge gibt es auch kein Modell in Zusi 3.
- Falls in Zusi 3 die Meldung erscheint, dass ein Zug zu lang zum Aufgleisen ist, sollte der Zug per entsprechendem Eintrag in die strecekn.xml aus der Fahrplandatei gelöscht werden, da Zusi 3 beim Aufgleisversuch abzustürzen scheint.
- Die Kurvenschienen sind Vielecke, denen der Zug in Zusi 3 exakt folgt, was zu einer sehr unruhigen Kurvenfahrt führen kann. Hier muss noch die Krümmung der Streckenelemnte bestimmt und eingetragen werden.
- Die Farben der Landschaft werden von Zusi 3 leicht anders dargestellt.
- LZB und GNT sind noch nicht implementiert.
- Teilweise klappt die Weiterschaltung der Signale nicht, so dass die Züge stehen bleiben.
- Die ortsfesten Zp9-Signale werden nicht mit übernommen, da Zusi 3 damit (noch) nichts anfangen kann.
- Teilweise laufen die Koordinaten der dargestellten Landschaft und der flexiblen Elemente darin, wie Züge und Signale, auseinander. Dadurch schweben Züge manchmal gut sichtbar über dem Gleis oder fahren leicht daneben. Indusi-Magnete liegen schon mal nicht an der richtigen Stelle.
- Die Fahrplandarstellung zeigt noch keine Ende-Zeichen des anschließenden Weichenbereichs.
- Züge mit Zugwende werden nur bis zur Zugwende konvertiert.
- Es lassen sich nur Strecken mit der Datei-Version 2.3 konvertieren.
- Bahnübergänge und Gleissperrsignale werden nicht bedient.
- Es wurden nur die Strecken "Linke Rheinstrecke" und "Eifel" getestet.
