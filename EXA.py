from registers import *

class EXA:
    def __init__(self, level, code, host, name, start = 0, scope = 'GLOBAL', x = Register(0), t = Register(0)):
        self.name = name
        self.code = code
        self.host = host
        self.cycle = level.cyc
        self.level = level
        self.registers = {
            'X': x,
            'T': t,
            'F': None,
            'M': Communication(scope, self)
        }
        self.children = []
        self.labels = {}

        self.line = 0
        for line in code:
            if line[0] == 'MARK':
                self.mark(line[1:])
            self.line += 1
        self.line = start

    def __repr__(self):
        line = str(self.line + 1) + '/' + str(len(self.code))
        if self.line + 1 > len(self.code):
            line = 'HALTED'
        string = ('\n' +
                    self.name + ': Line ' + line +
                    '\n' + str(self.registers) +
                    '\n' + str(self.host))
        if self.registers['F'] != None:
            string += '\n' + self.registers['F'].reprlong()
        string += '\n'
        return string
    def clamp(self, val):
        if val > 9999:
            val = 9999
        if val < -9999:
            val = -9999
        return val
    def typeArgs(self, args, types):
        args = [list(e) for e in zip(args, types)]
        try:
            for i in range(len(args)):
                if args[i][1] == 'R':
                    if not args[i][0] in ['X', 'T', 'F', 'M']:
                        raise Exception('INVALID ARGUMENTS')
                if args[i][1] == 'R/N':
                    if args[i][0] in ['X', 'T', 'F', 'M']:
                        args[i][1] = 'R'
                    elif type(args[i][0]) == int and -9999 <= args[i][0] and args[i][0] <= 9999:
                        args[i][1] = 'N'
                    else:
                        raise Exception('INVALID ARGUMENTS')
                if args[i][1] == 'L':
                    if not type(args[i][0]) == str:
                        raise Exception('INVALID ARGUMENTS')
        except IndexError:
            raise Exception('INVALID ARGUMENTS')
        for i in range(len(args)):
            if args[i][1] == 'R' and types[i] == 'R/N':
                args[i] = self.registers[args[i][0]].value()
            else:
                args[i] = args[i][0]
        return args

            # Basic Access

    def copy(self, args):
        args = self.typeArgs(args, ['R/N', 'R'])
        self.registers[args[1]].assign(args[0])

            # Arithmetic

    def addi(self, args):
        args = self.typeArgs(args, ['R/N', 'R/N', 'R'])
        if type(args[0]) != int or type(args[1]) != int:
            raise Exception('NUMERIC VALUE REQUIRED')
        val = args[0] + args[1]
        val = self.clamp(val)
        self.registers[args[2]].assign(val)
    def subi(self, args):
        args = self.typeArgs(args, ['R/N', 'R/N', 'R'])
        if type(args[0]) != int or type(args[1]) != int:
            raise Exception('NUMERIC VALUE REQUIRED')
        val = args[0] - args[1]
        val = self.clamp(val)
        self.registers[args[2]].assign(val)
    def muli(self, args):
        args = self.typeArgs(args, ['R/N', 'R/N', 'R'])
        if type(args[0]) != int or type(args[1]) != int:
            raise Exception('NUMERIC VALUE REQUIRED')
        val = args[0] * args[1]
        val = self.clamp(val)
        self.registers[args[2]].assign(val)
    def divi(self, args):
        args = self.typeArgs(args, ['R/N', 'R/N', 'R'])
        if type(args[0]) != int or type(args[1]) != int:
            raise Exception('NUMERIC VALUE REQUIRED')
        if args[1] == 0:
            raise Exception('CANNOT DIVIDE BY ZERO')
        val = args[0] / args[1]
        val = self.clamp(val)
        self.registers[args[2]].assign(val)
    def modi(self, args):
        args = self.typeArgs(args, ['R/N', 'R/N', 'R'])
        if type(args[0]) != int or type(args[1]) != int:
            raise Exception('NUMERIC VALUE REQUIRED')
        if args[1] == 0:
            raise Exception('CANNOT DIVIDE BY ZERO')
        val = args[0] % args[1]
        val = self.clamp(val)
        self.registers[args[2]].assign(val)
    def swiz(self, args):
        args = self.typeArgs(args, ['R/N', 'R/N', 'R'])
        if type(args[0]) != int or type(args[1]) != int:
            raise Exception('NUMERIC VALUE REQUIRED')
        args[0] = str(args[0])
        while len(args[0]) < 9:
            args[0] = '0' + args[0]
        args[1] = str(args[1])
        while len(args[1]) < 4:
            args[1] = '0' + args[1]
        val = ''
        for e in args[1]:
            val += args[0][-int(e)]
        self.registers[args[2]].assign(int(val))

            # Control Flow

    def mark(self, args):
        args = self.typeArgs(args, ['L'])
        if args[0] in self.labels:
            raise Exception('Label already defined')
        self.labels[args[0]] = self.line
    def jump(self, args):
        args = self.typeArgs(args, ['L'])
        if args[0] not in self.labels:
            raise Exception('Label not defined')
        self.line = self.labels[args[0]]
    def tjmp(self, args):
        args = self.typeArgs(args, ['L'])
        if args[0] not in self.labels:
            raise Exception('Label not defined')
        if self.registers['T'].value() == 1:
            self.line = self.labels[args[0]]
    def fjmp(self, args):
        args = self.typeArgs(args, ['L'])
        if args[0] not in self.labels:
            raise Exception('Label not defined')
        if self.registers['T'].value() == 0:
            self.line = self.labels[args[0]]

            # Conditions

    def teste(self, args):
        args = self.typeArgs(args, ['R/N', 'R/N'])
        if args[0] == args[1]:
            self.registers['T'].assign(1)
        else:
            self.registers['T'].assign(0)
    def testg(self, args):
        args = self.typeArgs(args, ['R/N', 'R/N'])
        if type(args[0]) != type(args[1]):
            return self.registers['T'].assign(0)
        if type(args[0]) == int:
            if args[0] > args[1]:
                self.registers['T'].assign(1)
            else:
                self.registers['T'].assign(0)
        if type(args[0]) == str:
            args[0] = args[0].lower()
            args[1] = args[1].lower()
            if args[0] < args[1]:
                self.registers['T'].assign(1)
            else:
                self.registers['T'].assign(0)
    def testl(self, args):
        args = self.typeArgs(args, ['R/N', 'R/N'])
        if type(args[0]) != type(args[1]):
            return self.registers['T'].assign(0)
        if type(args[0]) == int:
            if args[0] < args[1]:
                self.registers['T'].assign(1)
            else:
                self.registers['T'].assign(0)
        if type(args[0]) == str:
            args[0] = args[0].lower()
            args[1] = args[1].lower()
            if args[0] > args[1]:
                self.registers['T'].assign(1)
            else:
                self.registers['T'].assign(0)

            # Multiprocessing

    def repl(self, args):
        args = self.typeArgs(args, ['L'])
        if args[0] not in self.labels:
            raise Exception('Label not defined')
        exa = EXA(self.level, self.code, self.host, self.name + ':' + len(self.children), self.labels[args[0]], self.scope, Register(self.registers['X'].value()), Register(self.registers['T'].value()))
        self.level.exas.append(exa)
        self.children.append(exa)
    def halt(self, args):
        self.line = len(self.code)
    def kill(self, args):
        self.level.kill(self.name, self.host)

            # Movement

    def link(self, args):
        args = self.typeArgs(args, ['R/N'])
        if type(args[0]) != int:
            raise Exception('NUMERIC VALUE REQUIRED')
        if str(args[0]) in self.level.hosts[self.host]['links']:
            self.host = self.level.hosts[self.host]['links'][str(args[0])]
            if self.registers['F'] != None:
                self.registers['F'].link(self.host)
        else:
            raise Exception('LINK ID NOT FOUND')
    def host(self, args):
        args = self.typeArgs(args, ['R'])
        self.registers[args[0]].assign(self.host)

            # Communication

    def mode(self, args):
        self.registers['M'].mode()
    def voidm(self):
        self.registers['M'].value()
    def testmrd(self):
        return self.registers['M'].mrd()

            # File Manipulation

    def make(self, args):
        if self.registers['F'] == None:
            i = 400
            while i in self.level.files():
                i += 1
            self.registers['F'] = File([], i, self.host)
        else:
            raise Exception('CANNOT GRAB A SECOND FILE')
    def grab(self, args):
        if self.registers['F'] != None:
            raise Exception('CANNOT GRAB A SECOND FILE')
        args = self.typeArgs(args, ['R/N'])
        if type(args[0]) != int:
            raise Exception('NUMERIC VALUE REQUIRED')
        if self.level.grab(self.host, args[0]):
            self.registers['F'] = self.level.grab(self.host, args[0])
        else:
            raise Exception('FILE ID NOT FOUND')
    def file(self, args):
        if self.registers['F'] == None:
            raise Exception('NO FILE IS HELD')
        args = self.typeArgs(args, ['R'])
        args[0].assign(self.registers['F'].id)
    def seek(self, args):
        if self.registers['F'] == None:
            raise Exception('NO FILE IS HELD')
        args = self.typeArgs(args, ['R/N'])
        if type(args[0]) != int:
            raise Exception('NUMERIC VALUE REQUIRED')
        self.registers['F'].seek(args[0])
    def voidf(self):
        if self.registers['F'] == None:
            raise Exception('NO FILE IS HELD')
        self.registers['F'].void()
    def drop(self, args):
        if self.registers['F'] == None:
            raise Exception('NO FILE IS HELD')
        self.registers['F'] = None
    def wipe(self, args):
        if self.registers['F'] == None:
            raise Exception('NO FILE IS HELD')
        self.registers['F'].wipe()
    def testeof(self):
        if self.registers['F'] == None:
            raise Exception('NO FILE IS HELD')
        if self.registers['F'].eof():
            self.registers['T'].assign(1)
        else:
            self.registers['T'].assign(0)

            # Miscellaneous

    # def rand(self, args):
    #     # if self.level.noRandom:
    #     #     raise Exception('RAND not allowed here')
    #     args = self.typeArgs(args, ['R/N', 'R/N', 'R'])
    #     if type(args[0]) != int or type(args[1]) != int:
    #         raise Exception('NUMERIC VALUE REQUIRED')
    #     self.registers[args[2]].assign(randint(args[0], args[1]))

            # CORE

    def eval(self, cyc):
        if self.cycle < cyc and self.line < len(self.code):
            print(self)
            line = self.code[self.line]
            if line[0] not in ['TEST', 'VOID', 'NOOP', 'NOTE', 'MARK']:
                getattr(self, line[0].lower())(line[1:])
            elif line[0] == 'VOID':
                if line[1] == 'M':
                    self.voidm()
                elif line[1] == 'F':
                    self.voidf()
            elif line[0] == 'TEST':
                if line[1] == 'EOF':
                    self.testeof()
                elif line[1] == 'MRD':
                    self.testmrd()
                else:
                    if line[2] == '=':
                        self.teste([line[1], line[3]])
                    if line[2] == '>':
                        self.testg([line[1], line[3]])
                    if line[2] == '<':
                        self.testl([line[1], line[3]])
            self.line += 1
            self.cycle += 1
            if self.line == len(self.code):
                print(self)