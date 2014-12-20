import sys, os, time, random, thread, threading, Globals
from utils import cls
from utils import debug

class main(object):
    def __init__(self, gmode="custom", power=100, time=0, sectohour=86, usage=9.6):
        sys.setrecursionlimit(5000) #Magic.
        threading.stack_size(128*4096) #Magic.
        self.animlvlsum = 0
        self.gmode = gmode #Game mode. Normal / Custom (custom animatronics AI) / Survival (No time, no energy) / ???
        for animatronic in Globals.animatronics:
            self.animlvlsum += animatronic.ailvl
            self.ailvl = self.animlvlsum / len(Globals.animatronics) #This is the lvl of the night.
        self.leftdoor = False #False = Open / True = Closed
        self.rightdoor = False #Same ^^^^^^^^^^^^^^
        self.leftlight = False #False = Off / True = On
        self.rightlight = False #Same ^^^^^^^^^^^^^
        self.power = power #Power
        self.killed = False #Killed or not
        self.usrinput = "" #User input. Used in self.securityOffice() and self.cam()
        self.time = time - 1 #The "-1" is because automatically the timer sums 1.
        self.sectohour = sectohour #Seconds needed for a IN-GAME hour
        self.usage = usage #Amount of seconds that has to pass for draining 1% power
        self.camon = False #False = Not viewing cams / True = Viewing
        self.noh = 0 #"No one here" var. Used for saying if there's someone in a cam or not.
        if self.gmode != "survival": #Initialize the timers
            self.hourTimer()
        self.powerTimer()
        thread.start_new_thread(self.checkDoorTimer, ())
        thread.start_new_thread(self.foxkindDoorCheck, ())
        self.securityOffice() #The main gameplay aspect

    def shutdown(self): #Shuts down the whole game/Restarts it.
        debug.debugprint("Shutting down")
        for animatronic in Globals.animatronics:
            animatronic.dmove("off")
        sys.exit(0)
        os._exit(0)
        os.system("exit")

    def blackout(self): #Blackout event. yay
        for animatronic in Globals.animatronics:
            if animatronic.kind == "bear":
                print "Power went out..."
                cls.cls(random.randint(2, 8))
                print "%s is at the left door." % (animatronic.name)
                print "A music box starts playing."
                cls.cls(random.randint(0, random.randint(1, 10)))
                print "You see nothing at all."
                print "You hear steps."
                cls.cls(random.randint(1, random.randint(3, 8)))
                if self.time != 6:
                    self.die(animatronic)
                    break
                else:
                    pass

    def powerTimer(self): #Timer for the power.
        if self.killed == True or self.time >= 6 or self.power == 0 - 1:
            pass
        else:
            if self.power <= 0 - 1:
                self.blackout()
            else:
                self.usedpow = random.randint(1, 3)
                self.power -= self.usedpow
                debug.debugprint("Power goes down by %s" % (self.usedpow))
                threading.Timer(long(self.usage), self.powerTimer).start()
            return None

    def hourTimer(self): #Timer for the IN-GAME time.
        if self.time >= 6 and self.killed != True:
            cls.cls(1)
            print "5AM --> 6AM"
            print "You survived!"
            cls.cls(5)
            if self.gmode == "custom":
                print "NOTICE OF TERMINATION:"
                print "Reason: Tampering with the animatronics."
                print "General unproffesionalism. Odor."
                print ""
                print "Thanks, mngmnt."
            if self.gmode == "overtime":
                print "Good job, sport!"
                print "(You've earned some overtime.)"
                print "You get 120.50$"
            else:
                print "Good job, sport!"
                print "(See you next week!)"
                print "You get 120$."
            self.shutdown()
            return None
        else:
            self.time += 1
            threading.Timer(self.sectohour, self.hourTimer).start()
            return None

    def checkDoorTimer(self): #"Timer" that checks if there are animatronics at the doors
        for animatronic in Globals.animatronics: #Checks for animatronics
            if animatronic.location == "leftdoor": #If animatronic is at left door
                time.sleep(20 / animatronic.ailvl)
                if self.leftdoor == True: #If leftdoor is closed
                    animatronic.rmove("cam1b") #Go back to cam1b or not

                else: #Else if leftdoor is open
                    time.sleep(20 / animatronic.ailvl)
                    animatronic.dmove("inside") #Go inside
                    if self.ailvl > 12: #If AILVL is over 12
                        self.leftlight = "broken" #Break the light and door
                        self.leftdoor = "broken"

            if animatronic.location == "rightdoor":
                time.sleep(20 / animatronic.ailvl)
                if self.rightdoor == True:
                    animatronic.rmove("cam1b")


                else:
                    time.sleep(20 / animatronic.ailvl)
                    animatronic.dmove("inside")
                    if self.ailvl > 12:
                        self.rightlight = "broken"
                        self.rightdoor = "broken"

        if self.time >= 6 or self.power <= 0:
            pass
        else:
            time.sleep(20 / self.ailvl)
            self.checkDoorTimer()
        return None


    def foxkindDoorCheck(self):
        #debug.debugprint(("Foxkind door check.")
        if self.time >= 6 or self.power <= 0 - 1:
            pass

        else:
            for animatronic in Globals.animatronics:
                if animatronic.location == "leftdoor" and animatronic.kind == "fox":
                    if self.leftdoor == True:
                        print "%s bangs your door" % (animatronic.name)
                        self.powlost = random.randint(1, 15)
                        self.power -= self.powlost
                        print "You lost %s power" % (self.powlost)
                        animatronic.location = "cam1c"
                        animatronic.foxstatus = 0
                        animatronic.foxtseen = 0
                        time.sleep(1)
                        self.foxkindDoorCheck()
                    else:
                        self.die(animatronic)

            threading.Timer(3.0, self.foxkindDoorCheck).start()


        #GAMEPLAY#
#Basically the security office and the cameras.

    def securityOffice(self): #-Almost- the most important thing in main. From here you can do EVERYTHING.
        if self.power < 0 or self.time >= 6 or self.killed == True: #Checks if there's a blackout/You survived/You're dead
            pass
        else: #Prints power, time...
            print "----- %s %s power left. After %s seconds, 1 %s power is lost." % (self.power, "%", self.usage, "%")
            print "Security Office"
            if self.gmode == "survival":
                print "----- SURVIVAL MODE"

            if self.gmode != "survival" and self.time == 0:
                print "----- 12 PM" #I hate this time format

            if self.gmode != "survival" and self.time != 0:
                "----- %s AM" % (self.time)

            for animatronic in Globals.animatronics: #This for loop sets bearkind's bseen variable on false.
                if animatronic.kind == "bear":
                    animatronic.bseen = False

            self.usrinput = raw_input("> ").lower()

            if self.usrinput in ["debug", "debugmode"]:
                if Globals.debug == True:
                    Globals.debug = False
                else:
                    Globals.debug = True
                debug.debugprint("If you see this, debug mode is now enabled!")
                self.securityOffice()
                return None
            #Power
            if self.usrinput in ["power", "electricity", "energy"]:
                print "Power left: %s %s" % (self.power, "%")
                self.securityOffice()
                return None #"Closes" the current security office.

            #Cameras
            if self.usrinput in ["cam", "sec cam", "security cam", "camera", "cams", "cm", "camer"]:
                cls.cls(0.5, 0.5)
                self.usage -= 2.4
                self.camon = True
                self.cam()
                return None

            #Clears the window.
            if self.usrinput in ["clear", "cls"]:
                cls.cls()
                self.securityOffice()
                return None

            #Left door
            if self.usrinput in ["doorl", "left door", "ldoor", "door left", "doortleft", "leftdoor", "dl", "d l"]:
                if self.leftdoor == False:
                    print "Closed left door."
                    self.leftdoor = True
                    self.usage -= 3 #2.4 / 2,4
                    self.securityOffice()
                    return None

                if self.leftdoor == True:
                    print "Opened left door."
                    self.leftdoor = False
                    self.usage += 3
                    self.securityOffice()
                    return None

                if self.leftdoor == "broken":
                    print "Left door doesn't work..."
                    self.securityOffice()
                    return None


            #Right door
            if self.usrinput in ["doorr", "right door", "rdoor", "door right", "doortright", "rightdoor", "d r", "dr"]:
                if self.rightdoor == False:
                    print "Closed right door."
                    self.rightdoor = True
                    self.usage -= 3
                    self.securityOffice()
                    return None

                if self.rightdoor == True:
                    print "Opened right door."
                    self.rightdoor = False
                    self.usage += 3
                    self.securityOffice()
                    return None

                if self.rightdoor == "broken":
                    print "Right door doesn't work..."
                    self.securityOffice()
                    return None

            #Left light
            if self.usrinput in ["lightl", "left light", "llight", "light left", "lightleft", "leftlight", "ll", "l l"]:
                if self.leftlight == True:
                    print "Left light is now OFF."
                    self.leftlight = False
                    self.usage += 1.2
                    self.securityOffice()
                    return None

                if self.leftlight == False:
                    self.leftlight = True
                    if self.rightlight == True:
                        print "Right light is now OFF."
                        self.rightlight = False
                        self.usage += 1.2
                    self.usage -= 1.2
                    print "Left light is now ON."
                    self.foxkindDoorCheck()
                    for animatronic in Globals.animatronics:
                        if animatronic.location == "leftdoor":
                            print "%s is at the left door, looking at you." % (animatronic.name)
                    self.securityOffice()
                    return None

                if self.leftlight == "broken":
                    print "Left light doesn't work..."
                    self.securityOffice()
                    return None

            #Right light
            if self.usrinput in ["lightr", "right light", "rlight", "light right", "lightright", "rightlight", "lr", "l r"]:
                if self.rightlight == True:
                    print "Right light is now OFF."
                    self.rightlight = False
                    self.usage += 1.2
                    self.securityOffice()
                    return None

                if self.rightlight == False:
                    self.rightlight = True
                    if self.leftlight == True:
                        print "Left light is now OFF."
                        self.leftlight = False
                        self.usage += 1.2
                    self.usage -= 1.2
                    print "Right light is now ON."
                    for animatronic in Globals.animatronics:
                        if animatronic.location == "rightdoor":
                            print "%s is at the right door, looking at you." % (animatronic.name)
                    self.securityOffice()
                    return None

                if self.rightlight == "broken":
                    print "Right light doesn't work..."
                    self.securityOffice()
                    return None
            #Help
            if self.usrinput in ["help", "what do i do?", "?"]:
                print "-----"
                print "Hi! Welcome to pyDLASYIAS (pyDon't let animatronics stuff you in a suit)"
                print "It looks like you're asking for help."
                print "I'll help you!"
                print "Here's a command list:"
                print "'door left' 'door right' 'light left' 'light right' 'help' 'cam' 'clear' 'state'"
                print "There's a few more commands (Similar words that do the same as the words above)"
                print "Oh and about the 'camera mode'"
                print "It's very easy to use. You type the camera name and you see if something or someone is there!"
                print "You can also use some commands there, like 'exit'"
                print "And that's all. Except for how to play, but you should know how to play already, so..."
                print "Good night!"
                print "-----"
                self.securityOffice()
                return None

            if self.usrinput in ["state", "doors", "lights", "door state", "light state"]:
                if self.leftdoor == True:
                    print "Left door is closed."
                else:
                    print "Left door is open."

                if self.rightdoor == True:
                    print "Right door is closed."
                else:
                    print "Right door is open."

                if self.leftlight == True:
                    print "Left light is on."
                else:
                    print "Left light is off."

                if self.rightlight == True:
                    print "Right light is on."
                else:
                    print "Right light is off."

                self.securityOffice()
                return None

            #Unknown command.
            else:
                if self.killed == False:
                    print "What was that? Try again, please!"
                    self.securityOffice()
                    return None
                else:
                    print "You're dead. You can close the game now."
                    print "...but you can't escape"
                    self.shutdown()

    def cam(self): #Camera mode. You can watch the animatronics from here.
        if self.leftlight == True:
            self.usage += 1.2
            self.leftlight = False

        if self.rightlight == True:
            self.usage += 1.2
            self.rightlight = False

        if self.killed == True or self.time >= 6 or self.power == 0 - 1:
            pass
        else:
            for animatronic in Globals.animatronics:
                if animatronic.kind == "bear":
                    animatronic.bseen = True
            print "Cam list:"
            print " -- ".join(sorted(list(Globals.camdic))) #Wow. Just don't change it, it's magical...
            self.usrinput = raw_input("> ").lower()  #User input

            #Looks at a certain camera to see if something or someone is there.
            if self.usrinput in Globals.camdic.keys():
                print "----- %s %s power left. After %s seconds, 1 %s power is lost." % (self.power, "%", self.usage, "%")
                print Globals.camdic[self.usrinput] + " [Camera Mode]"
                if self.gmode == "survival":
                    print "----- SURVIVAL MODE"

                if self.gmode != "survival" and self.time == 0:
                    print "----- 12 PM" #I hate this time format

                if self.gmode != "survival" and self.time != 0:
                    print "----- %s AM" % (self.time)

                self.checkAnimCam(self.usrinput)
                self.cam()
                return None

            #Clears the window.
            if self.usrinput in ["clear", "cls"]:
                cls.cls()
                self.cam()
                return None

            #Closes camera mode. Also handles certains game overs.
            if self.usrinput in ["exit", "close", "x", "e", "c"]:
                time.sleep(1)
                for animatronic in Globals.animatronics: #Checks if there's "someone" inside...
                    if animatronic.location == "inside":
                        if animatronic.kind != "bear":
                            self.die(animatronic)

                    else:
                        self.usage += 2.4
                        self.securityOffice()
                        return None
                        for animatronic in Globals.animatronics:
                            if animatronic.kind == "bear":
                                animatronic.bseen = False



            else:
                if self.killed == False:
                    print "Unknown cam"
                    self.cam()
                    return None
                else:
                    print "You're dead. You can close the game"
                    print "...but the animatronics will wait for you"
                    self.shutdown()


    def die(self, animatronic):
        if animatronic.kind == "rabbit" or animatronic.kind == "chicken":
            self.killed = True
            cls.cls(1)
            print "%s jumps at your face as a loud screech comes from the animatronic." % (animatronic.name)
            print "%s got you..." % (animatronic.name)
            print "Game over."
            self.shutdown()

        if animatronic.kind == "bear":
            self.killed = True
            cls.cls(1)
            print "%s grabs you and jumps at your face. A really loud screech can be heard." % (animatronic.name)
            print "%s got you..." % (animatronic.name)
            print "Game over..."
            self.shutdown()

        if animatronic.kind == "fox":
            self.killed = True
            cls.cls(1)
            print "%s enters the room as a loud screech can be heard." % (animatronic.name)
            print "%s got you..." % (animatronic.name)
            print "Game over..."
            self.shutdown()



    def hallucination(self, kind):
        if kind == "camkind":
            self.randhall = random.randint(0, 80)
            if self.randhall in range(0, self.ailvl):
                print "IT'S ME   "
                if random.randint(0, 2) == 1:
                    print "            IT'S        ME"

    def someoneThere(self, cam):
        for animatronic in Globals.animatronics:
            if animatronic.location == cam:
                return True
        return False


    def checkAnimCam(self, cam):
        if cam == "cam2a":
            for animatronic in Globals.animatronics:
                if animatronic.kind == "fox" and animatronic.foxstatus >= 4:
                    animatronic.foxstatus = 5
                    animatronic.think()
                    print "You see %s sprinting down the hall." % (animatronic.name)
                    time.sleep(1)
                    self.securityOffice()
                    return None
                if animatronic.location == cam and animatronic.kind != "fox":
                    self.hallucination("camkind")
                    print "%s is here." % (animatronic.name)

        if cam == "cam1c":
            for animatronic in Globals.animatronics:
                if animatronic.location == cam and animatronic.kind == "fox":
                    animatronic.foxtseen += 1
                    if animatronic.foxstatus <= 0:
                        print "%s is hiding behind the curtain." % (animatronic.name)

                    if animatronic.foxstatus == 1:
                        print "%s is peeking through the curtain." % (animatronic.name)

                    if animatronic.foxstatus == 2:
                        print "%s is looking through the curtain." % (animatronic.name)

                    if animatronic.foxstatus == 3:
                        print "%s is out." % (animatronic.name)

                    if animatronic.foxstatus == 4:
                        print "%s is gone." % (animatronic.name)

        if cam == "cam1a":
            for animatronic in Globals.animatronics:
                if animatronic.location == cam:
                    if random.randint(0, 1) == 1:
                        print "%s is here." % (animatronic.name)
                    else:
                        print "%s is looking directly to the camera." % (animatronic.name)

        if cam == "cam4b":
            for animatronic in Globals.animatronics:
                if animatronic.location == cam and animatronic.kind != "bear":
                    print "%s is here." % (animatronic.name)

                if animatronic.location == cam and animatronic.kind == "bear":
                    print "%s is looking directly to the camera." % (animatronic.name)

        if cam == "cam6":
            for animatronic in Globals.animatronics:
                if animatronic.location == cam:
                    if animatronic.kind == "bear":
                        print "A music box can be heard."
                    else:
                        print "Noise can be heard."

        elif cam not in ["cam1c", "cam1a", "cam4b", "cam6", "cam2a"]:
            for animatronic in Globals.animatronics:
                if animatronic.location == cam and animatronic.kind != "bear":
                    print "%s is here." % (animatronic.name)
                if animatronic.location == cam and animatronic.kind == "bear":
                    print "%s" % (random.choice(["...huh?", "W-What's that?", "..."]))