import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
matplotlib.use('TKAgg')
import sys
import random
import requests, thread, threading, time, timeit
import re
import csv
from collections import defaultdict

columns = defaultdict(list) # each value in each column is appended to a list
#FOR JUNE 9
with open('data.csv', 'rb') as f:# extracting columns from csv
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value
            columns[k].append(v)

name = columns["Name"]
load = columns["Load"]
testload = []

listofIndex = [i for i, x in enumerate(name) if x == "N.Y.C."]

for each in listofIndex:
    testload.append(load[each])

#####=====================
columns1 = defaultdict(list)
with open('data1.csv', 'rb') as file: # extracting columns from csv
    reader1 = csv.DictReader(file) # read rows into a dictionary format
    for row in reader1: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            columns1[k].append(v) 

name1 = columns1["Name"]
load1 = columns1["Load"]

listofIndex1 = [i for i, y in enumerate(name1) if y == "N.Y.C."]

for each in listofIndex1:
	testload.append(load1[each])
#####=====================

nydata = iter(testload)

fig = plt.figure("Smart Meter POC- Jantsan")
ax1 = fig.add_subplot(1, 1, 1)
# d ax1.clear()
ax1.grid()

ax1.set_xlabel('Time(N)')
ax1.set_ylabel('LOAD (Reference/No Unit)')

#ax1.plot([], [], color='red', linewidth=3.0, label='Random')
ax1.plot([], [], color='blue', linewidth=2.0, label='SM#1')
ax1.plot([], [], color='cyan', linewidth=2.0, label='SM#2')
ax1.plot([],[], color = 'green', linewidth = 2.0, label = 'NYC LOAD')

ax1.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)

x = []
#data = []
data1 = []
data2 = []
data3 = []
val1 = 0
val2 = 0

print 'INITIATING JANTSANKHORLOO SMART METERING DEMO...'
photon1 = requests.get('') #1st photon access token goes here

number_result1 = map(int, (re.findall('\d+', photon1.content)))
val1 = number_result1[0]

photon2 = requests.get('') #2nd photon access token goes here

print 'Load completed'
number_result2 = map(int, (re.findall('\d+', photon2.content)))
val2 = number_result2[0]

print number_result1[0]
print number_result2[0]

def photon1Req():
    global val1
    while True:
        photon1 = requests.get('') # 1st photon access token
        number_result1 = map(int, (re.findall('\d+', photon1.content)))
        val1 = number_result1[0]

        print 'Photon 1:', val1  # Photon1
        #d time.sleep(1)
    return #d number_result1[0]

def photon2Req():
    global val2
    while True:
        photon2 = requests.get('') #2nd photon access token goes between the strings
        number_result2 = map(int, (re.findall('\d+', photon2.content)))
        val2 = number_result2[0]

        print 'Photon 2:', val2
        #d time.sleep(1)
    return

def animate(i):
    temp = float(next(nydata)) - 2000

    x.append(i)

    #data.append(random.random() * 1000 - random.random() * 100 + 4000)
    data1.append(val1) #d number_result1[0])  # d
    data2.append(val2) #d number_result2[0])  # d random.random()*2000)
    data3.append(temp)

    #ax1.plot(x, data, color='red', linewidth=3.0, label='Random')
    ax1.plot(x, data1, color='blue', linewidth=2.0, label='SM#1')
    ax1.plot(x, data2, color='cyan', linewidth=2.0, label='SM#2')
    ax1.plot(x, data3, color='green', linewidth=2.0, label='NYC LOAD')
    return

def main():
    netThread1 = threading.Thread(target = photon1Req)
    netThread2 = threading.Thread(target = photon2Req)
    netThread1.start()
    netThread2.start()
    ani = animation.FuncAnimation(fig, animate, interval=500)
    plt.show()
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
        print 'KeyboardInterrtup caught'

if __name__=='__main__':
    main()
