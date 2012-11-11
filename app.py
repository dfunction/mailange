# Imports
import redis
import hashlib
import argparse
import random
import base64
from flask import Flask
from flask import json
from flask import request

# Globals
app = Flask(__name__);
app.debug = True
r = None
characterSet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9','!','#','$','%','&#x26;',"'",'*','+','-','/','=','?','^','_','`','{','|','}','~','.','&#x22;','(',')',',',':',';','&#x3c;','&#x3e;','@','[','\\',']']
clearCharacterSet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9','!','#','$','%','&',"'",'*','+','-','/','=','?','^','_','`','{','|','}','~','.','"','(',')',',',':',';','<','>','@','[','\\',']']
fontFile = "courier-webfont.svg"
docHeader = '<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd" ><svg xmlns="http://www.w3.org/2000/svg"><metadata>Intelligible</metadata><defs>'
font = None
fontHeader = None
fontFaceHeader = None
glyphSet = []

# Routing
@app.route("/register", methods=["POST"])
def register():
    if ((request.form != None) and (request.form["email"] != "")):
        email = request.form["email"]
        sha1 = hashlib.sha1(email).hexdigest()
        if r.get(sha1) == None:
            if r.set(sha1, email):
                return json.dumps({"result":"Success", "hash" : sha1})
            else:
                return json.dumps({"result":"Failure: Redis Error"})
        else:
            return json.dumps({"result":"Success: Already Exists", "hash" : sha1})
    else:
        return json.dumps({"result":"Error: No email parameter specified"})
        

@app.route("/retrieve/<emailHash>", methods=["GET"])
def retrieve(emailHash):
    if (emailHash != ""):
        if r.get(emailHash) != None:
            return json.dumps({"result" : "Success", "font" : base64.b64encode(generateFont()), "email" : findEmail(r.get(emailHash))})
        else:
            return json.dumps({"result" : "Error, hash does not exist"})
    else:
        return json.dumps({"result":"Error, no email hash specified"})
    

# Functions
def init():
    global r, font
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    font = open(fontFile).read()
    generateFontHeader(font)
    generateFontFaceHeader(font)
    generateGlyphSet(font)

# at init functions
def generateFontHeader(font):
    global fontHeader
    HorizAdvXBegin = font.find('horiz-adv-x=',font.find('<font')) + 13
    HorizAdvXEnd = font.find(' >', HorizAdvXBegin) - 1
    HorizAdvX = font[HorizAdvXBegin:HorizAdvXEnd]
    fontHeader = '<font id="CourierRegular" horiz-adv-x="' + HorizAdvX + '" >'

def generateFontFaceHeader(font):
    global fontFaceHeader
    begin = font.find('<font-face')
    upmBegin = font.find('units', begin) + 14
    upmEnd = font.find('"', upmBegin)
    upm = font[upmBegin:upmEnd]
    
    ascBegin = font.find('ascent', begin) + 8
    ascEnd = font.find('"', ascBegin)
    asc = font[ascBegin:ascEnd]
    
    desBegin = font.find('descent', begin) + 9
    desEnd = font.find('"', desBegin)
    des = font[desBegin:desEnd] 
    
    fontFaceHeader = '<font-face units-per-em="' + upm + '" ascent="' + asc + '" descent="' + des + '" />'

def generateGlyphSet(font):
    for i in range(len(characterSet)):
        glyphBeginSearch = font.find('unicode="' + characterSet[i] + '"')
        glyphBegin = font.find("d=", glyphBeginSearch) + 3
        glyphEnd = font.find(" />",glyphBeginSearch) - 1
        glyph = font[glyphBegin:glyphEnd]
        glyphSet.append((i,glyph))

# on per font basis functions
def shuffleGlyphSet():
    for i in range(len(glyphSet)):
        newLocation = random.randint(0,len(glyphSet) - 1)
        temp = glyphSet[newLocation]
        glyphSet[newLocation] = glyphSet[i]
        glyphSet[i] = temp

def generateFont():
    shuffleGlyphSet()
    return generateObfuscatedFont()

def generateObfuscatedFont():
    obfuscatedFont = docHeader + fontHeader + fontFaceHeader
    for i in range(len(characterSet)):
        obfuscatedFont += '<glyph glyph-name="' + characterSet[i] + '" unicode="' + characterSet[i] + '" d="' + glyphSet[i][1] + '" />'
    obfuscatedFont += '</font></defs></svg>'
    return obfuscatedFont

def findEmail(email):
    newEmail = ''
    for char in email:
        newEmail += characterSet[findInGlyphSet(clearCharacterSet.index(char))]
    return newEmail

def findInGlyphSet(index):
    for i in range(len(glyphSet)):
        if glyphSet[i][0] == index:
            return i
    return -1

# Initialize the application
init()

# Start web server if run in command line
if __name__ == '__main__':
    app.run("ec2-23-21-153-84.compute-1.amazonaws.com", 5000)
