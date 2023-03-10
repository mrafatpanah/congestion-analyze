import matplotlib.pyplot as plt
from math import ceil
import os

cwndDict04 = {"reno": [0] * 1001, "cubic": [0] * 1001, "yeah": [0] * 1001}
cwndDict15 = {"reno": [0] * 1001, "cubic": [0] * 1001, "yeah": [0] * 1001}
goodputDict04 = {"reno": [0] * 1001, "cubic": [0] * 1001, "yeah": [0] * 1001}
goodputDict15 = {"reno": [0] * 1001, "cubic": [0] * 1001, "yeah": [0] * 1001}
rttDict04 = {"reno": [0] * 1001, "cubic": [0] * 1001, "yeah": [0] * 1001}
rttDict15 = {"reno": [0] * 1001, "cubic": [0] * 1001, "yeah": [0] * 1001}
lostDict04 = {"reno": [0] * 1001, "cubic": [0] * 1001, "yeah": [0] * 1001}
lostDict15 = {"reno": [0] * 1001, "cubic": [0] * 1001, "yeah": [0] * 1001}


def splitFile(filename):
	lines = []
	file = open(filename, 'r')
	line = file.readline()
	while line:
		lines.append(line.split())
		line = file.readline()
	return lines

def adjustArray(arr, defaultVal):
	for i in range(len(arr)):
		if arr[i] == defaultVal:
			arr[i] = arr[i-1] if i != 0 else 0
	return arr

def splitCWND(data):
	cwnds04 = [-1] * 1001
	cwnds15 = [-1] * 1001
	for line in data:
		if 'cwnd_' in line:
			indexes = [0,6]
			if line[1] == '0':
				cwnds04[ceil(float(line[0]))] = float(line[6])
			else:
				cwnds15[ceil(float(line[0]))] = float(line[6])
	cwnds04 = adjustArray(cwnds04, -1)
	cwnds15 = adjustArray(cwnds15, -1)

	return cwnds04, cwnds15

def splitAcks(data):
	acks04 = ['none'] * 1001
	acks15 = ['none'] * 1001
	for line in data:
		if 'ack_' in line:
			if line[1] == '0':
				acks04[ceil(float(line[0]))] = int(line[-1])
			else:
				acks15[ceil(float(line[0]))] = int(line[-1])
	return adjustArray(acks04, 'none'), adjustArray(acks15, 'none')

def splitLost(data):
	lost04 = [-1] * 1001
	lastLost04 = 0
	lost15 = [-1] * 1001
	lastLost15 = 0
	for line in data:
		if line[0] == 'd':
			if line[-4][0] == '0':
				lastLost04 += 1
				lost04[ceil(float(line[1]))] = lastLost04
			elif line[-4][0] == '1':
				lastLost15 += 1
				lost15[ceil(float(line[1]))] = lastLost15
	return adjustArray(lost04, -1), adjustArray(lost15, -1)

def splitRtt(data):
	rtt04 = [-1] * 1001
	rtt15 = [-1] * 1001
	for line in data:
		if 'rtt_' in line:
			if line[1] == '0':
				rtt04[ceil(float(line[0]))] = float(line[-1])
			else:
				rtt15[ceil(float(line[0]))] = float(line[-1])
	return adjustArray(rtt04, -1), adjustArray(rtt15, -1)

def addCwndDatas(renoData, cubicData, yeahData):
	global cwndDict04, cwndDict15
	renoCwnds04, renoCwnds15 = splitCWND(renoData)
	cubicCwnds04, cubicCwnds15 = splitCWND(cubicData)
	yeahCwnds04, yeahCwnds15 = splitCWND(yeahData)

	for i in range(1001):
		cwndDict04['reno'][i] += renoCwnds04[i]
		cwndDict04['cubic'][i] += cubicCwnds04[i]
		cwndDict04['yeah'][i] += yeahCwnds04[i]
		cwndDict15['reno'][i] += renoCwnds15[i]
		cwndDict15['cubic'][i] += cubicCwnds15[i]
		cwndDict15['yeah'][i] += yeahCwnds15[i]

def addGoodputDatas(renoData, cubicData, yeahData):
	global goodputDict04, goodputDict15
	renoGoodputs04, renoGoodputs15 = splitAcks(renoData)
	cubicGoodputs04, cubicGoodputs15 = splitAcks(cubicData)
	yeahGoodputs04, yeahGoodputs15 = splitAcks(yeahData)

	for i in range(1001):
		goodputDict04['reno'][i] += renoGoodputs04[i]
		goodputDict04['cubic'][i] += cubicGoodputs04[i]
		goodputDict04['yeah'][i] += yeahGoodputs04[i]
		goodputDict15['reno'][i] += renoGoodputs15[i]
		goodputDict15['cubic'][i] += cubicGoodputs15[i]
		goodputDict15['yeah'][i] += yeahGoodputs15[i]

def addRttDatas(renoData, cubicData, yeahData):
	global rttDict04, rttDict15
	renoRtts04, renoRtts15 = splitRtt(renoData)
	cubicRtts04, cubicRtts15 = splitRtt(cubicData)
	yeahRtts04, yeahRtts15 = splitRtt(yeahData)

	for i in range(1001):
		rttDict04['reno'][i] += renoRtts04[i]
		rttDict04['cubic'][i] += cubicRtts04[i]
		rttDict04['yeah'][i] += yeahRtts04[i]
		rttDict15['reno'][i] += renoRtts15[i]
		rttDict15['cubic'][i] += cubicRtts15[i]
		rttDict15['yeah'][i] += yeahRtts15[i]

def addLostDatas(renoData, cubicData, yeahData):
	global lostDict04, lostDict15
	renoLosts04, renoLosts15 = splitLost(renoData)
	cubicLosts04, cubicLosts15 = splitLost(cubicData)
	yeahLosts04, yeahLosts15 = splitLost(yeahData)

	for i in range(1001):
		lostDict04['reno'][i] += renoLosts04[i]
		lostDict04['cubic'][i] += cubicLosts04[i]
		lostDict04['yeah'][i] += yeahLosts04[i]
		lostDict15['reno'][i] += renoLosts15[i]
		lostDict15['cubic'][i] += cubicLosts15[i]
		lostDict15['yeah'][i] += yeahLosts15[i]

def runOneEpoch():
	os.system("cd ./reno/; ns ./reno.tcl")
	os.system("cd ./cubic/; ns ./cubic.tcl")
	os.system("cd ./yeah/; ns ./yeah.tcl")

	renoData = splitFile('./reno/renoTrace.tr')
	cubicData = splitFile('./cubic/cubicTrace.tr')
	yeahData = splitFile('./yeah/yeahTrace.tr')

	addCwndDatas(renoData, cubicData, yeahData)
	addGoodputDatas(renoData, cubicData, yeahData)
	addRttDatas(renoData, cubicData, yeahData)
	addLostDatas(renoData, cubicData, yeahData)

def calcAvgVars():
	global cwndDict04, cwndDict15, goodputDict04, goodputDict15
	for key in cwndDict04.keys():
		for i in range(1001):
			cwndDict04[key][i] /= 10
			cwndDict15[key][i] /= 10
			goodputDict04[key][i] /= 10
			goodputDict15[key][i] /= 10
			rttDict04[key][i] /= 10
			rttDict15[key][i] /= 10
			lostDict04[key][i] /= 10
			lostDict15[key][i] /= 10

def run():
	for i in range(10):
		runOneEpoch()
	calcAvgVars()

def analyzeCWND():
	global cwndDict04, cwndDict15
	colors = ['c', 'm', 'y', 'g', 'b', 'r']
	plt.figure()
	for key in cwndDict04.keys():
		plt.plot(range(1001), cwndDict04[key], label=key+'04', c = colors[-1])
		colors.pop()
		plt.plot(range(1001), cwndDict15[key], label=key+'15', c = colors[-1])
		colors.pop()
	
	plt.xlabel("time") 
	plt.ylabel("CWND") 
	plt.title("CWND per second") 
	plt.legend() 
	plt.show() 

def derivative(arr):
	arr2 = [0] * len(arr)
	for i in range(1, len(arr)):
		arr2[i] = arr[i] / i 
	arr2[0] = arr[0]
	return arr2

def difference(arr):
	arr2 = [0] * len(arr)
	for i in range(1, len(arr)):
		arr2[i] = arr[i] - arr[i-1]
	arr2[0] = arr[0]
	return arr2

def analyzeGoodPut():
	global goodputDict04, goodputDict15
	colors = ['c', 'm', 'y', 'g', 'b', 'r']
	plt.figure()
	for key in goodputDict04.keys():
		plt.plot(range(1001),derivative(goodputDict04[key]), label=key+'04', c = colors[-1])
		colors.pop()
		plt.plot(range(1001), derivative(goodputDict15[key]), label=key+'15', c = colors[-1])
		colors.pop()
	
	plt.xlabel("time") 
	plt.ylabel("Goodput rate") 
	plt.title("Goodput rate per second") 
	plt.legend() 
	plt.show() 

	# colors = ['c', 'm', 'y', 'g', 'b', 'r']
	# for key in goodputDict04.keys():
	# 	plt.plot(range(1001),difference(goodputDict04[key]), label=key+'04', c = colors[-1])
	# 	colors.pop()
	# 	plt.plot(range(1001), difference(goodputDict15[key]), label=key+'15', c = colors[-1])
	# 	colors.pop()

	# plt.xlabel("time") 
	# plt.ylabel("Goodput rate") 
	# plt.title("Goodput rate per second") 
	# plt.legend() 
	# plt.show() 


def analyzeRtt():
	global rttDict04, rttDict15
	colors = ['c', 'm', 'y', 'g', 'b', 'r']
	plt.figure()
	for key in rttDict04.keys():
		plt.plot(range(1001), rttDict04[key], label=key+'04', c = colors[-1])
		colors.pop()
		plt.plot(range(1001), rttDict15[key], label=key+'15', c = colors[-1])
		colors.pop()

	plt.xlabel("time") 
	plt.ylabel("RTT rate") 
	plt.title("RTT rate per second") 
	plt.legend() 
	plt.show() 

def analyzeLost():
	global lostDict04, lostDict15
	colors = ['c', 'm', 'y', 'g', 'b', 'r']
	plt.figure()
	for key in lostDict04.keys():
		plt.plot(range(1001),derivative(lostDict04[key]), label=key+'04', c = colors[-1])
		colors.pop()
		plt.plot(range(1001), derivative(lostDict15[key]), label=key+'15', c = colors[-1])
		colors.pop()

	plt.xlabel("time") 
	plt.ylabel("Packet loss rate") 
	plt.title("Packet loss rate per second") 
	plt.legend() 
	plt.show() 

	# colors = ['c', 'm', 'y', 'g', 'b', 'r']
	# for key in lostDict04.keys():
	# 	plt.plot(range(1001),difference(lostDict04[key]), label=key+'04', c = colors[-1])
	# 	colors.pop()
	# 	plt.plot(range(1001), difference(lostDict15[key]), label=key+'15', c = colors[-1])
	# 	colors.pop()

	# plt.xlabel("time") 
	# plt.ylabel("Packet loss rate") 
	# plt.title("Packet loss rate per second") 
	# plt.legend() 
	# plt.show() 


run()
analyzeCWND()
analyzeGoodPut()
analyzeRtt()
analyzeLost()