#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime

Z3ABS = r"C:\Users\Public\Documents\Zusi3"
Z2ABS = r"C:\Program Files (x86)\Zusi"
# Z3ABS = os.environ["ZUSI3_DATAPATH"]
# Z2ABS = os.environ["ZUSI2_DATAPATH"]
Z2REL = os.path.relpath(Z2ABS, Z3ABS)


def z2rel_to_z3rel(filename):
    return rf"Zusi2\{filename}"


def z2rel_to_abs(filename):
    return os.path.join(Z2ABS, filename).replace("\\", os.sep)


def z3rel_to_abs(filename):
    return os.path.join(Z3ABS, filename).replace("\\", os.sep)


def readfloat(f):
    line = f.readline()
    if line.startswith("#"):
        return None
    else:
        return float(line.strip().replace(",", "."))


def readfloatstr(f):
    line = f.readline()
    if line.startswith("#"):
        return None
    else:
        return line.strip().replace(",", ".")


def readposixtime(f):
    line = f.readline()
    if line.startswith("#"):
        return None
    else:
        posixtime = datetime.fromtimestamp(
            float(line.strip().replace(",", ".")) * 86400.0
        ) - (datetime(1970, 1, 1) - datetime(1899, 12, 30))
        return posixtime
