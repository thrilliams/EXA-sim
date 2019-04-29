from sys import argv
from level import Level
import json

file = open(argv[1])
data = json.loads(file.read())
file.close()

for i in range(len(data['exas'])):
    file = open(data['exas'][i])
    data['exas'][i] = file.read().split('\n')
    file.close()

Level(data)