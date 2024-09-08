"""
unshared.py
"""
__author__ = "BobLYX"
__version__ = "2024.09.08"

import random
from pprint import pprint
from uuid import uuid4
from multiprocessing import Process, Queue
import time
import datetime

def chunklist(li, chunks):
    quot, rem = divmod(len(li), chunks)
    divpt = lambda i: i * quot + min(i, rem)
    return [li[divpt(i):divpt(i+1)] for i in range(chunks)]

def roll(num, sides, mod=0):
    the_sum = 0
    for n in range(num):
        the_sum += random.randint(1,sides)
    the_sum += mod
    return the_sum

def attack(**kwargs):
    required = ["target", "source"]
    for r in required:
        if not r in kwargs.keys(): return
    target = kwargs["target"]
    source = kwargs["source"]
    damage = roll(1,2)
    target.health -= damage

    if(target.health <= 0): 
        #print("%s defeated %s!" % (source.id, target.id))
        pass
    pass

def moveRandom(**kwargs):
    required = ["source", "arena"]
    for r in required:
        if not r in kwargs.keys(): return
    source = kwargs["source"]
    arena = kwargs["arena"]
    coords = source.location.coords
    prelim_options = [(coords[0]+1, coords[1])
               ,(coords[0]-1, coords[1])
               ,(coords[0], coords[1]+1)
               ,(coords[0], coords[1]-1)
               ]
    final_options = []
    min_lim = -1
    max_lim = arena.size
    for o in prelim_options:
        if min_lim in o or max_lim in o:
            continue
        final_options.append(o)
        pass
    choice = random.choice(final_options)
    source.location = arena.places[choice]
    print("%s moved to %s." % (source.id, str(choice)))
    pass

def findRival(source, arena):
    rival = arena.randomOther(source)
    return rival

def findRivalMP(source, players):
    ids = []
    for i,p in enumerate(players):
        if p.id == source.id: continue
        ids.append(i)
    if len(ids) == 0:
        return
    other = random.choice(ids)
    other = players[other]
    return other

def actMP(players ,queue):
    for player in players:
        action = attack #random.choice(list(ACTIONS.values()))
        # pick a random foe
        if player.rival == None:
            rival = findRivalMP(player, players)
            player.rival = rival
        # move towards rival if not none
        if player.rival == None:
            return
        # just attack rival
        attack(source = player, target = player.rival)
    queue.put(players)

ACTIONS = {"attack": attack} 
# {"move": move, "attack": attack}

class Player:
    def __init__(self):
        self.id = str(uuid4()).split("-")[0]
        self.health = 10
        self.logo = "@"
        self.location = None
        self.rival = None
        pass
    def act(self, arena):
        action = random.choice(list(ACTIONS.values()))
        # pick a random foe
        if self.rival == None:
            rival = findRival(self, arena)
            self.rival = rival
        # move towards rival if not none
        if self.rival == None:
            return
        # just attack rival
        attack(source = self, target = self.rival)
    pass

class Place:
    def __init__(self, coords):
        occupants = []
        self.coords = coords
        pass
    pass

class Arena:
    def __init__(self):
        self.places = {}
        self.players = {} 
        self.size = 0
        self.sim_players = {} # for multiproc
        pass

    @staticmethod
    def generate(size = 10):
        arena = Arena()
        arena.size = size
        arena.places = {}
        for x in range(size):
            for y in range(size):
                arena.places[(x,y)] = Place((x,y))
                pass
            pass
        return arena

    def addRandomPlayers(self, number = 6):
        num_players = number #random.randint(2, number)
        for i in range(num_players):
            player = Player()
            self.players[player.id] = player
            place = random.choice(list(self.places.values()))
            player.location = place
            pass
        pass

    def randomPlayer(self):
        return random.choice(list(self.players.values()))

    def randomOther(self, player):
        '''
        Find a random other player
        '''
        ids = list(self.players.keys())
        ids.remove(player.id)
        if len(ids) == None:
            return None
        other_id = random.choice(ids)
        return self.players[other_id]

    def step(self):
        # Handle all players concurrently
        for player in arena.players.values():
                player.act(arena)
        #self.report()
        pass

    def step_mp(self, cpus = 10):
        # First split into 10 groups
        lists = chunklist(list(self.players.values()), cpus)
        procs = []
        q = Queue()
        rets = []
        
        for l in lists:
            process = Process(target=actMP, args=(l,q))
            procs.append(process)
            process.start()
            pass

        for p in procs:
            ret = q.get()
            rets.append(ret)

        for p in procs:
            p.join()

        for plist in rets:
            for p in plist:
                self.players[p.id] = p
            pass
        #self.report();

    def report(self):
        for p in self.players.values():
            print("%s: %d" %(p.id, p.health))
            pass

if __name__ == "__main__":
    num_players = 20000
    steps = 100

    # Single Process
    arena = Arena.generate()
    arena.addRandomPlayers(num_players)
    start = time.time()
    for i in range(1,1+steps):
        if i % 50 == 0:
            print("Single: Step %d"%i)
        arena.step()
    end = time.time()
    print("Single: Completed in %1.2f" % ((end - start)*1000))
    
    # Multi Process
    arena = Arena.generate()
    arena.addRandomPlayers(num_players)
    start = time.time()
    for i in range(1,1+steps):
        if i % 50 == 0:
            print("Multi: Step %d"%i)
        arena.step_mp(cpus = 10)
    end = time.time()

    print("Multi: Completed in %1.2f" % ((end - start)*1000))
