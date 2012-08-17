#from datetime import date
class Stock:
	mgsy = 0 #EPS TTM
	mgjzc = 0 #booking value MRQ
	pe = 0;#dynamic PE
	lastYearPe = 0#last year static PE
	pb = 0;
	ps = 0;#price/sales ratio
	rank = 0;
	lastUpdate = '';
	totalCap = 0;
	floatingCap = 0;
	date = '';
	close = 0 ;
	openPrice = 0;
	volume = 0;
	hasGap = False;
	name = '';
	yearHigh = 0;
	yearLow = 0;
	PercentChangeFromYearLow = '';
	PercebtChangeFromYearHigh = '';
	FiftydayMovingAverage = 0;
	TwoHundreddayMovingAverage = 0;
	PercentChangeFromTwoHundreddayMovingAverage = '';
	PercentChangeFromFiftydayMovingAverage = '';
	alert = False;
	state = 'OK'#OK,WARNING,CRITICAL,UP
	def __init__(self,code,current=0,percent=0,low=0,high=0):
		self.code = code
		self.current = current
		self.percent = percent
		self.low = low
		self.high = high
		
	def __str__(self):
		#self.pe = self.current/self.mgsy
		return self.code+'**now:'+str(self.current)+'**state:'+self.state+'**percent:'+str('%.2f'%self.percent+'%')+'**high:'+str('%.2f'%self.high)+'**low:'+str('%.2f'%self.low)+'**alarm:'+str(self.alert)+'**open:'+str('%.2f'%self.openPrice)+'**close:'+str('%.2f'%self.close)+'**volume:'+str(self.volume)+'**PE:'+str('%.2f'%self.pe)+'**PB:'+str('%.2f'%self.pb)+'**rank:'+str('%.2f'%self.rank)+'**EPS:'+str(self.mgsy)+'**mgjzc:'+str(self.mgjzc)+'**last:'+str(self.lastUpdate)+'**totalCap:'+str('%.2f'%(self.totalCap/10000))+'**marketCap:'+str('%.2f'%(self.floatingCap/10000))+'**date:'+str(self.date)
	
	def shortStr(self):
		return self.code+str('|%.2f'%self.percent+'%')+'**state:'+self.state+'**now:'+str(self.current)+'**high:'+str('%.2f'%self.high)+'**low:'+str('%.2f'%self.low)
	
	def compute(self):
		if (self.lastUpdate.find('03-31')!= -1):
			self.pe = self.current/(float(self.mgsy)*4)
			#print '03-31'			
		elif (self.lastUpdate.find('06-30')!= -1):
			self.pe = self.current/(float(self.mgsy)*4/2)
			#print '06-30'			
		elif (self.lastUpdate.find('09-30')!= -1):
			self.pe = self.current/(float(self.mgsy)*4/3)	
			#print '09-30'		
		elif (self.lastUpdate.find('12-31')!= -1):
			self.pe = self.current/float(self.mgsy)	
			#print '12-31'
		if (self.mgjzc!= 0):
			self.pb = self.current/float(self.mgjzc)
		self.rank = self.pe * self.pb
		pass 

if __name__ == "__main__":
	stock = Stock('601766')
	print stock
	