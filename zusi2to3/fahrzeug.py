#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import xml.etree.ElementTree as ET
from collections import namedtuple
from datetime import datetime

from . import common, landschaft
from .common import readfloat, readfloatstr

VerknParameter = namedtuple(
    "VerknParameter", ["dateiname_zusi", "x", "y", "z", "rx", "ry", "rz", "boundingr"]
)


def conv_wagen(
    z2pfad,
    z2fahrzeugdateiname_rel,
    z3pfad,
    zielverzeichnis_rel,
):

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
        print(
            f"{z2fahrzeugdateiname_abs} -> {z3fahrzeugdateiname_abs}", file=sys.stderr
        )
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
