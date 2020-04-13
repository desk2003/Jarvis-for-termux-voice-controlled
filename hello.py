import subprocess
import concurrent.futures
import requests
import threading
import re
from bs4 import BeautifulSoup
from datetime import datetime
import os
import time
import json
from datetime import date
import urllib.request
now=datetime.now()

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def intro():
    proc=subprocess.Popen(["termux-media-player play jarviss.mp3"],stdout=subprocess.PIPE,shell=True)
    (out,err)=proc.communicate()

def baseintro():
    track=now.hour
    if track>=5 and track<11:
        speech="Good morning sir. "
    elif track>=11 and track<18:
        speech="Good Afternoon sir. "
    elif track>=18 and track<20:
        speech="Good evening sir. "
    else:
        speech="Hello sir. "
    speak(f"\n{speech}Its {now.strftime('%d %B, %Y')} and current time is {now.strftime('%I:%M %p')} . ")


def speak(string):
    print(color.BOLD+color.CYAN+f"{string.title()}"+color.END)
    string=string.replace("\n","")
    os.system(f"termux-tts-speak {string}")

def say(dargs='Jarvis is listening....'):
    proc=subprocess.Popen(["termux-dialog speech -i\""+dargs+"\""],stdout=subprocess.PIPE,shell=True)
    (out,err)=proc.communicate()
    out=out.decode("utf-8")
    res=json.loads(out)
    string=res['text']
    string=string.lower()
    return string

def youtube():
    speak("\nOpening youtube , is there anything i can search for ")
    string2=say()
    if "no" in string2:
        os.system("termux-open-url 'https://youtube.com'")
    else:        
        string2=string2.replace(" ","+")
        os.system(f"termux-open-url 'https://youtube.com/results?search_query={string2}'")
    os.system("termux-notification -t \"Youtube is running\" --button1 \"close\" --button1-action \"am start --user 0 -n com.termux/com.termux.app.TermuxActivity;termux-notification-remove 2;python client.py\" --id 2 --ongoing")
    speak("\nI guess this might help")
        

def instagram():
    os.system("termux-open-url 'https://www.instagram.com'")
    os.system("termux-notification -t \"Instgarm is running\" --button1 \"close\" --button1-action \"am start --user 0 -n com.termux/com.termux.app.TermuxActivity;termux-notification-remove 2;python client.py\" --id 2 --ongoing")
    

def battery(mainval='no'):
    procbat=subprocess.Popen(["termux-battery-status"],stdout=subprocess.PIPE,shell=True)
    (outbat,err)=procbat.communicate()
    outbat=outbat.decode("utf-8")
    res = json.loads(outbat)
    if mainval=="yes":
        return round(res['temperature'],0),res['percentage'],res['health']
    else:
        return f"\n\nThe system temperature is {round(res['temperature'])} degree celcius and power is {res['percentage']} percent , and thats {res['health']} . "

def authenticate():
    procauth=subprocess.Popen(["termux-fingerprint"],stdout=subprocess.PIPE,shell=True)
    (outauth,err)=procauth.communicate()
    string=str(outauth)
    if string.find("SUCCESS")!=-1:
        return 1
    return 0

def listcontact(name):
    namelist=name.split("call")
    if (len(namelist)==2 and namelist[1]=="") or len(namelist)==1:
        speak("\nSir who do i call ")
        realname=say()
    else:
        realname=namelist[1].strip()
    print(realname)

    procaa=subprocess.Popen(["termux-contact-list"],stdout=subprocess.PIPE,shell=True)
    (outaa,err)=procaa.communicate()
    outaa=str(outaa)
    lists=re.findall(r'"(.*?)"', outaa)
    seen=[]
    for i in lists:
        if i!="name" and i!="number":
            seen.append(i.lower())
    data={}
    for i in range(len(seen)):
        if seen[i].find(realname)!=-1:
           data[seen[i]]=seen[i+1]
    res=not bool(data)
    if "True" in str(res):
        speak("\n\nContact not found")
        return 0
    else:
        if len(data)!=1:
            string="termux-dialog radio -v \""
            for key,value in data.items():
                string+=key+" @ "+value+","
            string=string[:-1]
            string+="\""
            proces=subprocess.Popen([string],stdout=subprocess.PIPE,shell=True)
            (outs,err)=proces.communicate()
            outs=str(outs)
            outs=outs[:-22]
            mainstr=outs.split("@")
            mainnumber=mainstr[1].replace(" ","")
        else:
            mainnumber=data[realname]
        os.system("termux-telephony-call "+mainnumber)
        os.system("termux-notification -t \"Resume Jarvis - Call function was running\" --button1 \"start\" --button1-action \"am start --user 0 -n com.termux/com.termux.app.TermuxActivity;termux-notification-remove 2;python client.py\" --id 2 --ongoing")
        return 1
        

def init():
    data={}
    f = open("status.json","r")
    string=f.read()
    data=json.loads(string)
    f.close()
    if data['registered']=="0":
        procinit=subprocess.Popen(["termux-dialog -t 'Enter your name'"],stdout=subprocess.PIPE,shell=True)
        (outinit,err)=procinit.communicate()
        string=str(outinit)
        string=string[:-7]
        string=string[31:]
        data['username']=string

        procinit1=subprocess.Popen(["termux-dialog date -t 'Enter Birth Date'"],stdout=subprocess.PIPE,shell=True)
        (outinit1,err)=procinit1.communicate()
        string=str(outinit1)
        string=string[:-7]
        string=string[31:]
        data['Birthdate']=string

        if data['username']=="" or data['Birthdate']=="":
            speak("\n\nSorry Something went wrong")
            exit(0)
        else:
            data['registered']="1"
            json_object= json.dumps(data,indent = 4)
            with open("status.json", "w") as outfile:
                outfile.write(json_object)
            speak("\n\nThank you "+data['username']+".")
            intro()

def google():
    speak("\nOpening google , is there anything i can search for ")
    string2=say()
    if "no" in string2:
        os.system("termux-open-url 'https://google.com'")
    else:
        string2=string2.replace(" ","+")
        os.system("termux-open-url 'https://google.com/search?q="+string2+"'")
        os.system("termux-notification -t \"Chrome is running\" --button1 \"close\" --button1-action \"am start --user 0 -n com.termux/com.termux.app.TermuxActivity;termux-notification-remove 2;python client.py\" --id 2 --ongoing")              
        speak("i guess, this might help")


def torch(argz):
    os.system("termux-torch "+argz) 

def whatsapp():
    os.system("am start --user 0 -n com.whatsapp/com.whatsapp.Main")
    os.system("termux-notification -t \"Whatsapp is running\" --button1 \"close\" --button1-action \"am start --user 0 -n com.termux/com.termux.app.TermuxActivity;termux-notification-remove 2;python client.py\" --id 2 --ongoing")

def proxy():
    os.system("am start --user 0 -n com.fast.free.unblock.secure.vpn/com.signallab.secure.activity.MainActivity")
    os.system("termux-notification -t \"Server Started - Return to termux\" --button1 \"Return\" --button1-action \"am start --user 0 -n com.termux/com.termux.app.TermuxActivity;termux-notification-remove 2;python client.py\" --id 2 --ongoing")


def shazam():
    os.system("am start --user 0 -n com.shazam.android.lite/com.shazam.android.lite.ui.SplashActivity")
    os.system("termux-notification -t \"Shazam is running\" --button1 \"Close\" --button1-action \"am start --user 0 -n com.termux/com.termux.app.TermuxActivity;termux-notification-remove 2;python client.py\" --id 2 --ongoing")


def dimmer():
    os.system("am start --user 0 -n com.genie.dimmer/com.genie.dimmer.MainActivity")

def torrent(news):
    os.system(f"termux-open *{news}*")
    os.system("termux-notification -t \"Torrent is running\" --button1 \"Close\" --button1-action \"am start --user 0 -n com.termux/com.termux.app.TermuxActivity;termux-notification-remove 2;python client.py\" --id 2 --ongoing")


def cam():
    os.system("am start --user 0 -n com.lenovo.gallery/com.android.camera.CameraLauncher")
    os.system("termux-notification -t \"Camera is running\" --button1 \"Close\" --button1-action \"am start --user 0 -n com.termux/com.termux.app.TermuxActivity;termux-notification-remove 2;python client.py\" --id 2 --ongoing")


def newclimate(pass_args):
    lists=pass_args.split(" ")
    params= {
            'apiKey': 'd522aa97197fd864d36b418f39ebb323',
            'format': 'json',
            'geocode': lists[1],
            'language': 'en-US',
            'units':'m'
            }
    r2 =requests.get(url='https://api.weather.com/v2/turbo/vt1observation',params=params)
    r2_data = r2.json()
    humidity = r2_data["vt1observation"]["humidity"]
    temperature = r2_data["vt1observation"]["temperature"]
    windspeed = r2_data["vt1observation"]["windSpeed"]
    phrase = r2_data["vt1observation"]["phrase"]
    uvspeed = r2_data["vt1observation"]["uvDescription"]
    return f"\n\nTemperature in {lists[0]} is {temperature} degree celcius with winds flowing at {windspeed} km per hr and humidity is {humidity} percent with {uvspeed} uv index and climate feels like {phrase} . "


def tendays():
    string=requests.get("https://www.goodreturns.in/src/gold_silver_rates.php?cmd=gold_rates_4_graph&city=pune&callback=jQuery19106600872184738995_1585913754501&_=1585913754502").text
    string=string[string.find("[")+1:string.rfind("]")]
    val=0
    for i in range(0,10):
        val=string.rfind("{",0,val)
    string=string[val:]
    string=string[1:-1]
    lists=string.split("},{")
    print("\n"+color.BOLD+color.PURPLE+"    Date      22carat  24carat"+color.END)
    for i in lists:
        string=f"{{{i}}}"
        data=json.loads(string)
        print(color.YELLOW,color.BOLD,data['on_date']," ",data['22_c_10g']," ",data['24_c_10g'],color.END)

def rate22():
    res=requests.get("https://www.goodreturns.in/gold-rates/pune.html")
    soup=BeautifulSoup(res.text,'html.parser')
    tab=soup.find('div',class_='gold_silver_table')
    table=tab.find('table')
    tr=table.find_all('tr')
    lists=[]
    for i in tr:
        td=i.find_all('td')
        for j in td:
            string=str(j.text.encode("utf-8"))
            if "xe2" in string:
                string=str(string[string.find(" ")+1:])
                lists.append(string.replace("'",""))
                break
    rate=lists[2]
    return f"\n\nGold rate for 22 carat gold is {rate} rupees "

def rate24():
    res=requests.get("https://www.goodreturns.in/gold-rates/pune.html")
    soup=BeautifulSoup(res.text,'html.parser')
    tab=soup.find_all('div',class_='gold_silver_table')
    table=tab[1].find('table')
    tr=table.find_all('tr')
    lists=[]
    for i in tr:
        td=i.find_all('td')
        for j in td:
            string=str(j.text.encode("utf-8"))
            if "xe2" in string:
                string=str(string[string.find(" ")+1:])
                lists.append(string.replace("'",""))
                break
    rate=lists[2]
    return f"and for 24 carat gold is {rate} rupees . "



def findmovie(mname):
    mname=mname.replace(" ","+")  
    res=requests.get("https://ytsmovies.to/?s="+mname)
    soup=BeautifulSoup(res.text,'html.parser')
    div=soup.find('div',class_='movies-list movies-list-full')
    a=div.find_all('a')
    for i in a:
        if i.text.find("HD")!=-1:
            return i['href']

def findlink(mname):
    first=findmovie(mname)
    res=requests.get(first)
    soup=BeautifulSoup(res.text,'html.parser')
    mdiv=soup.find_all('div',class_='modal-torrent')
    a=mdiv[1].find('a')
    return a['href']



def mfrate():
    url = 'https://www.moneycontrol.com/mutual-funds/nav/sbi-banking-financial-services-fund-regular-plan/MSB1099'
    response= requests.get(url)
    page=response.text
    soup=BeautifulSoup(page,'html.parser')
    tab=soup.find('div',class_='leftblok')
    span=tab.find_all('span')
    per=span[4].text
    per=per[:-1]
    dates=tab.find('div',class_='grayvalue').text
    dates=dates[1:-1]
    crate=float(per)
    trate=crate
    f=open("status.json","r")
    string=f.read()
    res=json.loads(string)
    yrate=res['ymf']
    ydate=res['ydate']
    yrate=float(yrate)
    tdate=date.today()
    if str(tdate)!=str(ydate):
        if yrate==crate:
            speech="\nThere is no change in the value."
        elif yrate>crate:
            speech=f"\nValue has dropped by {(yrate-crate)} percent , Yesterday the value was {yrate} percent. "
        else:
            speech=f"\nValue has hiked by {crate-yrate} percent ,Yesterday the value was {yrate} percent."
    else:
        speech=""
    res['ydate']=str(tdate)
    res['ymf']=str(crate)
    f.close()
    json_object = json.dumps(res, indent = 4)
    with open("status.json", "w") as outfile:
        outfile.write(json_object)
    return f"\nThe mutual fund resides at {trate} percent {dates} . {speech}"


def playsong(song):
    sstring='find /sdcard/ -iname "*'+song+'*"'
    procsong=subprocess.Popen([sstring],stdout=subprocess.PIPE,shell=True)
    (songout,err)=procsong.communicate()
    songout=songout.decode("utf-8")
    songout=songout.replace(" ","\ ")
    if len(songout)!=0:
        os.system(f"termux-media-player play {songout}")
    else:
        url = f"https://www.youtube.com/results?search_query={song}"
        response = requests.get(url)
        page=response.content
        page=str(page)
        start='<a aria-hidden="true"  href="/'
        page=page[page.find(start)+len(start):]
        end='" class=" yt-uix-sessionlink'
        lens=page.find(end)
        page=page[:lens]
        string=f"youtube-dl -f bestaudio https://www.youtube.com/{page}"
        page=page[8:]
        os.system(string)
        os.system(f"termux-media-player play *{page}*")
    os.system(f"termux-notification -t \"{song.title()}\" --button2 Pause --button2-action \"termux-media-player pause\" --button3 Stop --button3-action \"termux-media-player stop;python client.py;termux-notification-remove 2\" --id 2 --button1 Play --button1-action \"termux-media-player play\" --ongoing")



def playvideo(song):
    url = f"https://www.youtube.com/results?search_query={song}"
    response = requests.get(url)
    page=response.content
    page=str(page)
    start='<a aria-hidden="true"  href="/'
    page=page[page.find(start)+len(start):]
    end='" class=" yt-uix-sessionlink'
    lens=page.find(end)
    page=page[:lens]
    os.system(f"termux-open-url 'https://www.youtube.com/{page}'")
    os.system("termux-notification -t \"Youtube is running\" --button1 \"close\" --button1-action \"am start --user 0 -n com.termux/com.termux.app.TermuxActivity;termux-notification-remove 2;python client.py\" --id 2 --ongoing")                                                  


                 
def icorona(qry="all"):
    q=qry.lower()
    res=requests.get("https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India")
    page=res.text
    soup=BeautifulSoup(page,'html.parser')
    table=soup.find('table',class_='wikitable plainrowheaders sortable mw-collapsible')
    tr=table.find_all('tr')
    mlist=[]
    for i in tr:
        string=i.text
        lists=string.split("\n\n")
        cdata=[]
        for j in lists:
            cdata.append(j.strip())
        mlist.append(cdata)
    del mlist[0]
    del mlist[1]
    for i in mlist:
        if len(i)==6:
            if i[1].lower()==q or q=="all":
                return f"{i[1]} has {i[2]} active Cases with {i[3]} deaths and {i[4]} humans recovered. \nTotal cases in {i[1]} are {i[5]}.\n\n"


def corona(qry="all"):
    q=qry.lower()
    res=requests.get("https://www.worldometers.info/coronavirus/")
    page=res.content
    mlist=[]
    soup=BeautifulSoup(page,'html.parser')
    table=soup.find('table',id='main_table_countries_today')
    tr=table.find_all('tr')
    for i in tr:
        data=i.find_all("td")
        cdata=[]
        for j in data:
            cdata.append(j.text.strip())
        mlist.append(cdata)
    del mlist[0]
    for i in mlist:
        if i[0].lower()==q or q=="all":
            return f"\n{i[0]} has {i[6]} active cases with {i[3]} deaths and {i[5]} humans recovered.\nTotal Cases in {i[0]} are {i[1]}.\n\n"



def maharashtracorona(qry="all"):
    q=qry.lower()
    res=requests.get("https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Maharashtra")
    page=res.text
    soup=BeautifulSoup(page,'html.parser')
    table=soup.find('table',class_='wikitable plainrowheaders sortable')
    tr=table.find_all('tr')
    mlist=[]
    for i in tr:
        string=i.text
        lists=string.split("\n\n")
        cdata=[]
        for j in lists:
            cdata.append(j.strip())
        mlist.append(cdata)
                        
    del mlist[0]
    for i in mlist:
        if len(i)==5:
            if i[0].lower()==q or q=="all":
                pct=int(i[1])-(int(i[3])+int(i[2]))
                return f"{i[0]} has {pct} active cases with {i[3]} deaths and {i[2]} humans recovered.\nTotal Cases in {i[0]} are {i[1]}.\n\n"



def wait():
    os.system("termux-notification -t \"Resume Jarvis\" --button1 \"start\" --button1-action \"am start --user 0 -n com.termux/com.termux.app.TermuxActivity;termux-notification-remove 2;python client.py\" --id 2 --ongoing")


def getinput(argss):
    getproc=subprocess.Popen([f"termux-dialog text -t \"{argss}\""],stdout=subprocess.PIPE,shell=True)
    (getout,err)=getproc.communicate()
    getout=getout.decode("utf-8")
    data=json.loads(getout)
    return data['text']

def wakelock():
    os.system("termux-wake-lock")

def wakeunlock():
    os.system("termux-wake-unlock")

def volume():
    os.system("termux-volume music 200;termux-volume ring 200;termux-volume call 200;termux-volume system 200")

def bye(cond):
    speak(cond)
    os.system("termux-notification-remove 2")
    wakeunlock()
    exit(0)

def lighton():
    os.system("termux-torch on")

def lightoff():
    os.system("termux-torch off")


def printdetails(numberplate):
    data ={
            'vehicle_shrt_name':numberplate
        }
    url='http://www.rtovehicleinformation.com/rto-vehicle-information-maharashtra'
    x = requests.post(url, data=data)
    soup = BeautifulSoup(x.text,'html.parser')
    table=soup.find('table', id='divIncidents')
    val=table.find_all('td')
    details=[]
    i=0
    strr=""
    for link in val:
        if (i+1)%2==0 and i<16:
            strr+=link.text.replace('\n', ' ').strip()
            details.append(strr)
        else:
            strr=(link.text.replace('\n', ' ').strip())+" : "
        i+=1
    print("\n")
    for i in details:
        print(color.BOLD+color.YELLOW+i+color.END)


itext="""

    ___    ___   ______   _     _   _____   _____
   |_  |  / _ \  | ___ \ | |   | | |_   _| /  ___|
     | | / /_\ \ | |_/ / | |   | |   | |   \ `--.
     | | |  _  | |    /  \ |   | /   | |    `--. /
  /\_/ / | | | | | |\ \   \ \_/ /   _| |_  /\__/ /
 \____/  \_| |_/ \_| \_|   \___/    \___/  \____/
"""

ownertext="""
                 -- Made By JDC --
"""

if __name__=="__main__":
    try:
        urllib.request.urlopen('https://www.geeksforgeeks.org/')
        if authenticate()==1:
            os.system("clear")
            print("\n\n\n\t\t"+color.CYAN+color.BOLD+itext+color.END+"\n\n"+color.YELLOW+color.BOLD+"\t\t"+ownertext+color.END)
            wakelock()
            volume()
            init()
            baseintro()
            while 1:
                powval=battery("yes")
                if powval[0]>45 or powval[1]<15 or powval[2]!="GOOD":
                    batstring=battery()
                    bye(f"\nSir , it seems that the system integrity has been compromised . Issuing an immediate shutdown {batstring}. Thank you.")

                string=say("Say \"Jarvis...\"")
                print(color.GREEN+color.BOLD+f"\nYou said : {string}\n"+color.END)
                if any(x in string for x in ["jarvis","darvesh","nervous","john lewis","paris","service"]):
                    speak("how can i help you")
                    string2=say()
                    print(color.GREEN+color.BOLD+f"\nCommand : {string2}"+color.END)
                    if "open youtube" in string2:
                        youtube()
                        os.system("python server.py")
                    elif "launch camera" in string2:
                        cam()
                        os.system("python server.py")
                    elif "open google" in string2:
                        google()
                        os.system("python server.py")
                    elif "time" in string2:
                        baseintro()
                    elif "call" in string2:
                        callval=listcontact(string2)
                        if callval==1:
                            os.system("python server.py")
                    elif any(x in string2 for x in ["shutdown","bhai","bye"]):
                        bye("ok boss , This is jarvis signing off. ")
                    elif "open whatsapp" in string2:
                        whatsapp()
                        os.system("python server.py")
                    elif "count of" in string2:
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            f3=executor.submit(icorona,"maharashtra")
                            f2=executor.submit(maharashtracorona,"pune")
                            f1=executor.submit(corona,"india")
                        speak(f1.result()+f3.result()+f2.result())
                    elif "lights on" in string2:
                        lighton()
                    elif "find vehicle" in string2:
                        nums=getinput("Enter vehicle number")
                        if len(nums)>0:
                            printdetails(nums)
                        else:
                            speak("Invalid Number")
                    elif "open termux" in string2:
                        os.system("am start --user 0 -n com.termux/com.termux.app.TermuxActivity")
                    elif "lights off" in string2:
                        lightoff()
                    elif "battery status" in string2:
                        speak(battery())
                    elif "intoduce yourself" in string2:
                    	intro()
                    elif "temperature in pune" in string2:
                        speak(newclimate("pune 18.49,73.80"))
                    elif all(x in string2 for x in ["song","play"]):
                        string2=string2.replace("play","")
                        string2=string2.replace("song","")
                        if len(string2.strip())>2:
                            playsong(string2)
                            os.system("python server.py")
                        else:
                            speak("No song provided")
                    elif all(x in string2 for x in ["play","video"]):
                        string2=string2.replace("play","")
                        string2=string2.replace("video","")
                        print(string2)
                        if len(string2.strip())>2:
                            playvideo(string2)
                            os.system("python server.py")
                        else:
                            speak("No video provided")
                    elif "mutual fund" in string2:
                        speak(mfrate())
                    elif "gold rate" in string2:
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            f1=executor.submit(rate22)
                            f2=executor.submit(rate24)
                        speak(f1.result()+f2.result()+"\nThe ten days chart is mentioned below.")
                        tendays()
                    elif "find movie" in string2:
                        proxy()
                        os.system("python server.py")
                        one=getinput('Enter movie name')
                        if len(one)>0:
                            print("Downloading now....")
                            links=findlink(one)
                            os.system("wget "+links)
                            one=one.split(" ")
                            news=one[0].title()
                            torrent(news)
                            os.system("python server.py")
                        else:
                            speak("No movie provided")
                    elif "identify song" in string2:
                        shazam()
                        os.system("python server.py")
                    elif "night mode" in string2:
                        dimmer()
                    elif "open instagram" in string2:
                        instagram()
                        os.system("python server.py")
                    elif any(x in string2 for x in ["start the party","do it"]):
                        welcome()
                    elif any(x in string2 for x in ["wait","weight","sleep","sleep","stop","pause"]):
                        wait()
                        os.system("python server.py")
                elif any(x in string for x in ["bye","bhai","shutdown"]):
                    bye("Ok boss, This is jarvis signing off.")
                elif any(x in string for x in ["wait","weight","sleep","stop","pause"]):
                    wait()
                    os.system("python server.py")
                elif any(x in string for x in ["seth","shareit","say","start the party","do it"]):
                    welcome()
                time.sleep(6)
        else:
            speak("Fingerprint authentication failed")
    except Exception as e:
        print(color.YELLOW,color.BOLD,"\nNo Internet Connection\n",e,color.END)
