#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

treewag = ET.parse("wagen.xml")
nwag_root = treewag.getroot()

z2fahrzeugdateiname = ""
z3fahrzeugdateiname = ""
z3fahrzeughauptid = ""
z3fahrzeugnebenid = ""

for j in range(len(nwag_root)):
    if "Fahrzeug" in nwag_root[j].tag:
        if "Z2Dateiname_rel" in nwag_root[j].attrib:
            if "Z2Dateiname_rel" in nwag_root[j].attrib:
                z2fahrzeugdateiname = nwag_root[j].attrib["Z2Dateiname_rel"]
            if "FahrzeugInfo" in nwag_root[j][0].tag:
                if "IDHaupt" in nwag_root[j][0].attrib:
                    z3fahrzeughauptid = nwag_root[j][0].attrib["IDHaupt"]
                if "IDNeben" in nwag_root[j][0].attrib:
                    z3fahrzeugnebenid = nwag_root[j][0].attrib["IDNeben"]
                if "Datei" in nwag_root[j][0][0].tag:
                    if "Z3Dateiname_rel" in nwag_root[j][0][0].attrib:
                        z3fahrzeugdateiname = nwag_root[j][0][0].attrib[
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
    )
