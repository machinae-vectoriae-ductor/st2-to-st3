#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import shutil
import xml.etree.ElementTree as ET
from collections import namedtuple
from datetime import datetime

from . import common, landschaft
from .common import readfloat, readfloatstr, readposixtime

VerknParameter = namedtuple(
    "VerknParameter", ["dateiname_zusi", "x", "y", "z", "rx", "ry", "rz", "boundingr"]
)


def conv_wav(z2pfad, z2wav, z3pfad, zielverzeichnis_rel):
    z3wav = os.path.join(
        "RollingStock", zielverzeichnis_rel, os.path.relpath(z2wav, "loks")
    )
    os.makedirs(os.path.dirname(os.path.join(z3pfad, z3wav)), exist_ok=True)
    shutil.copy2(os.path.join(z2pfad, z2wav), os.path.join(z3pfad, z3wav))
    return z3wav


def conv_wagen(z2pfad, z2fahrzeugdateiname_rel, z3pfad, zielverzeichnis_rel):

    fahrzeugname = os.path.splitext(os.path.basename(z2fahrzeugdateiname_rel))[0]
    z2fahrzeugdateiname_abs = os.path.join(z2pfad, z2fahrzeugdateiname_rel)
    z3fahrzeugdateiname_rel = os.path.join(
        "RollingStock", zielverzeichnis_rel, fahrzeugname + ".rv.fzg"
    )
    z3fahrzeugdateiname_abs = os.path.join(z3pfad, z3fahrzeugdateiname_rel)
    # treefzg = ET.parse("fahrzeug.xml")
    # nwag_root = treewag.getroot()

    nfzg_root = ET.Element("Zusi")
    treefzg = ET.ElementTree(nfzg_root)
    nfzg_info = ET.SubElement(
        nfzg_root,
        "Info",
        {"DateiTyp": "Fahrzeug", "Version": "A.1", "MinVersion": "A.1"},
    )
    nfzg_fahrzeug = ET.SubElement(nfzg_root, "Fahrzeug")

    with open(z2fahrzeugdateiname_abs, "r", encoding="iso-8859-1") as ffzg:
        # print(
        #     f"{z2fahrzeugdateiname_abs} -> {z3fahrzeugdateiname_abs}", file=sys.stderr
        # )
        ffzg.readline()  # Zusi-Version
        ET.SubElement(nfzg_info, "AutorEintrag", {"AutorName": ffzg.readline().strip()})
        while not ffzg.readline().startswith("#"):
            pass
        nfzg_fzgvariante = ET.SubElement(
            nfzg_fahrzeug,
            "FahrzeugVariante",
            {
                "BR": fahrzeugname,
                "Beschreibung": "Zusi2-Wagen",
                "Farbgebung": "Zusi2",
                "IDHaupt": "1",
                "IDNeben": "1",
            },
        )
        ffzg.readline()  # Geschwindigkeitsmultiplikator ohne Funktion
        nfzg_Grunddaten = ET.SubElement(
            nfzg_fahrzeug, "FahrzeugGrunddaten", {"cwA": readfloatstr(ffzg)}
        )
        steuerventil = (
            ffzg.readline().strip()
        )  # Bauart des Steuerventils, zulässige Werte: Einloesig, Mehrloesig, Mehrloesig HBL-Anschluss
        if steuerventil == "Mehrloesig HBL-Anschluss":
            hblvorhanden = nfzg_Grunddaten.attrib["HBLVorhanden"] = "1"
        else:
            hblvorhanden = "0"
        bremsmassep = ffzg.readline().strip()  # Bremsmasse Stellung P in kg
        bremsmasseg = ffzg.readline().strip()  # Bremsmasse Stellung G in kg
        bremsmasser = ffzg.readline().strip()  # Bremsmasse Stellung R in kg
        bremsmassemg = ffzg.readline().strip()  # Bremsmasse Stellung Mg in kg
        ffzg.readline()  # reserviert für spätere Funktionen
        masse = readfloat(ffzg)
        nfzg_Grunddaten.attrib["Masse"] = str(masse)
        nfzg_Grunddaten.attrib["RotationsZuschlag"] = str(masse / 12.2)
        nfzg_Grunddaten.attrib["Rollwiderstand"] = str(masse * 0.0192)
        nfzg_Grunddaten.attrib["spMax"] = str(
            readfloat(ffzg) / 3.6
        )  # Höchstgeschwindigkeit in km/h
        rbehaeltervolumen = readfloatstr(ffzg)  # Volumen Hilfsluftbehälter in Liter
        scheibenbremse = (
            ffzg.readline().strip() == "0"
        )  # Bremsencharakteristik (1: Klotzbremse, 0: Scheibenbremse)
        if steuerventil == "Einloesig":
            nfzg_bremse = ET.SubElement(
                nfzg_fahrzeug,
                "BremseLuftEinlK1",
                {
                    "VolumenB": rbehaeltervolumen,
                    "VolumenZylinder": "10",
                    "FBremsuebersetzung": "12724.0",
                },
            )
            nfzg_bremskennlinie = ET.SubElement(nfzg_bremse, "BremsenKennungV")
            ET.SubElement(nfzg_bremskennlinie, "Pkt", {"PktY": "2.419"})
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "2.7236", "PktY": "1.939"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "2.7856", "PktY": "1.939"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "5.5092", "PktY": "1.529"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "5.5711", "PktY": "1.521"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "8.2947", "PktY": "1.319"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "11.1419", "PktY": "1.178"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "19.9939", "PktY": "0.913"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "22.2222", "PktY": "0.892"}
            )
            ET.SubElement(nfzg_bremskennlinie, "Stufe", {"StufenWert": "1"})
            ET.SubElement(nfzg_bremse, "BremseP", {"BremsGewicht": bremsmassep})
            ET.SubElement(nfzg_bremse, "BremseG", {"BremsGewicht": bremsmasseg})
        elif ("Mehrloesig" in steuerventil) and not scheibenbremse:
            nfzg_bremse = ET.SubElement(
                nfzg_fahrzeug,
                "Bremse_KE_GP",
                {
                    "VolumenR": rbehaeltervolumen,
                    "VolumenA": "10",
                    "VolumenZylinder": "10",
                    "FBremsuebersetzung": "12724.0",
                    "HBLAnschluss": hblvorhanden,
                },
            )
            nfzg_bremskennlinie = ET.SubElement(nfzg_bremse, "BremsenKennungV")
            ET.SubElement(nfzg_bremskennlinie, "Pkt", {"PktY": "2.419"})
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "2.7236", "PktY": "1.939"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "2.7856", "PktY": "1.939"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "5.5092", "PktY": "1.529"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "5.5711", "PktY": "1.521"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "8.2947", "PktY": "1.319"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "11.1419", "PktY": "1.178"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "19.9939", "PktY": "0.913"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "22.2222", "PktY": "0.892"}
            )
            ET.SubElement(nfzg_bremskennlinie, "Stufe", {"StufenWert": "1"})
            ET.SubElement(nfzg_bremse, "BremseP", {"BremsGewicht": bremsmassep})
            ET.SubElement(nfzg_bremse, "BremseG", {"BremsGewicht": bremsmasseg})
        else:
            nfzg_bremse = ET.SubElement(
                nfzg_fahrzeug,
                "Bremse_KE_GPR_Scheibe",
                {
                    "VolumenR": rbehaeltervolumen,
                    "VolumenA": "10",
                    "VolumenZylinder": "10",
                    "FBremsuebersetzung": "12724.0",
                    "HBLAnschluss": hblvorhanden,
                },
            )
            nfzg_bremskennlinie = ET.SubElement(nfzg_bremse, "BremsenKennungV")
            ET.SubElement(nfzg_bremskennlinie, "Pkt", {"PktY": "1.1"})
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "1.5475", "PktY": "1.072"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "2.6308", "PktY": "1.053"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "2.7856", "PktY": "1.05"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "5.4164", "PktY": "1.012"}
            )
            ET.SubElement(
                nfzg_bremskennlinie, "Pkt", {"PktX": "5.5711", "PktY": "1.01"}
            )
            ET.SubElement(nfzg_bremskennlinie, "Pkt", {"PktX": "10.9872", "PktY": "1"})
            ET.SubElement(nfzg_bremskennlinie, "Pkt", {"PktX": "11.1419", "PktY": "1"})
            ET.SubElement(nfzg_bremskennlinie, "Pkt", {"PktX": "55.5556", "PktY": "1"})
            ET.SubElement(nfzg_bremskennlinie, "Stufe", {"StufenWert": "1"})
            ET.SubElement(nfzg_bremse, "BremseP", {"BremsGewicht": bremsmassep})
            ET.SubElement(nfzg_bremse, "BremseG", {"BremsGewicht": bremsmasseg})
            ET.SubElement(nfzg_bremse, "BremseR", {"BremsGewicht": bremsmasser})
        if int(bremsmassemg) > 0:
            nfzg_mg = ET.SubElement(
                nfzg_fahrzeug,
                "MgBremse",
                {"BremsGewicht": bremsmassemg, "spUmschalt": "13.8889"},
            )
            nfzg_mgkennlinie = ET.SubElement(nfzg_mg, "BremsenKennungV")
            ET.SubElement(nfzg_mgkennlinie, "Pkt", {"PktY": "15"})
            ET.SubElement(nfzg_mgkennlinie, "Pkt", {"PktX": "6.9639", "PktY": "12.492"})
            ET.SubElement(
                nfzg_mgkennlinie, "Pkt", {"PktX": "13.9275", "PktY": "10.291"}
            )
            ET.SubElement(nfzg_mgkennlinie, "Pkt", {"PktX": "20.7367", "PktY": "8.722"})
            ET.SubElement(nfzg_mgkennlinie, "Pkt", {"PktX": "27.7003", "PktY": "7.514"})
            ET.SubElement(nfzg_mgkennlinie, "Pkt", {"PktX": "34.6642", "PktY": "6.409"})
            ET.SubElement(nfzg_mgkennlinie, "Pkt", {"PktX": "41.6281", "PktY": "5.505"})
            ET.SubElement(nfzg_mgkennlinie, "Pkt", {"PktX": "48.5917", "PktY": "4.802"})
            ET.SubElement(nfzg_mgkennlinie, "Pkt", {"PktX": "55.5556", "PktY": "4.2"})
            ET.SubElement(nfzg_mgkennlinie, "Stufe", {"StufenWert": "1"})

        laenge = readfloat(ffzg)
        nfzg_Grunddaten.attrib["Laenge"] = str(laenge)
        if laenge == 26.4:
            nfzg_Grunddaten.attrib["Achsstandsumme"] = "5"
            nfzg_Grunddaten.attrib["FesselAnfg"] = "3.7"
            nfzg_Grunddaten.attrib["FesselEnde"] = "3.7"
        # nfzg_fahrzeug.attrib["EinsatzAb"] = datetime.strftime(datetime.(float(ffpn.readline().strip())),"%Y-%m-%d"
        ffzg.readline()  # Einsatz ab (Einsatzzeitraum, nur zur Info) im Windows-Zeitformat
        ffzg.readline()  # Einsatz bis (Einsatzzeitraum, nur zur Info) im Windows-Zeitformat
        ffzg.readline()  # Maximaler Neigewinkel eines Neigetechnik-Fahrzeugs
        ffzg.readline()  # Waggontyp (nur zur Info)
        aussenansichtsdatei_rel = ffzg.readline().strip()
        conv = landschaft.conv_ls(aussenansichtsdatei_rel, no_displacement=True)
        ET.SubElement(
            nfzg_fzgvariante, "DateiAussenansicht", {"Dateiname": conv.dateiname_zusi}
        )
        ffzg.readline()  # Türschließsystem, zulässige Werte: TB0, ICE, Selbstabfertigung, sonst: ohne System
        ffzg.readline()  # reserviert für spätere Funktionen

        os.makedirs(os.path.dirname(z3fahrzeugdateiname_abs), exist_ok=True)
        ET.indent(treefzg, space=" ", level=0)
        treefzg.write(
            z3fahrzeugdateiname_abs, encoding="UTF-8-SIG", xml_declaration=True
        )
    ffzg.close
    return z3fahrzeugdateiname_rel


def conv_lok(
    z2pfad,
    z2fahrzeugdateiname_rel,
    z3pfad,
    zielverzeichnis_rel,
):

    fahrzeugname = os.path.splitext(os.path.basename(z2fahrzeugdateiname_rel))[0]
    z2fahrzeugdateiname_abs = os.path.join(z2pfad, z2fahrzeugdateiname_rel)
    z3fahrzeugdateiname_rel = os.path.join(
        "RollingStock",
        zielverzeichnis_rel,
        os.path.dirname(os.path.relpath(z2fahrzeugdateiname_rel, "loks")),
        fahrzeugname + ".rv.fzg",
    )
    z3fahrzeugdateiname_abs = os.path.join(z3pfad, z3fahrzeugdateiname_rel)

    nfzg_root = ET.Element("Zusi")
    treefzg = ET.ElementTree(nfzg_root)
    nfzg_info = ET.SubElement(
        nfzg_root,
        "Info",
        {
            "DateiTyp": "Fahrzeug",
            "Version": "A.5",
            "MinVersion": "A.1",
            "Beschreibung": "Zusi2-Lok",
        },
    )
    nfzg_fahrzeug = ET.SubElement(nfzg_root, "Fahrzeug")

    with open(z2fahrzeugdateiname_abs, "r", encoding="iso-8859-1") as ffzg:
        # print(
        #     f"{z2fahrzeugdateiname_abs} -> {z3fahrzeugdateiname_abs}", file=sys.stderr
        # )
        ffzg.readline()  # Zusi-Version
        ET.SubElement(nfzg_info, "AutorEintrag", {"AutorName": ffzg.readline().strip()})
        while not ffzg.readline().startswith("#"):  # Freier Text
            pass
        # Geschwindigkeitsmultiplikator ohne Funktion
        ffzg.readline()
        # cwA-Wert (Luftwiderstand) in m²
        cwa = ffzg.readline().strip()
        # Bauart Führerbremsventil, zulässige Werte: KnorrEinheitsbremsventil, D2D5
        bafbv = ffzg.readline().strip()
        # Bauart des Steuerventils, zulässige Werte: Einloesig, Mehrloesig, Mehrloesig HBL-Anschluss
        bastv = ffzg.readline().strip()
        # Bremsmasse Stellung P in kg
        bremsmassep = ffzg.readline().strip()
        # Ansaugvolumen des Luftpressers in l/min
        leistungpresser = readfloatstr(ffzg)
        # Volumen des Hauptluftbehälters in l
        volumenhb = readfloatstr(ffzg)
        # Bremsmasse Stellung G in kg
        bremsmasseg = ffzg.readline().strip()
        # Bremsmasse Stellung R in kg
        bremsmasser = ffzg.readline().strip()
        # Bremsmasse Stellung Mg in kg
        bremsmassemg = ffzg.readline().strip()
        # Zusatzbremse (Lesegilfe)
        ffzg.readline().strip()
        # Maximaler Bremszylinderdruck der Lok in bar
        zbmaxdruck = ffzg.readline().strip()
        # reserviert für spätere Funktionen
        ffzg.readline()
        while not ffzg.readline().startswith("#IF"):  # Endmarke Bremsen
            pass
        # Fahrzeug-Gesamtmasse in kg
        masse = readfloat(ffzg)
        # Länge des Fahrzeugs in m
        laenge = readfloat(ffzg)
        # Höchstgeschwindigkeit in km/h
        vmax = str(readfloat(ffzg) / 3.6)
        # Sound-Datei Achtungspfiff bei Zugabfertigung
        wav = ffzg.readline().strip()
        # Volumen Hilfsluftbehälter in Liter
        rbehaeltervolumen = ffzg.readline().strip()
        # Bremsencharakteristik, (1:Klotzbremse, 0: Scheibenbremse
        scheibenbremse = ffzg.readline().strip() == "0"
        # Übergangsgeschwindigkeit Druckluftergänzungsbremse in m/s
        a = ffzg.readline().strip()
        # Maximale AFB-Beschleunigung in m/s²
        a = ffzg.readline().strip()
        # Drehwinkel Augenpunkt X in rad
        a = ffzg.readline().strip()
        # Drehwinkel Augenpunkt Y in rad
        a = ffzg.readline().strip()
        # Drehwinkel Augenpunkt Z in rad
        a = ffzg.readline().strip()
        # Rastverhalten Auf-Ab-Schalter (1:rastet ein, 0: federt)
        a = ffzg.readline().strip()
        # Erster Cursor Pfeife
        a = ffzg.readline().strip()
        # Zweiter Cursor Pfeife
        a = ffzg.readline().strip()
        # Erster Cursor Luftpresser
        soundluftpresseranlauf = ffzg.readline().strip()
        # Zweiter Cursor Luftpresser
        soundluftpresserauslauf = ffzg.readline().strip()
        # Erster Cursor Lüfter
        a = ffzg.readline().strip()
        # Zweiter Cursor Lüfter
        a = ffzg.readline().strip()
        # Türschließsystem, zulässige Werte: TB0, ICE, Selbstabfertigung, alles andere: Ohne System
        tss = ffzg.readline().strip()
        # reserviert für spätere Funktionen
        ffzg.readline()
        # Sound Hintergrund
        z2hintergrundwav = ffzg.readline().strip()
        # Sound Rollgeräusch
        z2rollenwav = ffzg.readline().strip()
        # Sound Motor Leerlauf
        z2motor0wav = ffzg.readline().strip()
        # Sound Motor 1
        z2motor1wav = ffzg.readline().strip()
        # Sound Motor 2
        z2motor2wav = ffzg.readline().strip()
        # Sound Druckluftstrom
        z2druckluftstromwav = ffzg.readline().strip()
        # Sound Bremsenquietschen
        z2bremsenquitschenwav = ffzg.readline().strip()
        # Sound Schaltwerk
        z2schaltwerkwav = ffzg.readline().strip()
        # Sound Rastgeräusch Fahrschalter
        z2fahrschalterwav = ffzg.readline().strip()
        # Sound Rastgeräusch FbV
        z2fbvwav = ffzg.readline().strip()
        # Sound Weiche
        z2weichewav = ffzg.readline().strip()
        # Sound Kurve
        z2kurvewav = ffzg.readline().strip()
        # Sound Luftpresser
        z2lpwav = ffzg.readline().strip()
        # Sound Signalpfiff
        z2pfeifewav = ffzg.readline().strip()
        # Sound Sifa
        z2sifawav = ffzg.readline().strip()
        # PZB-Hupe
        z2pzbhupewav = ffzg.readline().strip()
        # Sound Zp9 (Abfahrtspfiff)
        wav = ffzg.readline().strip()
        # Sound Tunnel
        wav = ffzg.readline().strip()
        # Sound Brücke Stahl
        wav = ffzg.readline().strip()
        # Sound Brücke Stein
        wav = ffzg.readline().strip()
        # Sound Sprachausgabe AFB
        wav = ffzg.readline().strip()
        # Sound Sprachausgabe Zwangshalt
        wav = ffzg.readline().strip()
        # Sound Motor an
        wav = ffzg.readline().strip()
        # Sound Motor aus
        wav = ffzg.readline().strip()
        # Sound Hauptschalter
        z2hswav = ffzg.readline().strip()
        # Sound LZB-Schnarre
        z2lzbschnarrewav = ffzg.readline().strip()
        # Sound Glocke
        wav = ffzg.readline().strip()
        # Sound Schleuderschutz
        wav = ffzg.readline().strip()
        # Sound Sifa-Zwangsbremsung
        wav = ffzg.readline().strip()
        # Sound TB0
        z2tuersummerwav = ffzg.readline().strip()
        # Endemarke Sounds
        ffzg.readline()
        # Einsatz ab (Einsatzzeitraum, nur zur Info) im Windows-Zeitformat
        einsatzab = readposixtime(ffzg).strftime("%Y-%m-%d")
        # Einsatz bis (Einsatzzeitraum, nur zur Info) im Windows-Zeitformat
        einsatzbis = readposixtime(ffzg).strftime("%Y-%m-%d")
        # Baureihe
        baureihe = ffzg.readline().strip()
        # Anzahl Achsen
        anzahlachsen = int(readfloat(ffzg))
        # Ordnungsnummer
        ordnungsnummer = ffzg.readline().strip()
        # Datei, die das Layout des Führerstands enthält. Der Datei-Pfad bezieht sich auf das Zusi-Stammverzeichnis
        z2fst_rel = ffzg.readline().strip()
        if len(z2fst_rel) > 0:
            fuehrerstandsname = os.path.splitext(os.path.basename(z2fst_rel))[0]
            z2fst_abs = os.path.join(
                z2pfad, os.path.dirname(z2fst_rel), fuehrerstandsname + "_V24.fst"
            )
            z3ftd_rel = os.path.join(
                "RollingStock",
                zielverzeichnis_rel,
                os.path.dirname(os.path.relpath(z2fst_rel, "loks")),
                fahrzeugname + ".ftd",
            )
            z3ftd_abs = os.path.join(z3pfad, z3ftd_rel)
        # reserviert für spätere Funktionen
        ffzg.readline()
        # PZB-System, gültige Angaben: Indusi H54, Indusi I54, Indusi I60, Indusi I60R, PZB90 (Version 1.5), PZB90 (Version 1.6), LZB80_I60R, PZ80, PZ80R, Signum Alles andere führt zu -ohne PZB-
        pzbsystem = ffzg.readline().strip()
        # reserviert für spätere Funktionen
        ffzg.readline()
        # Sound PZB-Hupe, wird nicht ausgewertet
        ffzg.readline()
        # reserviert für spätere Funktionen
        ffzg.readline()
        # ZUB-System, gültige Angaben: ZUB122, alles andere führt zu -ohne ZUB-
        zub = ffzg.readline().strip()
        # Nicht vorhandene PZB-Zugarten, bitweise codiert
        wav = ffzg.readline().strip()
        # Schlusszeichen PZB-System
        ffzg.readline()
        # reserviert für spätere Funktionen
        ffzg.readline()
        # reserviert für spätere Funktionen
        ffzg.readline()
        # Antriebstyp, gültige Angaben: Dieselhydraulisch, Dieselmechanisch, DieselelektrischKonventionell, DieselelektrischDrehstrom, ElektrischReihenschluss, ElektrischDrehstrom
        antriebstyp = ffzg.readline().strip()
        # Antriebsleistung in W
        leistung = ffzg.readline().strip()
        # Max. Anfahrzugkraft in N
        wav = ffzg.readline().strip()
        # Bauart des Fahrschalters, gültige Angaben: FahrschalterStandard, FahrschalterWippe, FahrschalterZugkraft, Kombischalter
        fahrschaltertyp = ffzg.readline().strip()
        # Anzahl der Fahrstufen
        anzahlfahrstufen = int(readfloat(ffzg))
        # reserviert für spätere Funktionen
        ffzg.readline()
        # Anzahl Stufen AFB-Steller
        wav = ffzg.readline().strip()
        # reserviert für spätere Funktionen
        ffzg.readline()
        # Hochlaufzeit des Schaltwerks in sec (muss größer 0 sein)
        geschwschaltwerk = anzahlfahrstufen / readfloat(ffzg)
        # reserviert für spätere Funktionen
        ffzg.readline()
        if antriebstyp == "Dieselhydraulisch":
            # Leerlaufdrehzahl
            ndleer = ffzg.readline().strip()
            # maximale Motordrehzahl
            ndmax = ffzg.readline().strip()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # Wandler-Übersetzungen
            while not ffzg.readline().startswith("#"):
                pass
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # Wirkungsgrad Motor
            etadmot = ffzg.readline().strip()
            # Maximale Bremskraft der dynamischen Bremse in N
            fdynmax = ffzg.readline().strip()
            # Anzahl der Schaltstufen der dynamischen Bremse
            dynbremsstufen = ffzg.readline().strip()
            # Wirkungsgrad Übertragung
            wav = ffzg.readline().strip()
            # Anzahl Wandlerfüllstufen
            wav = ffzg.readline().strip()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # Endmarke Antrieb
            ffzg.readline()
        elif antriebstyp == "Dieselmechanisch":
            # Leerlaufdrehzahl
            ndleer = ffzg.readline().strip()
            # maximale Motordrehzahl
            ndmax = ffzg.readline().strip()
            # Motor-Nenndrehzahl
            ffzg.readline()
            # Übersetzungen
            while not ffzg.readline().startswith("#"):
                pass
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # Wirkungsgrad Motor
            etadmot = ffzg.readline().strip()
            # Maximale Bremskraft der dynamischen Bremse in N
            fdynmax = ffzg.readline().strip()
            # Anzahl der Schaltstufen der dynamischen Bremse
            dynbremsstufen = ffzg.readline().strip()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # Endmarke Antrieb
            ffzg.readline()
        elif antriebstyp == "DieselelektrischKonventionell":
            # Leerlaufdrehzahl
            ndleer = ffzg.readline().strip()
            # maximale Motordrehzahl
            ndmax = ffzg.readline().strip()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # Übersetzungen
            while not ffzg.readline().startswith("#"):
                pass
            # Exponent E-Motor
            ffzg.readline()
            # Nenn-Geschwindigkeit in km/h
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # Wirkungsgrad Motor
            etadmot = ffzg.readline().strip()
            # maximale Spannung in V
            ffzg.readline().strip()
            # Maximale Bremskraft der dynamischen Bremse in N
            fdynmax = ffzg.readline().strip()
            # Anzahl der Schaltstufen der dynamischen Bremse
            dynbremsstufen = ffzg.readline().strip()
            # Wirkungsgrad Übertragung
            wav = ffzg.readline().strip()
            # maximaler Strom in A
            wav = ffzg.readline().strip()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # Endmarke Antrieb
            ffzg.readline()
        elif antriebstyp == "DieselelektrischDrehstrom":
            # Leerlaufdrehzahl
            ndleer = ffzg.readline().strip()
            # maximale Motordrehzahl
            ndmax = ffzg.readline().strip()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # Übersetzungen
            while not ffzg.readline().startswith("#"):
                pass
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # Wirkungsgrad Motor
            etadmot = ffzg.readline().strip()
            # maximale Spannung in V
            ffzg.readline().strip()
            # Maximale Bremskraft der dynamischen Bremse in N
            fdynmax = ffzg.readline().strip()
            # Anzahl der Schaltstufen der dynamischen Bremse
            dynbremsstufen = ffzg.readline().strip()
            # Wirkungsgrad Übertragung
            wav = ffzg.readline().strip()
            # maximaler Strom in A
            wav = ffzg.readline().strip()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # Endmarke Antrieb
            ffzg.readline()
        elif antriebstyp == "ElektrischReihenschluss":
            # reserviert für spätere Funktionen
            ffzg.readline()
            # Übersetzungen
            while not ffzg.readline().startswith("#"):
                pass
            # Exponent E-Motor
            ffzg.readline()
            # Nenn-Geschwindigkeit in km/h
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # Wirkungsgrad Motor
            etamot = ffzg.readline().strip()
            # maximale Spannung in V
            ffzg.readline().strip()
            # Maximale Bremskraft der dynamischen Bremse in N
            fdynmax = ffzg.readline().strip()
            # Anzahl der Schaltstufen der dynamischen Bremse
            dynbremsstufen = ffzg.readline().strip()
            # Wirkungsgrad Übertragung
            ffzg.readline()
            # maximaler Strom in A
            maxoberstrom = ffzg.readline().strip()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # Endmarke Antrieb
            ffzg.readline()
        elif antriebstyp == " ElektrischDrehstrom":
            # reserviert für spätere Funktionen
            ffzg.readline()
            # Übersetzungen
            while not ffzg.readline().startswith("#"):
                pass
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # Wirkungsgrad Motor
            etamot = ffzg.readline().strip()
            # maximale Spannung in V
            ffzg.readline().strip()
            # Maximale Bremskraft der dynamischen Bremse in N
            fdynmax = ffzg.readline().strip()
            # Anzahl der Schaltstufen der dynamischen Bremse
            dynbremsstufen = ffzg.readline().strip()
            # Wirkungsgrad Übertragung
            ffzg.readline()
            # maximaler Strom in A
            maxoberstrom = ffzg.readline().strip()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # reserviert für spätere Funktionen
            ffzg.readline()
            # Endmarke Antrieb
            ffzg.readline()
        # Reibmasse in kg (die Masse, die auf den angetriebenen Rädern lastet)
        reibmasse = ffzg.readline().strip()
        # Faktor (0...1) für die Schleuderneigung des Antriebssystems (0 schleudert immer, 1: ideal gleichmäßige Kraftverteilung
        guetekraftverteilung = ffzg.readline().strip()
        # Schleuderschutzbauart, zulässige Werte Elektronisch, Motordrosselung, Schleuderschutzbremse, sonst: ohne
        schleuderschutzsystem = ffzg.readline().strip()
        # Maximaler Neigewinkel eines Neigetechnik-Fahrzeugs
        gntwinkel = readfloatstr(ffzg)
        # x-Koordinate des Lokführeraugenpunktes
        wav = ffzg.readline().strip()
        # y-Koordinate des Lokführeraugenpunktes
        wav = ffzg.readline().strip()
        # z-Koordinate des Lokführeraugenpunktes
        wav = ffzg.readline().strip()
        # Sifa-System, gültige Angaben: Zeit-Zeit-Sifa, Zeit-Weg-Sifa, Sifa86. Alles andere führt zu -ohne Sifa-
        sifasystem = ffzg.readline().strip()
        # Sound Sifa-Hupe, wird nicht ausgewertet
        ffzg.readline()
        # reserviert für spätere Funktionen
        ffzg.readline()
        # reserviert für spätere Funktionen
        ffzg.readline()
        # Schlusszeichen Sifa
        ffzg.readline()
        # Sound Pfeife
        wav = ffzg.readline().strip()
        # reserviert für spätere Funktionen
        ffzg.readline()
        # reserviert für spätere Funktionen
        ffzg.readline()
        # reserviert für spätere Funktionen
        ffzg.readline()
        # Landschaftsdatei, die die Außenansicht des Fahrzeugs enthält.
        aussenansichtsdatei_rel = ffzg.readline().strip()
        conv = landschaft.conv_ls(aussenansichtsdatei_rel, no_displacement=True)
    ffzg.close

    nfzg_fzgvariante = ET.SubElement(
        nfzg_fahrzeug,
        "FahrzeugVariante",
        {
            "BR": baureihe,
            "HistNummer": baureihe + " " + ordnungsnummer,
            "Beschreibung": baureihe + " " + ordnungsnummer + " Zusi2",
            "EinsatzAb": einsatzab,
            "EinsatzBis": einsatzbis,
            "IDHaupt": "1",
            "IDNeben": "1",
        },
    )
    ET.SubElement(
        nfzg_fzgvariante, "DateiAussenansicht", {"Dateiname": conv.dateiname_zusi}
    )
    ET.SubElement(nfzg_fzgvariante, "DateiFuehrerstand", {"Dateiname": z3ftd_rel})
    ET.SubElement(nfzg_fzgvariante, "DateiFuehrerstandRueckwaerts")
    ET.SubElement(
        nfzg_fahrzeug,
        "FahrzeugGrunddaten",
        {
            "Masse": str(masse),
            "Achsstandsumme": str(laenge * 0.4),
            "RotationsZuschlag": str(masse * 0.2),
            "cwA": cwa,
            "Rollwiderstand": str(masse * 0.01962),
            "Laenge": str(laenge),
            "spMax": str(vmax),
            "Neigewinkel": gntwinkel,
            "HBLVorhanden": "1",
            "LokModus": "1",
            "AnzahlAchsen": str(anzahlachsen),
        },
    )
    nfzg_lp = ET.SubElement(
        nfzg_fahrzeug,
        "Luftpresser",
        {"LeistungPresser": leistungpresser, "VolumenHB": volumenhb},
    )
    nfzg_sndlp = ET.SubElement(
        nfzg_lp,
        "SoundLuftpresser",
        {"PosAnlauf": soundluftpresseranlauf, "PosAuslauf": soundluftpresserauslauf},
    )
    ET.SubElement(
        nfzg_sndlp,
        "Datei",
        {"Dateiname": conv_wav(z2pfad, z2lpwav, z3pfad, zielverzeichnis_rel)},
    )
    if bastv == "Einloesig":
        nfzg_indbrems = ET.SubElement(
            nfzg_fahrzeug,
            "BremseLuftEinlK1",
        )
    elif bastv == "Mehrloesig":
        nfzg_indbrems = ET.SubElement(
            nfzg_fahrzeug,
            "Bremse_KE_GP",
        )
    elif bastv == "Mehrloesig HBL-Anschluss" and not scheibenbremse:
        nfzg_indbrems = ET.SubElement(
            nfzg_fahrzeug,
            "Bremse_KE_Tm",
            {
                "VolumenR": rbehaeltervolumen,
                "VolumenA": "10",
                "VolumenZylinder": "10",
                "FBremsuebersetzung": "20000",
                "HBLAnschluss": "1",
            },
        )
        nfzg_indbremskl = ET.SubElement(nfzg_indbrems, "BremsenKennungV")
        ET.SubElement(nfzg_indbremskl, "Pkt", {"PktY": "3.209"})
        ET.SubElement(nfzg_indbremskl, "Pkt", {"PktX": "2.7856", "PktY": "2.572"})
        ET.SubElement(nfzg_indbremskl, "Pkt", {"PktX": "5.5711", "PktY": "2.017"})
        ET.SubElement(nfzg_indbremskl, "Pkt", {"PktX": "8.3567", "PktY": "1.744"})
        ET.SubElement(nfzg_indbremskl, "Pkt", {"PktX": "11.1419", "PktY": "1.563"})
        ET.SubElement(nfzg_indbremskl, "Pkt", {"PktX": "19.9628", "PktY": "1.212"})
        ET.SubElement(nfzg_indbremskl, "Pkt", {"PktX": "36.0569", "PktY": "1.01"})
        if float(vmax) > 36.0569:
            ET.SubElement(nfzg_indbremskl, "Pkt", {"PktX": vmax, "PktY": "1.0"})
        nfzg_dirbrems = ET.SubElement(
            nfzg_fahrzeug,
            "BremseLuftDirekt",
            {
                "VolumenZylinder": "10",
                "FBremsuebersetzung": "20000",
            },
        )
        nfzg_dirbremskl = ET.SubElement(nfzg_dirbrems, "BremsenKennungV")
        ET.SubElement(nfzg_dirbremskl, "Pkt", {"PktY": "3.209"})
        ET.SubElement(nfzg_dirbremskl, "Pkt", {"PktX": "2.7856", "PktY": "2.572"})
        ET.SubElement(nfzg_dirbremskl, "Pkt", {"PktX": "5.5711", "PktY": "2.017"})
        ET.SubElement(nfzg_dirbremskl, "Pkt", {"PktX": "8.3567", "PktY": "1.744"})
        ET.SubElement(nfzg_dirbremskl, "Pkt", {"PktX": "11.1419", "PktY": "1.563"})
        ET.SubElement(nfzg_dirbremskl, "Pkt", {"PktX": "19.9628", "PktY": "1.212"})
        ET.SubElement(nfzg_dirbremskl, "Pkt", {"PktX": "36.0569", "PktY": "1.01"})
        if float(vmax) > 36.0569:
            ET.SubElement(nfzg_dirbremskl, "Pkt", {"PktX": vmax, "PktY": "1.0"})
    elif bastv == "Mehrloesig HBL-Anschluss" and scheibenbremse:
        nfzg_indbrems = ET.SubElement(
            nfzg_fahrzeug,
            "Bremse_KE_GPR_Scheibe",
        )
    nfzg_indbrems.attrib["AnzahlAchsen"] = str(anzahlachsen)
    if scheibenbremse:
        nfzg_indbrems.attrib["Bremsbauart"] = "1"
    else:
        nfzg_indbrems.attrib["Bremsbauart"] = "2"
    ET.SubElement(nfzg_indbrems, "BremseP", {"BremsGewicht": bremsmassep})
    ET.SubElement(nfzg_indbrems, "BremseG", {"BremsGewicht": bremsmasseg})
    if not bastv == "Einloesig":
        ET.SubElement(nfzg_indbrems, "BremseR", {"BremsGewicht": bremsmasser})
    if antriebstyp == "ElektrischReihenschluss":
        if int(fdynmax) > 0:
            nfzg_dynbrems = ET.SubElement(
                nfzg_fahrzeug,
                "DynbremseElektrReihenschluss",
                {
                    "Fremderregt": "1",
                    "Volt": "2",
                    "Antriebsachsen": str(anzahlachsen),
                    "Reibmasse": reibmasse,
                    "GueteKraftverteilung": guetekraftverteilung,
                    "GrenzdruckHL": "3",
                },
            )
            nfzg_dynbremskl = ET.SubElement(
                nfzg_dynbrems,
                "Kennfeld",
                {"xText": "Geschwindigkeit", "yText": "Bremskraft"},
            )
            ET.SubElement(nfzg_dynbremskl, "Pkt", {"PktY": "0.0"})
            ET.SubElement(nfzg_dynbremskl, "Pkt", {"PktX": "8.0", "PktY": "0.0"})
            ET.SubElement(nfzg_dynbremskl, "Pkt", {"PktX": "12.0", "PktY": fdynmax})
            ET.SubElement(nfzg_dynbremskl, "Pkt", {"PktX": vmax, "PktY": fdynmax})
            ET.SubElement(nfzg_dynbremskl, "Stufe", {"StufenWert": "1"})
            ET.SubElement(
                nfzg_dynbrems,
                "Nachlaufsteuerung",
                {"AnzahlSchaltstufen": dynbremsstufen},
            )
        nfzg_antrieb = ET.SubElement(
            nfzg_fahrzeug,
            "AntriebsmodellElektrischReihenschluss",
            {
                "Volt": "2",
                "etaTrafo": "0.97",
                "MaxOberstrom": maxoberstrom,
                "GrenzwertUeberwacht": "0",
                "Leistung": leistung,
                "Antriebsachsen": str(anzahlachsen),
                "Reibmasse": reibmasse,
                "GueteKraftverteilung": guetekraftverteilung,
                "GrenzdruckHL": "3",
            },
        )
        ET.SubElement(
            nfzg_antrieb,
            "Nachlaufsteuerung",
            {
                "AnzahlSchaltstufen": str(round(anzahlfahrstufen)),
                "GeschwAuf": str(geschwschaltwerk),
                "GeschwAb": str(geschwschaltwerk),
            },
        )

    # if steuerventil == "Einloesig":
    # nfzg_bremse = ET.SubElement(
    # nfzg_fahrzeug,
    # "BremseLuftEinlK1",
    # {
    # "VolumenB": rbehaeltervolumen,
    # "VolumenZylinder": "10",
    # "FBremsuebersetzung": "12724.0",
    # },
    # )
    # nfzg_bremskennlinie = ET.SubElement(nfzg_bremse, "BremsenKennungV")
    # ET.SubElement(nfzg_bremskennlinie, "Pkt", {"PktY": "2.419"})
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "2.7236", "PktY": "1.939"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "2.7856", "PktY": "1.939"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "5.5092", "PktY": "1.529"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "5.5711", "PktY": "1.521"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "8.2947", "PktY": "1.319"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "11.1419", "PktY": "1.178"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "19.9939", "PktY": "0.913"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "22.2222", "PktY": "0.892"}
    # )
    # ET.SubElement(nfzg_bremskennlinie, "Stufe", {"StufenWert": "1"})
    # ET.SubElement(nfzg_bremse, "BremseP", {"BremsGewicht": bremsmassep})
    # ET.SubElement(nfzg_bremse, "BremseG", {"BremsGewicht": bremsmasseg})
    # elif ("Mehrloesig" in steuerventil) and not scheibenbremse:
    # nfzg_bremse = ET.SubElement(
    # nfzg_fahrzeug,
    # "Bremse_KE_GP",
    # {
    # "VolumenR": rbehaeltervolumen,
    # "VolumenA": "10",
    # "VolumenZylinder": "10",
    # "FBremsuebersetzung": "12724.0",
    # "HBLAnschluss": hblvorhanden,
    # },
    # )
    # nfzg_bremskennlinie = ET.SubElement(nfzg_bremse, "BremsenKennungV")
    # ET.SubElement(nfzg_bremskennlinie, "Pkt", {"PktY": "2.419"})
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "2.7236", "PktY": "1.939"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "2.7856", "PktY": "1.939"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "5.5092", "PktY": "1.529"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "5.5711", "PktY": "1.521"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "8.2947", "PktY": "1.319"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "11.1419", "PktY": "1.178"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "19.9939", "PktY": "0.913"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "22.2222", "PktY": "0.892"}
    # )
    # ET.SubElement(nfzg_bremskennlinie, "Stufe", {"StufenWert": "1"})
    # ET.SubElement(nfzg_bremse, "BremseP", {"BremsGewicht": bremsmassep})
    # ET.SubElement(nfzg_bremse, "BremseG", {"BremsGewicht": bremsmasseg})
    # else:
    # nfzg_bremse = ET.SubElement(
    # nfzg_fahrzeug,
    # "Bremse_KE_GPR_Scheibe",
    # {
    # "VolumenR": rbehaeltervolumen,
    # "VolumenA": "10",
    # "VolumenZylinder": "10",
    # "FBremsuebersetzung": "12724.0",
    # "HBLAnschluss": hblvorhanden,
    # },
    # )
    # nfzg_bremskennlinie = ET.SubElement(nfzg_bremse, "BremsenKennungV")
    # ET.SubElement(nfzg_bremskennlinie, "Pkt", {"PktY": "1.1"})
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "1.5475", "PktY": "1.072"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "2.6308", "PktY": "1.053"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "2.7856", "PktY": "1.05"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "5.4164", "PktY": "1.012"}
    # )
    # ET.SubElement(
    # nfzg_bremskennlinie, "Pkt", {"PktX": "5.5711", "PktY": "1.01"}
    # )
    # ET.SubElement(nfzg_bremskennlinie, "Pkt", {"PktX": "10.9872", "PktY": "1"})
    # ET.SubElement(nfzg_bremskennlinie, "Pkt", {"PktX": "11.1419", "PktY": "1"})
    # ET.SubElement(nfzg_bremskennlinie, "Pkt", {"PktX": "55.5556", "PktY": "1"})
    # ET.SubElement(nfzg_bremskennlinie, "Stufe", {"StufenWert": "1"})
    # ET.SubElement(nfzg_bremse, "BremseP", {"BremsGewicht": bremsmassep})
    # ET.SubElement(nfzg_bremse, "BremseG", {"BremsGewicht": bremsmasseg})
    # ET.SubElement(nfzg_bremse, "BremseR", {"BremsGewicht": bremsmasser})
    # if int(bremsmassemg) > 0:
    # nfzg_mg = ET.SubElement(
    # nfzg_fahrzeug,
    # "MgBremse",
    # {"BremsGewicht": bremsmassemg, "spUmschalt": "13.8889"},
    # )
    # nfzg_mgkennlinie = ET.SubElement(nfzg_mg, "BremsenKennungV")
    # ET.SubElement(nfzg_mgkennlinie, "Pkt", {"PktY": "15"})
    # ET.SubElement(nfzg_mgkennlinie, "Pkt", {"PktX": "6.9639", "PktY": "12.492"})
    # ET.SubElement(
    # nfzg_mgkennlinie, "Pkt", {"PktX": "13.9275", "PktY": "10.291"}
    # )
    # ET.SubElement(nfzg_mgkennlinie, "Pkt", {"PktX": "20.7367", "PktY": "8.722"})
    # ET.SubElement(nfzg_mgkennlinie, "Pkt", {"PktX": "27.7003", "PktY": "7.514"})
    # ET.SubElement(nfzg_mgkennlinie, "Pkt", {"PktX": "34.6642", "PktY": "6.409"})
    # ET.SubElement(nfzg_mgkennlinie, "Pkt", {"PktX": "41.6281", "PktY": "5.505"})
    # ET.SubElement(nfzg_mgkennlinie, "Pkt", {"PktX": "48.5917", "PktY": "4.802"})
    # ET.SubElement(nfzg_mgkennlinie, "Pkt", {"PktX": "55.5556", "PktY": "4.2"})
    # ET.SubElement(nfzg_mgkennlinie, "Stufe", {"StufenWert": "1"})

    # laenge = readfloat(ffzg)
    # nfzg_Grunddaten.attrib["Laenge"] = str(laenge)
    # if laenge == 26.4:
    # nfzg_Grunddaten.attrib["Achsstandsumme"] = "5"
    # nfzg_Grunddaten.attrib["FesselAnfg"] = "3.7"
    # nfzg_Grunddaten.attrib["FesselEnde"] = "3.7"
    #       nfzg_fahrzeug.attrib["EinsatzAb"] = datetime.strftime(datetime.(float(ffpn.readline().strip())),"%Y-%m-%d"
    # ffzg.readline()  # Einsatz ab (Einsatzzeitraum, nur zur Info) im Windows-Zeitformat
    # ffzg.readline()  # Einsatz bis (Einsatzzeitraum, nur zur Info) im Windows-Zeitformat
    # ffzg.readline()  # Maximaler Neigewinkel eines Neigetechnik-Fahrzeugs
    # ffzg.readline()  # Waggontyp (nur zur Info)
    # aussenansichtsdatei_rel = ffzg.readline().strip()
    # conv = landschaft.conv_ls(aussenansichtsdatei_rel, no_displacement=True)
    # ET.SubElement(
    # nfzg_fzgvariante, "DateiAussenansicht", {"Dateiname": conv.dateiname_zusi}
    # )
    # ffzg.readline()  # Türschließsystem, zulässige Werte: TB0, ICE, Selbstabfertigung, sonst: ohne System
    # ffzg.readline()  # reserviert für spätere Funktionen

    os.makedirs(os.path.dirname(z3fahrzeugdateiname_abs), exist_ok=True)
    ET.indent(treefzg, space=" ", level=0)
    treefzg.write(z3fahrzeugdateiname_abs, encoding="UTF-8-SIG", xml_declaration=True)

    if len(z2fst_rel) > 0:
        with open(z2fst_abs, "r", encoding="iso-8859-1") as ffst:
            ffst.readline()  # Zusi-Version
            ffst.readline()  # mindestens erforderliche Zusi-Version
            while ffst.readline().startswith("#"):  # Freier Text
                pass
            print(ffst.readline())
        ffst.close

        nfst_root = ET.Element("Zusi")
        treefst = ET.ElementTree(nfst_root)
        ET.SubElement(
            nfst_root,
            "Info",
            {
                "DateiTyp": "Fuehrerstand",
                "Version": "A.7",
                "MinVersion": "A.1",
                "Beschreibung": "Zusi2-Lok",
            },
        )
        nfst_fst = ET.SubElement(
            nfst_root,
            "Fuehrerstand",
        )
        nfst_funkt = ET.SubElement(
            nfst_fst,
            "Funktionalitaeten",
        )
        if fahrschaltertyp == "Standard":
            nfst_fahrschalter = ET.SubElement(
                nfst_funkt,
                "Kombischalter",
                {"FktName": "Fahrschalter", "Tastaturzuordnung": "1"},
            )
            for i in range(anzahlfahrstufen + 1):
                nfst_fahrstufe = ET.SubElement(nfst_fahrschalter, "Raste")
                ET.SubElement(
                    nfst_fahrstufe,
                    "Belegung",
                    {
                        "FunktionStr": "Fahrstufe",
                        "Parameter": str(round((i / anzahlfahrstufen), 4)),
                    },
                )
                if i > 0:
                    ET.SubElement(
                        nfst_fahrstufe,
                        "Koppelung",
                        {
                            "Koppelart": "Koppelart_Verriegeln",
                            "NameGekoppelterSchalter": "Richtungsschalter",
                        },
                    )
        elif fahrschaltertyp == "Wippe":
            print("Achtung andere Fahrschalter")
        elif fahrschaltertyp == "Zugkraft":
            print("Achtung andere Fahrschalter")
        elif fahrschaltertyp == "Kombischalter":
            print("Achtung andere Fahrschalter")
        if len(z2fahrschalterwav) > 0:
            ET.SubElement(
                ET.SubElement(
                    nfst_fahrschalter,
                    "RastSound",
                ),
                "Datei",
                {
                    "Dateiname": conv_wav(
                        z2pfad, z2fahrschalterwav, z3pfad, zielverzeichnis_rel
                    )
                },
            )
        if int(fdynmax) > 0:
            nfst_bremssteller = ET.SubElement(
                nfst_funkt,
                "Kombischalter",
                {
                    "FktName": "Bremssteller",
                    "Tastaturzuordnung": "2",
                    "Grundstellung": dynbremsstufen,
                },
            )
            for i in range(int(dynbremsstufen), -1, -1):
                nfst_bremsstellerstufe = ET.SubElement(nfst_bremssteller, "Raste")
                ET.SubElement(
                    nfst_bremsstellerstufe,
                    "Belegung",
                    {
                        "FunktionStr": "DynBremseX",
                        "Parameter": str(round((i / int(dynbremsstufen)), 4)),
                    },
                )

        # AFB zurückgestellt

        if bafbv == "KnorrEinheitsbremsventil":
            nfst_FbV = ET.SubElement(
                nfst_funkt,
                "Kombischalter",
                {"FktName": "Führerbremsventil K10", "Tastaturzuordnung": "4"},
            )
            # for i in range(anzahlfahrstufen + 1):
            #     nfst_fahrstufe = ET.SubElement(nfst_FbV, "Raste")
            #     ET.SubElement(
            #         nfst_fahrstufe,
            #         "Belegung",
            #         {
            #             "FunktionStr": "Fahrstufe",
            #             "Parameter": str(round((i / anzahlfahrstufen), 4)),
            #         },
            #     )
            #     if i > 0:
            #         ET.SubElement(
            #             nfst_fahrstufe,
            #             "Koppelung",
            #             {
            #                 "Koppelart": "Koppelart_Verriegeln",
            #                 "NameGekoppelterSchalter": "Richtungsschalter",
            #             },
            #         )
        else:
            nfst_FbV = ET.SubElement(
                nfst_funkt,
                "Kombischalter",
                {
                    "FedertUnten": "1",
                    "Grundstellung": "8",
                    "FktName": "Führerbremsventil D2/D5",
                    "Tastaturzuordnung": "4",
                },
            )
            if len(z2fbvwav) > 0:
                ET.SubElement(
                    ET.SubElement(nfst_FbV, "RastSound", {"Lautstaerke": "1"}),
                    "Datei",
                    {
                        "Dateiname": conv_wav(
                            z2pfad, z2fbvwav, z3pfad, zielverzeichnis_rel
                        )
                    },
                )
                nfst_fbvstufe = ET.SubElement(nfst_FbV, "Raste")
                ET.SubElement(
                    nfst_fbvstufe,
                    "Belegung",
                    {
                        "FunktionStr": "HllBremsen",
                    },
                )
                nfst_fbvstufe = ET.SubElement(
                    nfst_FbV, "Raste", {"SperreRunter": "1", "SperrZeit": "0.5"}
                )
                ET.SubElement(
                    nfst_fbvstufe,
                    "Belegung",
                    {"FunktionStr": "HllDruck", "Parameter": "3.5"},
                )
                ET.SubElement(
                    nfst_fbvstufe,
                    "Koppelung",
                    {
                        "NameGekoppelterSchalter": "Bremssteller",
                        "RastenNummer": "0",
                        "Koppelart": "Koppelart_Mitnehmen",
                    },
                )
                nfst_fbvstufe = ET.SubElement(nfst_FbV, "Raste")
                ET.SubElement(
                    nfst_fbvstufe,
                    "Belegung",
                    {"FunktionStr": "HllDruck", "Parameter": "3.8"},
                )
                ET.SubElement(
                    nfst_fbvstufe,
                    "Koppelung",
                    {
                        "NameGekoppelterSchalter": "Bremssteller",
                        "RastenNummer": "1",
                        "Koppelart": "Koppelart_Mitnehmen",
                    },
                )
                nfst_fbvstufe = ET.SubElement(nfst_FbV, "Raste")
                ET.SubElement(
                    nfst_fbvstufe,
                    "Belegung",
                    {"FunktionStr": "HllDruck", "Parameter": "4.0"},
                )
                ET.SubElement(
                    nfst_fbvstufe,
                    "Koppelung",
                    {
                        "NameGekoppelterSchalter": "Bremssteller",
                        "RastenNummer": "2",
                        "Koppelart": "Koppelart_Mitnehmen",
                    },
                )
                nfst_fbvstufe = ET.SubElement(nfst_FbV, "Raste")
                ET.SubElement(
                    nfst_fbvstufe,
                    "Belegung",
                    {"FunktionStr": "HllDruck", "Parameter": "4.2"},
                )
                ET.SubElement(
                    nfst_fbvstufe,
                    "Koppelung",
                    {
                        "NameGekoppelterSchalter": "Bremssteller",
                        "RastenNummer": "3",
                        "Koppelart": "Koppelart_Mitnehmen",
                    },
                )
                nfst_fbvstufe = ET.SubElement(nfst_FbV, "Raste")
                ET.SubElement(
                    nfst_fbvstufe,
                    "Belegung",
                    {"FunktionStr": "HllDruck", "Parameter": "4.4"},
                )
                ET.SubElement(
                    nfst_fbvstufe,
                    "Koppelung",
                    {
                        "NameGekoppelterSchalter": "Bremssteller",
                        "RastenNummer": "4",
                        "Koppelart": "Koppelart_Mitnehmen",
                    },
                )
                nfst_fbvstufe = ET.SubElement(nfst_FbV, "Raste")
                ET.SubElement(
                    nfst_fbvstufe,
                    "Belegung",
                    {"FunktionStr": "HllDruck", "Parameter": "4.7"},
                )
                ET.SubElement(
                    nfst_fbvstufe,
                    "Koppelung",
                    {
                        "NameGekoppelterSchalter": "Bremssteller",
                        "RastenNummer": "5",
                        "Koppelart": "Koppelart_Mitnehmen",
                    },
                )
                nfst_fbvstufe = ET.SubElement(nfst_FbV, "Raste")
                ET.SubElement(
                    nfst_fbvstufe,
                    "Belegung",
                    {
                        "FunktionStr": "HllMittel",
                    },
                )
                ET.SubElement(
                    nfst_fbvstufe,
                    "Koppelung",
                    {
                        "NameGekoppelterSchalter": "Bremssteller",
                        "RastenNummer": "6",
                        "Koppelart": "Koppelart_Mitnehmen",
                    },
                )
                nfst_fbvstufe = ET.SubElement(nfst_FbV, "Raste")
                ET.SubElement(
                    nfst_fbvstufe,
                    "Belegung",
                    {"FunktionStr": "HllDruck", "Parameter": "5.0"},
                )
                nfst_fbvstufe = ET.SubElement(nfst_FbV, "Raste")
                ET.SubElement(
                    nfst_fbvstufe,
                    "Belegung",
                    {
                        "FunktionStr": "HllFuellen",
                    },
                )
                ET.SubElement(
                    nfst_funkt,
                    "Angleicher",
                    {
                        "Taster": "1",
                        "FktName": "Angleicher",
                        "Tastaturzuordnung": "41",  # Wegen Bug in TCP-Schnittstelle
                    },
                )
        nfst_zbv = ET.SubElement(
            nfst_funkt,
            "Kombischalter",
            {
                "FktName": "Zusatzbremsventil",
                "Tastaturzuordnung": "5",
                "FedertOben": "1",
                "Grundstellung": "2",
            },
        )
        nfst_zbvstellung = ET.SubElement(nfst_zbv, "Raste")
        ET.SubElement(nfst_zbvstellung, "Belegung", {"FunktionStr": "ZbvBremsen"})
        nfst_zbvstellung = ET.SubElement(nfst_zbv, "Raste")
        ET.SubElement(nfst_zbvstellung, "Belegung", {"FunktionStr": "ZbvMittel"})
        nfst_zbvstellung = ET.SubElement(nfst_zbv, "Raste")
        ET.SubElement(nfst_zbvstellung, "Belegung", {"FunktionStr": "ZbvLoesen"})
        nfst_richtungsschalter = ET.SubElement(
            nfst_funkt,
            "Kombischalter",
            {
                "FktName": "Richtungsschalter",
                "Tastaturzuordnung": "7",
                "Mittelposition": "1",
                "Grundstellung": "0",
            },
        )
        nfst_richtung = ET.SubElement(nfst_richtungsschalter, "Raste")
        ET.SubElement(nfst_richtung, "Belegung", {"FunktionStr": "RischaV"})
        nfst_richtung = ET.SubElement(nfst_richtungsschalter, "Raste")
        ET.SubElement(nfst_richtung, "Belegung", {"FunktionStr": "Rischa0"})
        ET.SubElement(
            nfst_richtung,
            "Koppelung",
            {
                "Koppelart": "Koppelart_Verriegeln",
                "NameGekoppelterSchalter": "Fahrschalter",
            },
        )
        nfst_richtung = ET.SubElement(nfst_richtungsschalter, "Raste")
        ET.SubElement(nfst_richtung, "Belegung", {"FunktionStr": "RischaR"})
        nfst_sand = ET.SubElement(
            nfst_funkt,
            "Sander",
            {"Taster": "1", "FktName": "Sander", "Tastaturzuordnung": "9"},
        )

        # Türsystem zurückgstellt tss

        nfst_pfeife = ET.SubElement(
            nfst_funkt,
            "Pfeife",
            {"Taster": "1", "FktName": "Pfeife/Glocke", "Tastaturzuordnung": "12"},
        )
        if len(z2pfeifewav) > 0:
            ET.SubElement(
                ET.SubElement(
                    nfst_pfeife,
                    "SoundTief",
                ),
                "Datei",
                {
                    "Dateiname": conv_wav(
                        z2pfad, z2pfeifewav, z3pfad, zielverzeichnis_rel
                    )
                },
            )
        nfst_luefter = ET.SubElement(
            nfst_funkt,
            "Luefter",
            {"Taster": "1", "FktName": "Lüfter", "Tastaturzuordnung": "14"},
        )

        pzbvorhanden = False
        if pzbsystem == "Indusi H54" or pzbsystem == "Indusi I54":
            z3pzbsystem = "IndusiI54"
            pzbvorhanden = True
        elif pzbsystem == "Indusi I60":
            z3pzbsystem = "IndusiI60"
            pzbvorhanden = True
        elif pzbsystem == "Indusi I60R":
            z3pzbsystem = "IndusiI60R"
            pzbvorhanden = True
        elif pzbsystem == "PZB90 (Version 1.5)":
            z3pzbsystem = "PZB90I60R_V15"
            pzbvorhanden = True
        elif pzbsystem == "PZB90 (Version 1.6)":
            z3pzbsystem = "PZB90I60R_V20"
            pzbvorhanden = True
        elif pzbsystem == "LZB80 / I80":
            z3pzbsystem = "LZB80_I80"
            pzbvorhanden = True
        elif pzbsystem == "PZ80":
            z3pzbsystem = "PZ80"
            pzbvorhanden = True
        elif pzbsystem == "PZ80R":
            z3pzbsystem = "PZB90_PZ80R_V20"
            pzbvorhanden = True
        if pzbvorhanden:
            nfst_pzb = ET.SubElement(
                nfst_funkt,
                z3pzbsystem,
            )
            if len(z2pzbhupewav) > 0:
                ET.SubElement(
                    ET.SubElement(
                        nfst_pzb,
                        "SoundIndusiHupe",
                    ),
                    "Datei",
                    {
                        "Dateiname": conv_wav(
                            z2pfad, z2pzbhupewav, z3pfad, zielverzeichnis_rel
                        )
                    },
                )
        if pzbsystem == "LZB80 / I80":
            if len(z2lzbschnarrewav) > 0:
                ET.SubElement(
                    ET.SubElement(
                        nfst_pzb,
                        "SoundIndusiSchnarre",
                    ),
                    "Datei",
                    {
                        "Dateiname": conv_wav(
                            z2pfad, z2pzbhupewav, z3pfad, zielverzeichnis_rel
                        )
                    },
                )
        sifavorhanden = False
        if sifasystem == "Zeit-Zeit-Sifa":
            z3sifasystem = "Sifa_ZeitZeit"
            sifavorhanden = True
        elif sifasystem == "Zeit-Weg-Sifa":
            z3sifasystem = "Sifa_ZeitWeg"
            sifavorhanden = True
        elif sifasystem == "Sifa86":
            z3sifasystem = "Sifa86"
            sifavorhanden = True
        if sifavorhanden:
            nfst_sifa = ET.SubElement(
                nfst_funkt, z3sifasystem, {"Taster": "1", "Tastaturzuordnung": "16"}
            )
            if len(z2sifawav) > 0:
                ET.SubElement(
                    ET.SubElement(
                        nfst_sifa,
                        "SoundSifa",
                    ),
                    "Datei",
                    {
                        "Dateiname": conv_wav(
                            z2pfad, z2sifawav, z3pfad, zielverzeichnis_rel
                        )
                    },
                )
        nfst_hs = ET.SubElement(
            nfst_funkt,
            "Kombischalter",
            {
                "FktName": "Hauptschalter",
                "Tastaturzuordnung": "17",
                "FedertOben": "1",
                "FedertUnten": "1",
                "Grundstellung": "1",
                "Mittelposition": "1",
            },
        )
        nfst_hsstellung = ET.SubElement(nfst_hs, "Raste")
        ET.SubElement(nfst_hsstellung, "Belegung", {"FunktionStr": "HauptschalterAus"})
        nfst_hsstellung = ET.SubElement(nfst_hs, "Raste")
        ET.SubElement(nfst_hsstellung, "Belegung", {"FunktionStr": "HauptschalterNull"})
        nfst_hsstellung = ET.SubElement(nfst_hs, "Raste")
        ET.SubElement(nfst_hsstellung, "Belegung", {"FunktionStr": "HauptschalterEin"})
        if schleuderschutzsystem == "Elektronisch":
            nfst_schleuderschutz = ET.SubElement(
                nfst_funkt,
                "SchleuderschutzElektr",
                {"FktName": "Elektronischer Schleuderschutz"},
            )
        elif schleuderschutzsystem == "Motordrosselung":
            nfst_schleuderschutz = ET.SubElement(
                nfst_funkt,
                "SchleuderschutzDrosselung",
                {"FktName": "Schleuderschutz (Motordrosselung)"},
            )
        elif schleuderschutzsystem == "Schleuderschutzbremse":
            nfst_schleuderschutz = ET.SubElement(
                nfst_funkt,
                "Schleuderschutzbremse",
                {
                    "Taster": "1",
                    "FktName": "Schleuderschutzbremse",
                    "Tastaturzuordnung": "19",
                },
            )
        nfst_sa = ET.SubElement(
            nfst_funkt,
            "Kombischalter",
            {
                "FktName": "Stromabnehmer",
                "Tastaturzuordnung": "43",
                "FedertOben": "1",
                "FedertUnten": "1",
                "Grundstellung": "1",
                "Mittelposition": "1",
            },
        )
        nfst_sastellung = ET.SubElement(nfst_sa, "Raste")
        ET.SubElement(nfst_sastellung, "Belegung", {"FunktionStr": "StromabnehmerAb"})
        nfst_sastellung = ET.SubElement(nfst_sa, "Raste")
        ET.SubElement(nfst_sastellung, "Belegung", {"FunktionStr": "StromabnehmerNull"})
        nfst_sastellung = ET.SubElement(nfst_sa, "Raste")
        ET.SubElement(nfst_sastellung, "Belegung", {"FunktionStr": "StromabnehmerAuf"})
        nfst_lpaus = ET.SubElement(
            nfst_funkt,
            "LuftpresserAus",
            {"Taster": "1", "FktName": "Luftpresser aus", "Tastaturzuordnung": "45"},
        )

        if len(z2hintergrundwav) > 0:
            nfst_fstsound = ET.SubElement(nfst_funkt, "FuehrerstandSound")
            nfst_sound = ET.SubElement(nfst_fstsound, "Sound", {"Lautstaerke": "1"})
            ET.SubElement(
                nfst_sound,
                "Datei",
                {
                    "Dateiname": conv_wav(
                        z2pfad, z2hintergrundwav, z3pfad, zielverzeichnis_rel
                    )
                },
            )
        if len(z2druckluftstromwav) > 0:
            nfst_fstsound = ET.SubElement(nfst_funkt, "FuehrerstandSound")
            nfst_sound = ET.SubElement(
                nfst_fstsound, "Sound", {"Loop": "1", "Lautstaerke": "1"}
            )
            ET.SubElement(
                nfst_sound,
                "Datei",
                {
                    "Dateiname": conv_wav(
                        z2pfad, z2druckluftstromwav, z3pfad, zielverzeichnis_rel
                    )
                },
            )
            nfst_soundabhkt = ET.SubElement(
                nfst_fstsound,
                "Abhaengigkeit",
                {"PhysikGroesse": "6", "LautstaerkeAbh": "1"},
            )
            nfst_soundkennfeld = ET.SubElement(nfst_soundabhkt, "Kennfeld")
            ET.SubElement(nfst_soundkennfeld, "Pkt", {"PktX": "0", "PktY": "0"})
            ET.SubElement(nfst_soundkennfeld, "Pkt", {"PktX": "1", "PktY": "1"})
        nfst_grafik = ET.SubElement(
            nfst_fst,
            "Grafik",
        )
        ET.SubElement(nfst_grafik, "RenderFlags", {"TexVoreinstellung": "2"})
        ET.SubElement(nfst_grafik, "Grunddaten", {"GrafikName": "Hauptansicht"})

    os.makedirs(os.path.dirname(z3ftd_abs), exist_ok=True)
    ET.indent(treefst, space=" ", level=0)
    treefst.write(z3ftd_abs, encoding="UTF-8-SIG", xml_declaration=True)

    return z3fahrzeugdateiname_rel
