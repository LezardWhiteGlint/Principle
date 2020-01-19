import matplotlib.pyplot as plt
import random

class BurnRateStressTest(object):
    def __init__(self,asset,burnRate,interestRate,testPeriod):
        self.asset = asset
        self.burnRate = burnRate
        self.testPeriod = testPeriod
        self.interestRate = interestRate
        self.inflationPossibility = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07]
        self.inflationHistoricalData = [0.0723,
                                        0.1881,
                                        0.1825,
                                        0.0305,
                                        0.0356,
                                        0.064,
                                        0.1461,
                                        0.243,
                                        0.1679,
                                        0.0831,
                                        0.0279,
                                        -0.0077,
                                        -0.0140,
                                        0.0035,
                                        0.0072,
                                        -0.007,
                                        0.0113,
                                        0.0382,
                                        0.0178,
                                        0.0165,
                                        0.0482,
                                        0.0593,
                                        -0.0073,
                                        0.0318,
                                        0.0555,
                                        0.0262,
                                        0.026,
                                        0.0192,
                                        0.014,
                                        0.02,
                                        0.0159,
                                        0.0207]
        self.inflationHistoricalDataAfterWTO = [-0.007,
                                                0.0113,
                                                0.0382,
                                                0.0178,
                                                0.0165,
                                                0.0482,
                                                0.0593,
                                                -0.0073,
                                                0.0318,
                                                0.0555,
                                                0.0262,
                                                0.026,
                                                0.0192,
                                                0.014,
                                                0.02,
                                                0.0159,
                                                0.0207]

    def getAsset(self):
        return self.asset

    def getInterestRate(self):
        return self.interestRate

    def getBurnRate(self):
        return self.burnRate

    def getTestPeriod(self):
        return self.testPeriod

    def getInflationRate(self, historicalData=False, afterWTO=False):
        if historicalData == False:
            return self.inflationPossibility
        elif afterWTO == False:
            return self.inflationHistoricalData
        else:
            return self.inflationHistoricalDataAfterWTO

    def currntAssetCalculator(self, asset, interestRate, inflationRate):
        result = (asset-self.getBurnRate()) * (1 + interestRate - inflationRate)
        return result

    def stressTest(self, runs=1,historicalData = False,afterWTO = False):
        minMonth = 300
        failTimes = 0
        for run in range(runs):
            remainAsset = []
            startingAsset = self.getAsset()
            testingPeriod = self.getTestPeriod()
            currentAsset = startingAsset
            interestRate = self.getInterestRate()
            inflationRateSet = self.getInflationRate(historicalData,afterWTO)
            for month in range(1, testingPeriod+1):
                inflationRate = random.choice(inflationRateSet)
                currentAsset = self.currntAssetCalculator(currentAsset,interestRate,inflationRate)
                if currentAsset < 0:
                    if minMonth > month:
                        minMonth = month
                    if month < runs:
                        failTimes += 1
                    break
                else:
                    remainAsset.append(currentAsset)

            plt.plot(remainAsset, color = "r")
        print("Asset worst case scenario last " + str(minMonth) + " month")
        print(str(((runs - failTimes)/runs)*100)+"%"+" of runs successfully last "+str(self.getTestPeriod())+" month")
        plt.show()

test = BurnRateStressTest(1000000,2000,0.025,300)
test.stressTest(5000,True,True)







