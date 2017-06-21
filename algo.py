'''
The trade algorithm for WealthSimple Assignment
Author: Jinhua Wang
License MIT
For simplicity purposes, this file assumes stock prices follows Brownian Motion,
and we only trade SP500. 
'''

import numpy as np

class TradeData:
	'''
		Soure of the trade data
		to simplify matters, assume that only SP500 is traded
	'''
	'''
		Assume that the stock price movement follows Brownion Motion
	'''
	def brownMotion(self, starting_price):
		T = 1 #a month
		mu = 0.1
		sigma = 0.5
		S0 = starting_price
		dt = 0.03 #every day
		N = int(round(T/dt))
		t = np.linspace(0, T, N)
		W = np.random.standard_normal(size = N) 
		W = np.cumsum(W)*np.sqrt(dt) 
		X = (mu-0.5*sigma**2)*t + sigma*W 
		S = S0*np.exp(X) 
		return S

class Account:
	cash=1000000000
	portfolio={
		"SP500":0
	}
	trans_history=[]
	def purchase(self, price, volume, day):
		self.cash = self.cash - price * volume
		self.portfolio["SP500"] = self.portfolio["SP500"] + volume
		self.trans_history.append(
			{
				"action": "buy",
				"time": day,
				"price":price,
				"volume":volume,
			}
		)
	def sell(self, price, volume, day):
		self.cash = self.cash + price * volume
		self.portfolio["SP500"] = self.portfolio["SP500"] - volume
		self.trans_history.append(
			{
				"action": "sell",
				"time": day,
				"price":price,
				"volume":volume,				
			}
		)


class Algorithm:
	stockprices=[]
	#beginning net worth
	begin_net = 0
	#ending net worth
	end_net = 0
	def __init__(self):
		# account A is for panic selling investor
		self.accountA = Account()
		# account B is for hold and sell investor
		self.accountB = Account()
		trade = TradeData()
		self.stockprices = trade.brownMotion(2436)
		#first day buy 50000 stocks 
		self.accountA.purchase(self.stockprices[0],50000,0)
		self.accountB.purchase(self.stockprices[0],50000,0)
		self.begin_netA = self.accountA.portfolio["SP500"] * self.stockprices[0] + self.accountA.cash
		self.begin_netB = self.accountB.portfolio["SP500"] * self.stockprices[0] + self.accountB.cash
	#assumes that an investor dumps all the stocks when the return drops below -2%
	def panic_sell(self):
		sell_date = -1;
		for i, price in enumerate(self.stockprices):
			if i>=1: #start from the second day
				return_daily = (self.stockprices[i]-self.stockprices[0])/self.stockprices[0] 
				if return_daily < 0.02 and self.accountA.portfolio["SP500"]>0: 
					self.accountA.sell(self.stockprices[i],self.accountA.portfolio["SP500"], i)
					sell_date = i;
				if sell_date!=-1 and i - sell_date >= 20 or i==(len(self.stockprices)-1):
					self.accountA.purchase(self.stockprices[i], 50000, i)
		#evaluate the performance 
		end_netA = self.accountA.portfolio["SP500"] + self.stockprices[len(self.stockprices)-1] + self.accountA.cash
		return_net = (end_netA - self.begin_netA) / self.begin_netA
		print "Return of panic selling strategy after 30 trading days is " + str(return_net)
		return return_net

	#assumes an investor holds when the return drops below -2%
	def hold_sell(self):
		end_netB = self.accountB.portfolio["SP500"] + self.stockprices[len(self.stockprices)-1] + self.accountB.cash
		return_net = (end_netB - self.begin_netB) / self.begin_netB
		print "Return of hold strategy after 30 trading days is " + str(return_net)
		return return_net

performance_a = []
performance_b = []
count_b_better_than_a = 0

for x in range(0, 100):
	print "\n"
	print "Simulation "+ str(x) + " results:"
	a = Algorithm()
	return_a = a.panic_sell()
	performance_a.append(return_a)
	return_b = a.hold_sell()
	performance_b.append(return_b)
	print "\n"

print "simulation finished \n"

print "there are " + str(len(performance_a)) + " cases in total"

for i, val in enumerate(performance_a):
	if performance_b[i]>performance_a[i]:
		count_b_better_than_a = count_b_better_than_a+1

percentage = float(count_b_better_than_a)/len(performance_a) * 100

print "In "+ str(percentage) + "% of 100 cases, hold strategy performs better than panic sell strategy \n\n"