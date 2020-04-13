apt update && apt upgrade
pkg install termux-api
pkg install python 
pkg install wget
pkg install ffmpeg -y
pip install youtube-dl
pip install bs4
pip install --upgrade pip
command -v python > /dev/null 2>&1 || { echo >&2 "Python not installed"; exit 1; }
command -v wget > /dev/null 2>&1 || { echo >&2 "Wget not installed"; exit 1; }
command -v ffmpeg > /dev/null 2>&1 || { echo >&2 "Python Not Installed"; exit 1; }
command -v pip > /dev/null 2>&1 || { echo >&2 "Python Not Installed"; exit 1; }
