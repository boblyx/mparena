"""
shared.py
"""
__author__ = "BobLYX"
__version__ = "2024.09.08"

import random
from pprint import pprint
from uuid import uuid4
from multiprocessing import Process, Manager
from multiprocessing import managers as m
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

class CMan(m.BaseManager):
    pass

class Player:
    def __init__(self):
        self.id = str(uuid4()).split("-")[0]
        self.health=10
        pass
    def get_id(self):
        return self.id

    def get_health(self):
        return self.health

    def take_dmg(self,dmg):
        self.health -= dmg
        pass

    def report(self):
        return self.__dict__
    pass

class PlayerDict:
    def __init__(self):
        player
        pass
    pass

def attack(players, arena):
    for player in players:
        other_ids = [p for p in list(arena.pids)]
        other_id = random.choice(other_ids)
        other_player = arena.players[other_id]
        if other_player.get_health() <= 0: return
        other_player.take_dmg(roll(1,6))
        #print("%s attacked %s" % (player.get_id(), other_id))
        if other_player.get_health() <= 0: 
            #print("%s defeated %s" % (player.get_id(), other_id))
            return
    pass

def attack2(players):
    for player in players:
        other_ids = [p.get_id() for p in players]
        other_id = random.choice(other_ids)
        if other_id == player.get_id(): return
        other_player = arena.players[other_id]
        if other_player.get_health() <= 0: return
        other_player.take_dmg(roll(1,6))
        #print("%s attacked %s" % (player.get_id(), other_id))
        if other_player.get_health() <= 0: 
            #print("%s defeated %s" % (player.get_id(), other_id))
            return
    pass

CMan.register("Player", Player)
MANAGER = Manager()
class Arena:
    def __init__(self, manager):
        self.manager = manager
        self.players = MANAGER.dict()
        self.pids = MANAGER.list()
        pass

    def addPlayers(self,num):
        for i in range(num):
            player = manager.Player()
            #print(player.get_id())
            self.players[player.get_id()] = player
            self.pids.append(player.get_id())
        pass

    def step(self, cpus = 10):
        lists = chunklist((self.players.values()), cpus)
        procs = []
        for l in lists:
            #process = Process(target=attack, args=(l, arena))
            process = Process(target=attack2, args=(l,))
            procs.append(process)
            process.start()
            pass
        for p in procs:
            p.join()
        pass

CMan.register("Arena", Arena)

with CMan() as manager:
    arena = Arena(manager)
    arena.addPlayers(2000) # ~ 6000ms

    start = time.time()
    arena.step(cpus = 10)

    #for p in arena.players.values():
    #    #pprint(p.report())
    #    pass

    end = time.time()
    print("Completed in %1.2f" % ((end - start)*1000))
