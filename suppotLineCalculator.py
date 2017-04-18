import numpy as np
import pandas as pd
import quandl
import math
import sys

def calculateCDP(H, L, C):
	return (H + L + 2.0 * C) / 4.0

def calculatePT(H, L):
	return H - L

def calculateSupports(PH,PL, H, L, C):
	CDP = calculateCDP(H, L, C)
	PT = calculatePT(PH, PL)
	AH = CDP + PT
	NH = 2 * CDP - L
	AL = CDP - PT
	HL = 2 * CDP - H
	return (AH, NH, AL, HL)

def upOrDip(O, C):
	return (C - O) >= 0



# [main funciton]
# @params: 前日最高点， 前日最低点，昨日最高点，昨日最低点，昨日收盘价
# @params: trickerName
# 运行方法1：python supporLineCalculator.py 前日最高点， 前日最低点，昨日最高点，昨日最低点，昨日收盘价
# example: python suppotLineCalculator.py 143.35 140.06 142.15 141.01 141.80
#
# 运行方法2：python supporLineCalculator.py tricker name
# example: python suppotLineCalculator.py AAPL
if __name__ == '__main__':
	if len(sys.argv) > 2:
		sys.argv = [float(sys.argv[i]) for i in range(1,6)]
		AH, NH, AL, HL = calculateSupports(sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
		print("The support bounders for tomorrow are:")
		print("AH（最高值即强压力点）: " + str(round(AH,2)))
		print("NH（次高值即弱压力点）: " + str(round(NH,2)))
		print("AL（最低值即强支撑点）: " + str(round(AL,2)))
		print("HL（次低值即弱支撑点）: " + str(round(HL,2)))
	else:
		ticker = sys.argv[1]
		quandl.ApiConfig.api_key = '6PcspJiyEshZTzxZYgHZ'
		data = quandl.get_table('WIKI/PRICES', ticker = ticker.upper(), paginate=True)
		count = 0
		total = len(data.index)
		for i in range(3, len(data.index)):
			AH, NH, AL, HL = calculateSupports(float(data.iloc[i - 3].high), float(data.iloc[i - 3].low), float(data.iloc[i - 2].high), float(data.iloc[i - 2].low), float(data.iloc[i - 2].close))
			if (data.iloc[i - 1].close >= NH):
				if upOrDip(data.iloc[i].open, data.iloc[i].close):
					count+=1
			elif (data.iloc[i - 1].close <= HL):
				if not upOrDip(data.iloc[i].open, data.iloc[i].close):
					count+=1
			else:
				count+=1

		print("The correctness for this stock is", round((count / total) * 100, 2))

		AH, NH, AL, HL = calculateSupports(float(data.iloc[-2].high), float(data.iloc[-2].low), float(data.iloc[-1].high), float(data.iloc[-1].low), float(data.iloc[-1].close))
		print("The support bounders for tomorrow are:")
		print("AH（最高值即强压力点）: " + str(round(AH,2)))
		print("NH（次高值即弱压力点）: " + str(round(NH,2)))
		print("AL（最低值即强支撑点）: " + str(round(AL,2)))
		print("HL（次低值即弱支撑点）: " + str(round(HL,2)))

