from EXA import *
import json
# from time import sleep
from random import choice

class Level:
    def __init__(self, levels):
        self.cyc = 0
        self.exas = []


        data = json.loads(levels)
        for host in data['hosts']:
            for i in range(len(data['hosts'][host]['files'])):
                data['hosts'][host]['files'][i] = File(data['hosts'][host]['files'][i][0], data['hosts'][host]['files'][i][1], host)
        self.hosts = data['hosts']


        for exa in data['exas']:
            file = open(exa)
            code = file.read().split('\n')
            file.close()
            for i in range(len(code)):
                try:
                    code[i] = code[i][0:code[i].index('#')].split()
                except ValueError:
                    code[i] = code[i].split()
                for j in range(len(code[i])):
                    try:
                        code[i][j] = int(code[i][j])
                    except ValueError:
                        code[i][j] = code[i][j]
            while [] in code:
                code.remove([])
            self.exas.append(EXA(self, code, 'AHIZOME', 'X' + chr(ord('A') + len(self.exas))))


        self.cycle()
    def __repr__(self):
        return str(self.hosts)
    def files(self):
        files = []
        for host in self.hosts:
            files += self.hosts[host]['files']
        return files
    def grab(self, host, id):
        for file in self.files():
            if file.host == host and file.id == id:
                return file
        return False
    def kill(self, name, host):
        exas = []
        for exa in self.exas:
            if exa.name != name and exa.host == host:
                exas.append(exa)
        choice(exas).halt()
    def cycle(self):
        for exa in self.exas:
            exa.eval(self.cyc)
        if any([e.line < len(e.code) for e in self.exas]): # if any EXAs still have instructions to run
            self.cyc += 1
            # sleep(0.25)
            self.cycle()

file = open('level.json', 'r')
Level(file.read())
file.close()