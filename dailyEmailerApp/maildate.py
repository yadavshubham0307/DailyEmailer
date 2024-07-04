from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


'''
This Script class generate the message date in string according to finder type 
'''

class DateFinder:
    msg_sent_time = "21:13:00"   #write Daiy cron job running time
    time_format ="%H:%M:%S"
    msg_sent_time_object = datetime.strptime(msg_sent_time,time_format).time()
    date_format = "%Y-%m-%d"
    current_datetime = datetime.now()
    
    def __init__(self,schdOn,schdType,finderType):
        self.schdOn = schdOn
        self.schdType = schdType
        self.finderType = finderType
        print(f"maildate data : {self.schdOn}, {self.schdType}, {self.finderType}")
        self.findDate = self.datefinder()
        
    def  __str__(self):
        if self.finderType == 'current':
            if self.findDate != str(self.current_datetime.date()):
                return ""
        return str(self.findDate)
                
        
    #main function of find date    
    def datefinder(self):
        if self.schdType == 'Once':
            return self.onceDate()
        elif self.schdType == 'Daily':
            return self.dailyDate()
        elif self.schdType == 'Weekly':
            return self.weeklyDate()
        elif self.schdType == 'Monthly':
            return self.monthlyDate()
        elif self.schdType == 'Yearly':
            return self.YearlyDate()
        else:
            return ''
        
    #Function find the date for Once type mail transfer
    def onceDate(self):
        msg_date = datetime.strptime(self.schdOn,self.date_format)
        if msg_date.date() == self.current_datetime.date():
            if (self.msg_sent_time_object > self.current_datetime.time() or self.finderType == 'current'):
                return self.schdOn
            
        elif(msg_date.date() > self.current_datetime.date()):
            return self.schdOn
        
        return ''
    
    #Function find the date for Daily type mail transfer
    def dailyDate(self):
        if (self.msg_sent_time_object < self.current_datetime.time() and self.finderType == 'pending'):
            return str(self.current_datetime.date()+timedelta(days=1))
        else:
            return str(self.current_datetime.date())
        
    #Function find the date for Weekly type mail transfer    
    def weeklyDate(self):
        weekday = {
            "Monday" : 0,
            "Tuesday" : 1,
            "Wednusday" : 2,
            "Thrusday" : 3,
            "Friday" : 4,
            "Saturday" : 5,
            "Sunday" : 6,
        }
        curr_week_num = self.current_datetime.date().weekday()
        
        if(weekday[self.schdOn] > curr_week_num):
            adddays = weekday[self.schdOn]-curr_week_num
            return str(self.current_datetime.date()+timedelta(days=adddays))
            
        elif(weekday[self.schdOn] < curr_week_num):
            adddays = 7-curr_week_num + weekday[self.schdOn]
            return str(self.current_datetime.date()+timedelta(days=adddays))
            
        else:
           
            if (self.msg_sent_time_object > self.current_datetime.time() or self.finderType == 'current'):
               
                return str(self.current_datetime.date())
                
            else:
                
                return str(self.current_datetime.date()+timedelta(days=7))
            
    #Function find the date for Monthly type mail transfer 
    def monthlyDate(self):
        if(self.current_datetime.date().day == int(self.schdOn)):
            if (self.msg_sent_time_object > self.current_datetime.time() or self.finderType == 'current'):
                return str(self.current_datetime.date())
            else:
                dateMake = f"{self.current_datetime.date().year}-{self.current_datetime.date().month}-{self.schdOn:02}"
                makedDate = datetime.strptime(dateMake,self.date_format)
                return str(makedDate.date()+relativedelta(months=1))
        elif(self.current_datetime.date().day > int(self.schdOn)):
            dateMake = f"{self.current_datetime.date().year}-{self.current_datetime.date().month:02}-{self.schdOn:02}"
            makedDate = datetime.strptime(dateMake,self.date_format)
            return str(makedDate.date()+relativedelta(months=1))
        else:
            dateMake = f"{self.current_datetime.date().year}-{self.current_datetime.date().month:02}-{self.schdOn:02}"
            return dateMake
        
    #Function find the date for Yearly type mail transfer 
    def YearlyDate(self):
        msg_date = datetime.strptime(self.schdOn,self.date_format)
        if msg_date.date().day == self.current_datetime.date().day and msg_date.date().month == self.current_datetime.date().month:
            if (self.msg_sent_time_object > self.current_datetime.time() or self.finderType == 'current'):
                return str(self.current_datetime.date())
            else:
                nextDate = self.current_datetime.date() + relativedelta(years=1)
                return str(nextDate)
        elif(msg_date.date().month <= self.current_datetime.date().month):
            return f"{self.current_datetime.date().year+1}-{msg_date.date().month:02}-{msg_date.date().day:02}"
        else:
            return f"{self.current_datetime.date().year}-{msg_date.date().month:02}-{msg_date.date().day:02}"
        
        
    
        
                