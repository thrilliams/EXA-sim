class Register:
    def __init__(self, val):
        self.val = val
    def __repr__(self):
        return str(self.val)
    def value(self):
        return self.val
    def assign(self, val):
        if type(val) == int:
            if val > 9999:
                val = 9999
            if val < -9999:
                val = -9999
        self.val = val

class File(Register):
    def __init__(self, data, id, host):
        self.data = data
        self.id = id
        self.host = host
        self.index = 0
    def __repr__(self):
        return str(self.id)
    def reprlong(self):
        return ', '.join(self.data)
    def value(self):
        try:
            v = self.data[self.index]
        except IndexError:
            raise Exception('FILE ACCESS OUT OF RANGE')
        self.index += 1
        return v
    def assign(self, val):
        if type(val) == int:
            if val > 9999:
                val = 9999
            if val < -9999:
                val = -9999
        if self.index == len(self.data):
            self.data.append(val)
        else:
            self.data[self.index] = val
        self.index += 1
    def seek(self, index):
        self.index += index
        if self.index > len(self.data):
            self.index = len(self.data)
        if self.index < 0:
            self.index = 0
    def void(self):
        try:
            self.data.pop(self.index)
        except IndexError:
            raise Exception('FILE ACCESS OUT OF RANGE')
    def wipe(self):
        self.data = []
        self.index = 0
    def eof(self):
        return self.index == len(self.data)
    def link(self, host):
        self.host = host

class Communication(Register):
    def __init__(self, scope, parent):
        self.scope = scope
        self.parent = parent
        self.val = None
    def __repr__(self):
        return str(self.val)
    def value(self):
        if self.scope == 'GLOBAL':
            scope = 'GLOBAL'
        else:
            scope = parent.host
        level.m[scope].reading = True
        if level.m[scope].writing:
            level.m[scope].writing = False
            return level.m[scope].val
        else:
            parent.cycle += 1
            return self.value()
    def assign(self, val):
        if self.scope == 'GLOBAL':
            scope = 'GLOBAL'
        else:
            scope = parent.host
        level.m[scope].writing = True
        if level.m[scope].reading:
            level.m[scope].reading = False
            level.m[scope].val = val
        else:
            parent.cycle += 1
            self.assign(val)
    def mode(self):
        if self.mode == 'GLOBAL':
            self.mode = 'LOCAL'
        else:
            self.mode = 'GLOBAL'
    def mrd(self):
        if self.scope == 'GLOBAL':
            scope = 'GLOBAL'
        else:
            scope = parent.host
        return level.m[scope].writing