#!/bin/bash
# Javis A.I --JDC
#youtube.com/suyash Jawale
#not for illegel use
#Made By Suyash Jawale.
if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
	echo ""
else
	echo "No Internet Connection"
	exit 1
fi
pkg install python -y >/dev/null 2>&1
pkg install wget -y >/dev/null 2>&1
pkg install ffmpeg -y >/dev/null 2>&1
pkg install termux-api -y >/dev/null 2>&1

command -v python > /dev/null 2>&1 || { echo >&2 "Python not installed"; exit 1; }
command -v wget > /dev/null 2>&1 || { echo >&2 "Wget not installed"; exit 1; }
command -v ffmpeg > /dev/null 2>&1 || { echo >&2 "Python Not Installed"; exit 1; }
python hello.py
