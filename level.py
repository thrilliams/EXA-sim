from EXA import EXA
import registers as r
# from time import sleep
from random import choice

class Level:
    def __init__(self, data):
        self.cyc = 0
        self.exas = []
        data['hosts'] = dict(data['hosts'])

        for host in data['hosts'].items():
            for i in range(len(host[1]['files'])):
                host[1]['files'][i] = r.File(host[1]['files'][i][0], host[1]['files'][i][1], host[0])
        self.hosts = data['hosts']


        for code in data['exas']:
            for i in range(len(code)):
                if code[i].find('#') > -1:
                    code[i] = code[i][0:code[i].find('#')].split()
                else:
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
        for host in self.hosts.items():
            for file in host[1]['files']:
                files.append(file)
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
        if any([e.line < len(e.code) for e in self.exas]):
            # if any EXAs still have instructions to run
            self.cyc += 1
            # sleep(0.25)
            self.cycle()