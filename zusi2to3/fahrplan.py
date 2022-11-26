#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from . import fahrzeug


def conv_fpn(
    z2pfad,
    z2fahrplandateiname_rel,
    st3_name,
    z3pfad,
    zielverzeichnis_rel,
    rekursionstiefe,
):
    seen_nrs = set()
    tfz_ng = []
    wag_ng = []

    fahrplanname = os.path.splitext(os.path.basename(z2fahrplandateiname_rel))[0]
    z2fahrplandateiname_abs = os.path.join(z2pfad, "Strecken", z2fahrplandateiname_rel)
    z3fahrplandateiname_rel = os.path.join(
        "Timetables", zielverzeichnis_rel, fahrplanname + ".fpn"
    )
    z3fahrplandateiname_abs = os.path.join(z3pfad, z3fahrplandateiname_rel)
    treetfz = ET.parse("tfz.xml")
    ntfz_root = treetfz.getroot()
    treewag = ET.parse("wagen.xml")
    nwag_root = treewag.getroot()

    with open(z2fahrplandateiname_abs, "r", encoding="iso-8859-1") as ffpn:
        print(
            f"{z2fahrplandateiname_abs} -> {z3fahrplandateiname_abs}", file=sys.stderr
        )
        ffpn.readline()

        nfpn_root = ET.Element("Zusi")
        treefpn = ET.ElementTree(nfpn_root)
        ET.SubElement(
            nfpn_root,
            "Info",
            {"DateiTyp": "Fahrplan", "Version": "A.1", "MinVersion": "A.1"},
        )
        nfpn_fahrplan = ET.SubElement(
            nfpn_root,
            "Fahrplan",
            {
                "AnfangsZeit": datetime.strftime(
                    datetime.strptime(ffpn.readline().strip(), "%Y-%m-%d  %H:%M:%S"),
                    "%Y-%m-%d %H:%M:%S",
                ),
                "trnDateien": "1",
            },
        )
        ET.SubElement(
            nfpn_fahrplan,
            "BefehlsKonfiguration",
            {"Dateiname": r"Signals\Deutschland\Befehle\408_2015.authority.xml"},
        )
        ET.SubElement(nfpn_fahrplan, "Begruessungsdatei")
        while z2zugdateiname_rel := ffpn.readline():
            z2zugdateiname_abs = os.path.join(
                os.path.dirname(z2fahrplandateiname_abs),
                z2zugdateiname_rel.strip().replace("\\", os.sep),
            )
            with open(
                z2zugdateiname_abs,
                "r",
                encoding="iso-8859-1",
            ) as f2:
                f2.readline()  # Zusi-Version
                orig_zugnr = f2.readline().strip()
                zugnr = orig_zugnr
                i = 1
                while zugnr in seen_nrs:
                    zugnr = f"{orig_zugnr}_{i}"
                    i += 1
                seen_nrs.add(zugnr)
                gattung = f2.readline().strip()
                z3zugdateiname = gattung + zugnr + ".trn"
                z3zugdateiname_rel = os.path.join(
                    "Timetables", zielverzeichnis_rel, fahrplanname, z3zugdateiname
                )
                z3zugdateiname_abs = os.path.join(z3pfad, z3zugdateiname_rel)
                nzug_root = ET.Element("Zusi")
                treezug = ET.ElementTree(nzug_root)
                ET.SubElement(
                    nzug_root,
                    "Info",
                    {"DateiTyp": "Zug", "Version": "A.1", "MinVersion": "A.1"},
                )
                nzug_zug = ET.SubElement(nzug_root, "Zug", {})
                nzug_zug.attrib["Gattung"] = gattung
                nzug_zug.attrib["Nummer"] = zugnr
                bremsstellung = f2.readline().strip()  # TODO Bremsstellung
                if bremsstellung == "G":
                    nzug_zug.attrib["BremsstellungZug"] = "1"
                elif bremsstellung == "P":
                    nzug_zug.attrib["BremsstellungZug"] = "2"
                elif bremsstellung == "PMg":
                    nzug_zug.attrib["BremsstellungZug"] = "3"
                elif bremsstellung == "R":
                    nzug_zug.attrib["BremsstellungZug"] = "4"
                elif bremsstellung == "RMg":
                    nzug_zug.attrib["BremsstellungZug"] = "5"
                if "deko" in z2zugdateiname_rel.lower():
                    nzug_zug.attrib["Dekozug"] = "1"
                    nzug_zug.attrib["FahrplanGruppe"] = "Deko"
                elif gattung in [
                    "AZ",
                    "D",
                    "EC",
                    "Expr D",
                    "F",
                    "IC",
                    "ICE",
                    "TEE",
                    "THA",
                ]:
                    nzug_zug.attrib["FahrplanGruppe"] = "Fernverkehr"
                elif gattung in ["E", "N", "RB", "RE", "RE1", "RE2", "RE5", "RE7"]:
                    nzug_zug.attrib["FahrplanGruppe"] = "Nahverkehr"
                elif gattung in ["DG", "NG", "SG", "TEEM"]:
                    nzug_zug.attrib["FahrplanGruppe"] = "Güterverkehr"
                else:
                    nzug_zug.attrib["FahrplanGruppe"] = "Sonstiges"
                nzug_fahrzeuge_minus_1 = int(f2.readline())
                fahrzeug_gedreht = [f2.readline().strip() == "-1"]
                f2.readline()  # Reserviert für spätere Funktionen
                zugvMax = float(f2.readline().replace(",", ".")) / 3.6
                if zugvMax > 0.0:
                    nzug_zug.attrib["spZugNiedriger"] = str(zugvMax)
                f2.readline()  # max. Beschleunigung bei Autopilot/AFB
                fahrzeugliste = [f2.readline().strip()]
                while f2.readline().strip() != "#IF":  # PZB-Modus
                    pass
                nzug_zug.attrib["Prio"] = f2.readline().strip()
                f2.readline()  # Einsatzreferenz
                f2.readline()  # Treibstoffvorrat
                f2.readline()  # reserviert
                f2.readline()  # reserviert
                f2.readline()  # Zugtyp
                nzug_zug.attrib["Zuglauf"] = f2.readline().strip()
                f2.readline()  # Türsystem
                nzug_zug.attrib["MBrh"] = "1.00"
                nzug_zug.attrib["Rekursionstiefe"] = str(rekursionstiefe)
                nzug_zug.attrib[
                    "Buchfahrplandll"
                ] = r"_InstSetup\lib\timetable\Buchfahrplan_DB_1979.dll"
                # nzug_zug.attrib["Buchfahrplandll"] = r"_InstSetup\lib\timetable\Buchfahrplan_DB_2006.dll"
                ET.SubElement(
                    nzug_zug,
                    "Datei",
                    {"Dateiname": z3fahrplandateiname_rel, "NurInfo": "1"},
                )
                for i in range(6):
                    f2.readline()  # reserviert für spätere Funktionen
                erster_eintrag = True
                hat_zugwende = False
                while (betrst := f2.readline().strip()) != "#IF":
                    if (
                        not hat_zugwende
                    ):  # Die Daten nach einer Zugwende werden verworfen, da Zusi 3 damit nicht umgehen kann.
                        nzug_fahrplaneintrag = ET.SubElement(
                            nzug_zug, "FahrplanEintrag", {"Betrst": betrst}
                        )
                        ankunft = f2.readline().strip()
                        if not "1899" in ankunft:
                            nzug_fahrplaneintrag.attrib["Ank"] = datetime.strftime(
                                datetime.strptime(ankunft, "%Y-%m-%d  %H:%M:%S"),
                                "%Y-%m-%d %H:%M:%S",
                            )
                        nzug_fahrplaneintrag.attrib["Abf"] = datetime.strftime(
                            datetime.strptime(
                                f2.readline().strip(), "%Y-%m-%d  %H:%M:%S"
                            ),
                            "%Y-%m-%d %H:%M:%S",
                        )
                        while (gleis := f2.readline().strip()) != "#":
                            ET.SubElement(
                                nzug_fahrplaneintrag,
                                "FahrplanSignalEintrag",
                                {"FahrplanSignal": gleis},
                            )
                            if erster_eintrag:
                                erster_eintrag = False
                                nzug_zug.attrib[
                                    "FahrstrName"
                                ] = f"Aufgleispunkt -> {betrst} {gleis}"
                        while (spezialaktion := f2.readline().strip()) != "#":
                            if spezialaktion in ["1", "2"]:
                                print(
                                    f'{nzug_zug.attrib["Gattung"]} {nzug_zug.attrib["Nummer"]}: Zugwende {nzug_fahrplaneintrag.attrib["Betrst"]}',
                                    file=sys.stderr,
                                )
                                hat_zugwende = True
                            f2.readline()
                            f2.readline()  # reserviert für spätere Funktionen
                        f2.readline()  # reserviert für spätere Funktionen
                f2.readline()  # reserviert für spätere Funktionen

                for i in range(nzug_fahrzeuge_minus_1):
                    fahrzeugliste.append(f2.readline().strip())
                    fahrzeug_gedreht.append(f2.readline() == "1")
                    f2.readline()

                nzug_fahrzeugvarianten = ET.SubElement(
                    nzug_zug,
                    "FahrzeugVarianten",
                    {"Bezeichnung": "default", "ZufallsWert": "1"},
                )

                lokgefunden = True
                for i in range(len(fahrzeugliste)):
                    fahrzeuggefunden = False
                    z3fahrzeughauptid = "1"
                    z3fahrzeugnebenid = "1"
                    z2z3gedreht = False
                    z3saschaltung = "0"
                    if ".lok" in str(fahrzeugliste[i]).lower():
                        for j in range(len(ntfz_root)):
                            if "Fahrzeug" in ntfz_root[j].tag:
                                if "Z2Dateiname_rel" in ntfz_root[j].attrib:
                                    if (
                                        ntfz_root[j]
                                        .attrib["Z2Dateiname_rel"]
                                        .encode("ascii")
                                        .lower()
                                        == str(fahrzeugliste[i]).encode("ascii").lower()
                                    ):
                                        if "FahrzeugInfo" in ntfz_root[j][0].tag:
                                            if "IDHaupt" in ntfz_root[j][0].attrib:
                                                z3fahrzeughauptid = ntfz_root[j][
                                                    0
                                                ].attrib["IDHaupt"]
                                            if "IDNeben" in ntfz_root[j][0].attrib:
                                                z3fahrzeugnebenid = ntfz_root[j][
                                                    0
                                                ].attrib["IDNeben"]
                                            if "SASchaltung" in ntfz_root[j][0].attrib:
                                                z3saschaltung = ntfz_root[j][0].attrib[
                                                    "SASchaltung"
                                                ]
                                            if "Z2Z3Gedreht" in ntfz_root[j][0].attrib:
                                                z2z3gedreht = (
                                                    ntfz_root[j][0].attrib[
                                                        "Z2Z3Gedreht"
                                                    ]
                                                    == "1"
                                                )
                                            if "Datei" in ntfz_root[j][0][0].tag:
                                                if (
                                                    "Z3Dateiname_rel"
                                                    in ntfz_root[j][0][0].attrib
                                                ):
                                                    z3fahrzeugdateiname = ntfz_root[j][
                                                        0
                                                    ][0].attrib["Z3Dateiname_rel"]
                                        fahrzeuggefunden = True
                        if fahrzeuggefunden != True:
                            lokgefunden = False
                            if str(fahrzeugliste[i]) not in tfz_ng:
                                tfz_ng.append(str(fahrzeugliste[i]))
                            if "elektroloks" in str(fahrzeugliste[i]).lower():
                                z3fahrzeugdateiname = r"RollingStock\Deutschland\Epoche4\Elektroloks\BRD\120\120.rv.fzg"
                                z3saschaltung = "2"
                            elif "elektrotriebwagen" in str(fahrzeugliste[i]).lower():
                                z3fahrzeugdateiname = r"RollingStock\Deutschland\Epoche4\Elektroloks\BRD\120\120.rv.fzg"
                                z3saschaltung = "2"
                            elif "steuerwagen" in str(fahrzeugliste[i]).lower():
                                z3fahrzeugdateiname = r"RollingStock\Deutschland\Epoche5\Reisezugwagen\FV-Steuerwagen\Bimdzf269.rv.fzg"
                            else:
                                z3fahrzeugdateiname = r"RollingStock\Deutschland\Epoche3\Dieselloks\BRD\V160_Familie\218\218.rv.fzg"
                    else:
                        for j in range(len(nwag_root)):
                            if "Fahrzeug" in nwag_root[j].tag:
                                if "Z2Dateiname_rel" in nwag_root[j].attrib:
                                    if (
                                        nwag_root[j]
                                        .attrib["Z2Dateiname_rel"]
                                        .encode("ascii")
                                        .lower()
                                        == str(fahrzeugliste[i]).encode("ascii").lower()
                                    ):
                                        if "FahrzeugInfo" in nwag_root[j][0].tag:
                                            if "IDHaupt" in nwag_root[j][0].attrib:
                                                z3fahrzeughauptid = nwag_root[j][
                                                    0
                                                ].attrib["IDHaupt"]
                                            if "IDNeben" in nwag_root[j][0].attrib:
                                                z3fahrzeugnebenid = nwag_root[j][
                                                    0
                                                ].attrib["IDNeben"]
                                            if "Z2Z3Gedreht" in ntfz_root[j][0].attrib:
                                                z2z3gedreht = (
                                                    ntfz_root[j][0].attrib[
                                                        "Z2Z3Gedreht"
                                                    ]
                                                    == "1"
                                                )
                                            if "Datei" in nwag_root[j][0][0].tag:
                                                if (
                                                    "Z3Dateiname_rel"
                                                    in nwag_root[j][0][0].attrib
                                                ):
                                                    z3fahrzeugdateiname = nwag_root[j][
                                                        0
                                                    ][0].attrib["Z3Dateiname_rel"]
                                        fahrzeuggefunden = True
                        if fahrzeuggefunden != True:
                            if str(fahrzeugliste[i]) not in wag_ng:
                                wag_ng.append(str(fahrzeugliste[i]))
                            z3fahrzeugdateiname = fahrzeug.conv_wagen(
                                z2pfad,
                                fahrzeugliste[i],
                                z3pfad,
                                r"Deutschland\Zusi2_Fahrzeuge",
                            )

                    nzug_fzginfo = ET.SubElement(
                        nzug_fahrzeugvarianten,
                        "FahrzeugInfo",
                        {"IDHaupt": z3fahrzeughauptid, "IDNeben": z3fahrzeugnebenid},
                    )
                    if z3saschaltung != "0":
                        nzug_fzginfo.attrib["SASchaltung"] = z3saschaltung
                    if fahrzeug_gedreht[i] ^ z2z3gedreht:
                        nzug_fzginfo.attrib["Gedreht"] = "1"
                    ET.SubElement(
                        nzug_fzginfo,
                        "Datei",
                        {"Dateiname": z3fahrzeugdateiname},
                    )

            f2.close
            os.makedirs(os.path.dirname(z3zugdateiname_abs), exist_ok=True)
            ET.indent(treezug, space=" ", level=0)
            treezug.write(
                z3zugdateiname_abs, encoding="UTF-8-SIG", xml_declaration=True
            )

            # if not ("deko" in z2zugdateiname_rel.lower()):
            if lokgefunden:
            # if True:
                nfpn_zug = ET.SubElement(nfpn_fahrplan, "Zug")
                # print(f"{z2zugdateiname_abs} -> {z3zugdateiname_abs}", file=sys.stderr)
                ET.SubElement(nfpn_zug, "Datei", {"Dateiname": z3zugdateiname_rel})
        nfpn_strmodul = ET.SubElement(nfpn_fahrplan, "StrModul")
        ET.SubElement(nfpn_strmodul, "Datei", {"Dateiname": st3_name})
        ET.SubElement(nfpn_strmodul, "p")
        ET.SubElement(nfpn_strmodul, "phi")
        ET.SubElement(nfpn_fahrplan, "UTM")
        ET.indent(treefpn, space=" ", level=0)
        os.makedirs(os.path.dirname(z3fahrplandateiname_abs), exist_ok=True)
        treefpn.write(
            z3fahrplandateiname_abs, encoding="UTF-8-SIG", xml_declaration=True
        )
        # for i in range(len(tfz_ng)):
        #     print("Fahrzeug " + tfz_ng[i] + " nicht in Übersetzungstabelle gefunden.")
        # for i in range(len(wag_ng)):
        #     print("Fahrzeug " + wag_ng[i] + " nicht in Übersetzungstabelle gefunden.")
    ffpn.close
