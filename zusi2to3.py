#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET

from zusi2to3 import strecke, fahrplan


treekonv = ET.parse("strecken.xml")
nkonv_root = treekonv.getroot()

for ikonv in range(len(nkonv_root)):
    if "Pfade" in nkonv_root[ikonv].tag:
        if "Zusi2Pfad" in nkonv_root[ikonv].attrib:
            z2pfad = nkonv_root[ikonv].attrib["Zusi2Pfad"]
        try:
            z2pfad = os.environ["ZUSI2_DATAPATH"]
            print("Verwende Pfad Zusi2-Pfad aus der Umgebungsvariable: " + z2pfad)
        except:
            print(
                "Umgebungsvariable für den Zusi3-Pfad nicht gesetzt. Verwende Pfad aus der XML-Datei: "
                + z2pfad
            )
        if "Zusi3Pfad" in nkonv_root[ikonv].attrib:
            z3pfad = nkonv_root[ikonv].attrib["Zusi3Pfad"]
            print("Verwende Pfad Zusi3-Pfad aus der Umgebungsvariable: " + z3pfad)
        try:
            z3pfad = os.environ["ZUSI3_DATAPATH"]
        except:
            print(
                "Umgebungsvariable für den Zusi3-Pfad nicht gesetzt. Verwende Pfad aus der XML-Datei: "
                + z3pfad
            )
    if "Strecke" in nkonv_root[ikonv].tag:
        if ("Streckendatei" in nkonv_root[ikonv].attrib) and (
            "Zielverzeichnis" in nkonv_root[ikonv].attrib
        ):
            zielverzeichnis_rel = nkonv_root[ikonv].attrib["Zielverzeichnis"]
            (st3_name, rekursionstiefe) = strecke.conv_str(
                z2pfad,
                nkonv_root[ikonv].attrib["Streckendatei"],
                z3pfad,
                zielverzeichnis_rel,
            )
            for jkonv in range(len(nkonv_root[ikonv])):
                if "Fahrplan" in nkonv_root[ikonv][jkonv].tag:
                    if "Fahrplandatei" in nkonv_root[ikonv][jkonv].attrib:
                        fahrplan.conv_fpn(
                            z2pfad,
                            nkonv_root[ikonv][jkonv].attrib["Fahrplandatei"],
                            st3_name,
                            z3pfad,
                            zielverzeichnis_rel,
                            rekursionstiefe,
                        )
