from pymongo import MongoClient
import openpyxl
from openpyxl import Workbook

# client = MongoClient()
# DB = client.AmazonCA
# Collection = DB.ChargeCableV2

wb = Workbook()

fileName = "USBChargerCA.xlsx"

class Output(object):
    def __init__(self,fileName,dbName,collectionName):
        self.client = MongoClient()
        self.fileName = fileName
        self.DB = self.client[dbName]
        self.Collection = self.DB[collectionName]

    def getAllRecord(self):
        return self.Collection.find()

    def xlsxOutput(self):
        wb = Workbook()

