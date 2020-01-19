import matplotlib.pyplot as plt

class Mortgage(object):
    def __init__(self,discount):
        self.mortgageRate = 0.048
        self.discount = discount
        self.LPR = 0.048
        self.difference = 0

    def LPRChange(self):
        self.difference = self.mortgageRate * self.discount - self.LPR


    def interestRate(self):
        result = []
        interestRate = 0
        while interestRate <= 0.1:
            result.append(interestRate)
            interestRate += 0.0001
        return result

    def originalRateList(self):
        result = []
        interestRate = 0
        while interestRate <= 0.1:
            result.append(interestRate * self.discount)
            interestRate += 0.0001
        return result

    def changedRateList(self):
        self.LPRChange()
        result = []
        interestRate = 0
        while interestRate <= 0.1:
            result.append(interestRate + self.difference)
            interestRate += 0.0001
        return result


upperBound = Mortgage(1.3)
lowerBound = Mortgage(0.7)

plt.plot(upperBound.changedRateList(),label = "1.3 LPR")
plt.plot(upperBound.originalRateList(),label = "1.3 origin")
plt.plot(lowerBound.changedRateList(),label = "0.7 LPR")
plt.plot(lowerBound.originalRateList(),label = "0.7 origin")
plt.plot(lowerBound.interestRate(),label = "interest rate")
plt.axhline(y = 0.048 * 1.3, color = "r")
plt.axhline(y = 0.048 * 0.7, color = "r")
plt.legend()
plt.show()


