# Konvertierung von Zusi-2-Strecken nach Zusi 3
Dieses Programm dient dazu, Zusi2-Strecken nach Zusi3 zu konvertieren.
Dazu passt man in der Datei strecken.xml die Pfade an die eigene Installation an, wobei die eingestellten Pfade für eine Standard-Installation stimmen sollten. Zudem entfernt an den gewünschten Strecken und Fahrpläne die Kommentarzeichen. Danach startet man zusi2to3.py, wobei man mindestens Python 3.9 benötigt.

Dies ist ein unfertiges Projekt mit vielen Einschränkungen, von denen sich manche eventuell niemals beheben lassen.

Folgende Einschränkungen liegen an der Zusi2-Datenbasis und sind nicht behebbar:
- Die Grafik ist im Vergleich zu den Zusi3-Projekten sehr einfach. In manchen Strecken sind nur die Bahnanlagen dargestellt und keinerlei Landschaft.

Folgende Einschränkungen lassen sich möglicherweise noch beheben:
- Zusi2 hat einen großen Fahrzeugpark, der mit den Dateien tfz.xml und wagen.xml auf Zusi3 abgebildet werden soll. Dies ist bisher nur für die Triebfahrzeuge des 1978er Fahrplans der linken Rheinstrecke geschehen. Bei Triebfahrzeugen, für die noch keine Übersetzung angelegt wurde, werden die BR120 und die BR218 als Ersatz genommen. Bei Wagen werden dann die Zusi2-Modelle konvertiert. Für manche Zusi-Fahrzeuge gibt es auch kein Modell in Zusi3.
- Die Kurvenschienen sind Vielecke, denen der Zug in Zusi3 exakt folgt, was zu einer sehr unruhigen Kurvenfahrt führen kann.
- Die Farben der Landschaft werden von Zusi3 leicht anders dargestellt.
- Die Kombinationssignale flackern teilweise sinnlos.
- Die PZB geht nur sehr vereinzelt. LZB und GNT sind noch gar nicht implementiert.
- Teilweise klappt die Weiterschaltung der Signale nicht, so dass die Züge stehen bleiben. Ein Zeitsprung führt sicher in diesen Zustand.
- Die ortsfesten Zp9-Signale leuchten dauernd.
- Teilweise laufen die Koordinaten der dargestellten Landschaft und der flexibelen Elemente darin, wie Züge und Signale, auseinander. Dadurch schweben Züge manchmal gut sichtbar über dem Gleis oder fahren leicht daneben. Indusi-Magnete liegen schon mal nicht an der richtigen Stelle.
- Die Fahrplandarstellung zeigt noch keine Sbk-Signale und keine Ende-Zeichen des anschließenden Weichenbereichs. Auch die Darstellung des verkürzten Vorsignalabstands und der Signalgeschwindigkeiten sind noch nicht korrekt.
- Züge mit Zugwende werden nur bis zur Zugwende konvertiert.
- Es lassen sich nur Strecken mit der Datei-Version 2.3 konvertieren.
- Es wurden nur die Strecken "Linke Rheinstrecke" und "Eifel" getestet.
