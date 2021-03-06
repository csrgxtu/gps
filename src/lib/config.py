#!/usr/bin/env python
# coding=utf8
# Author: Archer Reilly
# Date: 07/Dec/2014
# File: config.py
# Desc: configuration file, set some constant vars that will
# be used in this project.
#
# Produced By CSRGXTU
# from os import getcwd
from os.path import dirname

# ROOT = getcwd() + '/'
ROOT = dirname(__file__) + '/../'

# contains the top n IP one ip per line from fast to slow
# TOP_IP_FILE = "/home/archer/Documents/gps/src/static/top.txt"
TOP_IP_FILE = ROOT + 'static/top.txt'

# log file contains logs of the search behaviour
# LOG_FILE = "/home/archer/Documents/gps/src/static/log.txt"
LOG_FILE = ROOT + 'static/log.txt'

# IP_FILE contains available ip seperated by |
# IP_FILE = "/home/archer/Documents/gps/src/static/ip.txt"
IP_FILE = ROOT + 'static/ip.txt'

# CACERT_FILE contains certification information used by checkip.py
# CACERT_FILE = "/home/archer/Documents/gps/src/static/cacert.pem"
CACERT_FILE = ROOT + 'static/cacert.pem'

# IP_TMP_OK_FILE contains temp ok ips
# IP_TMP_OK_FILE = "/home/archer/Documents/gps/src/static/ip_tmpok.txt"
IP_TMP_OK_FILE = ROOT + 'static/ip_tmpok.txt'

# IP_TMP_ERR_FILE contains temp error ips
# IP_TMP_ERR_FILE = "/home/archer/Documents/gps/src/static/ip_tmperror.txt"
IP_TMP_ERR_FILE = ROOT + 'static/ip_tmperror.txt'

# EXTRA_IP_FILE used by checkip.py
# EXTRA_IP_FILE = "/home/archer/Documents/gps/src/static/extraip.txt"
EXTRA_IP_FILE = ROOT + 'static/extraip.txt'
