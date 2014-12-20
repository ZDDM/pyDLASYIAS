import sys, os, time, random, thread, threading, Globals
from utils import cls
from utils import debug

class animatronic(object): #Animatronics' class.
    def __init__(self, name, kind, ailvl=20, location="cam1a"):
        self.name = name         #Name will be used for printing things.
        self.kind = kind         #Kinds: Chicken / Rabbit / Bear (WIP) / Fox
        self.ailvl = ailvl       #AI LVL. 1 - 20. ("0 AI LVL" is impossible to achieve, because you can't divide by zero.)
        self.location = location #This location determines where the animatronics are.
        self.slocation = location #Starting location.
        Globals.animatronics.append(self) #Appends itself to animatronics' list.
        if self.kind == "fox":   #Foxkind variables.
            self.foxstatus = 0 #0 = Hiding. 1 = Peeking. 2 = Looking thro. 3 = Out 4 = About to sprint 5 = Sprinting
            self.foxtseen = 0 #Times seen.
            self.foxsleep = 0 #Number of seconds to sleep until next status.

        if self.kind == "bear": #Bearkind variables.
            self.bseen = False #Being seen. If the camera is active, this variable will be true. Else, it will be false.

        if self.ailvl <= 20:
            if self.ailvl == 0:
                self.ailvl = 0.5
            debug.debugprint("%s's AI started." % (self.name.upper()), self)
            if self.kind == "bear":
                if self.ailvl > 5:
                    debug.debugprint("%s's AI IS NOW ACTIVE!" % (self.name.upper()), self)
                    self.dmove("cam1a")
                else:
                    self.dmove("off")

            thread.start_new_thread(self.think, ()) #Multithreading. This makes the game possible

        else:
            print "%s's AI LEVEL IS OVER 20. BE CAREFUL!" % (self.name.upper())
            if self.kind == "bear":
                if self.ailvl > 5:
                    debug.debugprint("%s's AI IS NOW ACTIVE!" % (self.name.upper()), self)
                    self.dmove("cam1a")
                else:
                    self.dmove("off")
            thread.start_new_thread(self.think, ()) #Multithreading. This makes the game possible

    def dmove(self, room): #Direct move / Debug move. Moves an animatronic to a location.
        self.location = room
        if room == "off":
            debug.debugprint("%s has been queued for shutdown." % (self.name), self)
        else:
            debug.debugprint("DMoved %s to %s" % (self.name, room), self)
        return None

    def rmove(self, room): #Random move. Moves an animatronic (or not) to a location.
        self.choice = random.choice(room) #Yup. You can input lists!
        debug.debugprint("%s's choice was %s" % (self.name, self.choice), self)
        if random.randint(0, self.ailvl / 2) in range(0, self.ailvl / 2):
            self.location = self.choice
            debug.debugprint("%s moved to %s" % (self.name, self.choice), self)
            self.think()
            return None

        else:
            debug.debugprint("%s didn't move at all" % (self.name), self)
            self.think()
            return None

    def think(self):
        if self.location == "off": #Shuts down the AI
            debug.debugprint("%s's AI is shutting down." % (self.name), self)
            os.system("exit")
            sys.exit(0)
            os._exit(0)
            return None
        else:
            #Chicken's AI
            if self.kind == "chicken":
                debug.debugprint("%s is thinking..." % (self.name), self)
                time.sleep(random.randint(20, 25) / self.ailvl)
                if self.location == "cam1a":
                    self.rmove(["cam1b"])
                if self.location == "cam1b":
                    self.rmove(["cam1a", "cam7", "cam6", "cam4a"])
                if self.location == "cam7":
                    self.rmove(["cam1b"])
                if self.location == "cam6":
                    self.rmove(["cam1b"])
                if self.location == "cam4a":
                    self.rmove(["cam1b", "rightdoor", "cam4b", "cam4b"])
                if self.location == "cam4b":
                    self.rmove(["cam4a", "rightdoor", "cam1a"])
                if self.location == "rightdoor":
                    debug.debugprint("%s is at rightdoor." % (self.name), self)
                if self.location == "inside":
                    pass
                return None
                time.sleep(random.randint(20, 25) / self.ailvl)


            #Rabbit's AI
            if self.kind == "rabbit":
                debug.debugprint("%s is thinking..." % (self.name), self)
                time.sleep(random.randint(20, 25) / self.ailvl)
                if self.location == "cam1a":
                    self.rmove(["cam1b"])
                if self.location == "cam1b":
                    self.rmove(["cam1a", "cam5", "cam2a", "cam2a"]) #Do not edit cam2a, it's doubled for a reason.
                if self.location == "cam5":
                    self.rmove, (["cam1b"])
                if self.location == "cam2a":
                    self.rmove(["cam3", "leftdoor", "cam2b", "cam2b"])
                if self.location == "cam3":
                    self.rmove(["cam2a", "leftdoor", "cam2b"])
                if self.location == "cam2b":
                    self.rmove(["cam2a", "leftdoor", "cam1a"])
                if self.location == "leftdoor":
                    debug.debugprint("%s is at leftdoor." % (self.name), self)
                if self.location == "inside":
                    pass
                return None
                time.sleep(random.randint(20, 25) / self.ailvl)

            #Fox's AI
            if self.kind == "fox":
                debug.debugprint("%s is thinking..." % (self.name), self)
                time.sleep(random.randint(20, 25) / self.ailvl)
                if self.foxstatus == 4:
                    time.sleep(100 / self.ailvl)
                    self.foxstatus = 5


                if self.foxstatus >= 5:
                    debug.debugprint("%s is sprinting towards the Security Office." % (self.name), self)
                    time.sleep(20 / self.ailvl)
                    self.location = "cam2a"
                    time.sleep(20 / self.ailvl)
                    self.location = "leftdoor"

                if self.foxtseen >= 1:
                    debug.debugprint("%s status remains at %s." % (self.name, self.foxstatus), self)
                    self.foxsleep += self.foxtseen
                    self.basesleep = random.randint(150, 200) / self.ailvl
                    self.foxtseen = 0
                    time.sleep(self.basesleep + self.foxsleep)
                    if random.randint(0, 1) == 1:
                        self.foxstatus += 1
                        debug.debugprint("%s status is now %s." % (self.name, self.foxstatus), self)
                        self.think()
                    else:
                        debug.debugprint("%s status remains at %s." % (self.name, self.foxstatus), self)
                        self.think()



                else:
                    if random.randint(0, 1) == 1:
                        self.foxstatus +=1
                        debug.debugprint("%s status is now %s" % (self.name, self.foxstatus), self)
                    else:
                        debug.debugprint("%s status remains at %s" % (self.name, self.foxstatus), self)
                    time.sleep(random.randint(150, 200) / self.ailvl)
                    self.think()


            #Bear's AI
            if self.kind == "bear":
                if self.ailvl > 5:
                    debug.debugprint("%s is thinking..." % (self.name), self)
                    time.sleep(40 / self.ailvl)
                    if self.location == "cam1a":
                        if self.someoneThere("cam1a") == True:
                            debug.debugprint("%s.bseen = %s" % (self.name, self.bseen), self)
                            if self.bseen == False:
                                self.rmove(["cam1b"])
                                print ""
                                print "A deep laugh can be heard."
                                print "> "
                                self.think()
                        else:
                            self.think()


                    if self.location == "cam1b":
                        if self.bseen == False:
                                print ""
                                print "A deep laugh can be heard."
                                print "> "
                                self.rmove("cam7")
                        else:
                            self.think()

                    if self.location == "cam7":
                        if self.bseen == False:
                                print ""
                                print "A deep laugh can be heard."
                                print "> "
                                self.rmove(["cam6"])
                        else:
                            self.think()

                    if self.location == "cam4a":
                        if self.bseen == False:
                                print ""
                                print "A deep laugh can be heard."
                                print "> "
                                self.rmove(["cam4b"])

                    if self.location == "cam4b":
                        time.sleep(40 / self.ailvl)
                        if self.bseen == False:
                            print ""
                            print "A deep laugh can be heard."
                            print "> "
                            self.rmove(["inside", "cam4a", "cam4a"])

                    if self.location == "rightdoor":
                        pass
                else:
                    pass

                return None


    def someoneThere(self, cam): #Function for bearkind. Duh.
        for animatronic in Globals.animatronics:
            if animatronic.kind == "bear":
                pass
            elif animatronic.location == cam:
                return True
        return False