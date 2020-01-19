class BigSaving(object):
    def __init__(self,savingAmount,rate):
        self.savingAmount = savingAmount
        self.inerestAcummulated = 0
        self.rate = rate
        self.monthDays = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}


    def resultDisplay(self):
        print("saving amount = "+str(self.savingAmount))

    def interestWithdraw3YearsLater(self):
        self.savingAmount = self.savingAmount*(1+self.rate*3)
        self.resultDisplay()

    def interestDepositEveryMonth(self,moneyMarketRate):
        for year in range(3):
            for month in range(1,13):
                self.inerestAcummulated += self.inerestAcummulated*(moneyMarketRate*self.monthDays[month]/365) + self.savingAmount*self.rate*self.monthDays[month]/365
        self.savingAmount += self.inerestAcummulated
        self.resultDisplay()

scenario1 = BigSaving(300000,0.039)
scenario2 = BigSaving(300000,0.0379)


scenario1.interestWithdraw3YearsLater()
scenario2.interestDepositEveryMonth(0.02)

