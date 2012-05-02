'''
Created on 2011-3-7

@author: simon
'''
import sys, traceback
from datetime import date

#parse real time stock price from yahoo finance
def parseFinanceData(code):
    from lxml import etree
    from lxml.html import parse
    url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22600327.SS%22)&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
    print url
    page = parse(url).getroot()
    result = etree.tostring(page)
    print result
    import io
    with io.open('test.xml','wb') as f:
       #f.writelines(result)
       pass 
    
    r = page.xpath('//div[@class="tab01"]');
    #print len(r)    
    from stock import Stock
    stock = Stock(code)
    for a in r:  
        tree= etree.ElementTree(a)  
        #print etree.tostring(tree) 
        datas = tree.xpath('//td') 
        #print len(datas)
        index =0
        for data in datas:
            dataTree = etree.ElementTree(data);
            #print etree.tostring(dataTree)
            values = dataTree.xpath('//text()')
            index +=1
            #print index
            if (len(values)==1 ):
                #print values
                #print len(values[0])
                #print str(values[0])
                if (index == 32):
                    mgsy = values[0]
                    #print mgsy+'***************'
                    stock.mgsy = mgsy
                elif (index == 52):
                    mgjzc = values[0]
                    #print mgjzc+'***************'
                    stock.mgjzc = mgjzc
                elif (index == 2):
                    last_update = values[0]
                    #print last_update
                    stock.lastUpdate = last_update                    
         
        return stock   

#get history data from yahoo finance API    
def getHistorialData(code,save = False,beginDate = '',endDate = ''):
    from lxml import etree
    from lxml.html import parse
    #yahoo stock ticker need post-fix ".SS" for Shanghai,'.SZ' for shenzheng
    if (code.startswith('6')):
        code2 = code +".SS"
    else:
        code2 = code +".SZ"
    if len(endDate) == 0:
        print "Poll all history date for "+code
        from datetime import date
        url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22'+code2+'%22%20and%20startDate%20%3D%20%22'+beginDate+'%22%20and%20endDate%20%3D%20%22'+str(date.today())+'%22&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
    else:
        url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22'+code2+'%22%20and%20startDate%20%3D%20%22'+beginDate+'%22%20and%20endDate%20%3D%20%22'+endDate+'%22&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
    print url
    page = parse(url).getroot()
    result = etree.tostring(page)
    print result
    
    r = page.xpath('//quote');
    from stock import Stock
    historyDatas = []
    from dao.stockdao import findLastUpdate
    from dao.stockdao import findOldestUpdate
    lastStock = findLastUpdate(code)
    oldestStock = findOldestUpdate(code)
    print "lastStock***"+lastStock.__str__()
    print "oldestStock***"+oldestStock.__str__()
    for a in r:  
        tree= etree.ElementTree(a)  
        #print etree.tostring(tree) 

        stock = Stock(code)           
        stock.date = tree.xpath('//date')[0].text
        stock.high = float(tree.xpath('//high')[0].text)
        stock.low = float(tree.xpath('//low')[0].text)  
        stock.openPrice = float(tree.xpath('//open')[0].text)
        stock.close = float(tree.xpath('//close')[0].text)
        stock.volume = float(tree.xpath('//volume')[0].text)
        
        isNewData = True;
        if lastStock is not None:            
            isNewData = (stock.date > lastStock['date']) or (stock.date < oldestStock['date'])
        print stock.date+'***isNewData***'+str(isNewData)
        if isNewData and save:  
            from dao.stockdao import saveStock
            saveStock(stock);
        #print stock    
        historyDatas.append(stock) 
    historyDatas.sort(key=lambda item:item.date,reverse=True) 
#    for stock in historyDatas:
#        print stock 
#    pass 
    
    for i in  range(len(historyDatas)):
        if i == len(historyDatas)-1:
            continue
        else:
            last = historyDatas[i]
            prev = historyDatas[i+1]
            if (last.openPrice!= prev.close and
                (last.low >prev.high or last.high<prev.low)):
                print "gap***"+last.__str__()               
                         

#parse all history data from yahoo
def parseAllHistoryData(file):
    import io
    with io.open(file,'rb') as f:
        list = [];
        for i in range(1000):
            line = f.readline()
            if (len(line) == 0):
                break;
            else :
                l = line.strip();
                if (len(l)==7):
                    code = l[1:]                    
                    #print len(l)  
                    #print l  
                elif (len(l) == 6):
                    code = l;                   
                else :
                    print l; 
                    continue
                
               #parse code
                try:
                    getHistorialData(code,True,'2011-01-01')                                       
                except:
                    traceback.print_exc(file=sys.stdout)
                    continue       
                

        pass
    
#lastDays: the last range to check the index,default will be 1 year's data(52 weeks),i.e,the sampling period
#newDays: the latest days trigger the index
#ex. computeNhnlIndex(file,360,3,2012-05-02) will check the 360 days trading record before 2012-05-02,
#to check if the price during the nearest 3 days trigger NH-NL index
def computeNhnlIndex(file,lastDays,nearDays,endDate = str(date.today())):
    result = {}
    import io
    with io.open(file,'rb') as f:
        nhList = [];
        nlList = [];
        nhCount = 0;
        nlCount = 0;
        for i in range(1000):
            line = f.readline()
            if (len(line) == 0):
                break;
            else :
                l = line.strip();
                if (len(l)==7):
                    code = l[1:]                    
                    #print len(l)  
                    #print l  
                elif (len(l) == 6):
                    code = l;                   
                else :
                    print l; 
                    continue
                
               #parse code
                try:
                    from dao.stockdao import triggerNhNl
                    triggered = triggerNhNl(code,lastDays,nearDays,endDate)   
                    if triggered == 1:
                        nhCount += 1;
                        nhList.append(code)
                    elif triggered == -1:
                        nlCount += 1;     
                        nlList.append(code)                                                   
                except:
                    traceback.print_exc(file=sys.stdout)
                    continue       
        
        print 'nhCount ****'+str(nhCount)+str(nhList)
        print 'nlCount ****'+str(nlCount)+str(nlList)

        pass

#compute the NHNL index between beginDate and endDate
def computeNhnlIndexWithinRange(file,lastDays,nearDays,endDate = str(date.today()),beginDate = str(date.today())):
    
    pass                    
                    
if __name__ == '__main__':
    stocks = ['600327','600739','600573','600583','600718','600827','601111','601866','600880']
#    for stock in stocks:
#        getHistorialData(stock)
#    getHistorialData('600383',True,'2011-01-01')
    
#    parseAllHistoryData('stock_list_all')
    computeNhnlIndex('stock_list_all',52*7,7)
    
#    from dao.stockdao import findAllStocks
#    findAllStocks();
#                
#    import logging
#    LOG_FILENAME = 'example.log'
#    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
#
#    logging.error('This message should go to the log file')