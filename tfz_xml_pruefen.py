#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

treetfz = ET.parse("tfz.xml")
ntfz_root = treetfz.getroot()


for j in range(len(ntfz_root)):
    z2fahrzeugdateiname = ""
    z3fahrzeugdateiname = ""
    z3fahrzeughauptid = ""
    z3fahrzeugnebenid = ""
    z3saschaltung = ""
    if "Fahrzeug" in ntfz_root[j].tag:
        if "Z2Dateiname_rel" in ntfz_root[j].attrib:
            if "Z2Dateiname_rel" in ntfz_root[j].attrib:
                z2fahrzeugdateiname = ntfz_root[j].attrib["Z2Dateiname_rel"]
            if "FahrzeugInfo" in ntfz_root[j][0].tag:
                if "IDHaupt" in ntfz_root[j][0].attrib:
                    z3fahrzeughauptid = ntfz_root[j][0].attrib["IDHaupt"]
                if "IDNeben" in ntfz_root[j][0].attrib:
                    z3fahrzeugnebenid = ntfz_root[j][0].attrib["IDNeben"]
                if "SASchaltung" in ntfz_root[j][0].attrib:
                    z3saschaltung = ntfz_root[j][0].attrib["SASchaltung"]
                if "Datei" in ntfz_root[j][0][0].tag:
                    if "Z3Dateiname_rel" in ntfz_root[j][0][0].attrib:
                        z3fahrzeugdateiname = ntfz_root[j][0][0].attrib[
                            "Z3Dateiname_rel"
                        ]
    print(
        z2fahrzeugdateiname
        + "  "
        + z3fahrzeugdateiname
        + " HauptID: "
        + z3fahrzeughauptid
        + " NebenID: "
        + z3fahrzeugnebenid
        + " SASchaltung: "
        + z3saschaltung
    )
