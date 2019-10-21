"""
亚马逊需求
网站  https://www.amazon.ca/
需求1：
针对特定的搜索词，收集 additional infomation  除开 shipping weight之外都要，收集20页
需求2：
跟需求1差不多，只收集additional infomation中的ID和评论数

"""
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import openpyxl


#initiate database
# client = MongoClient()
# DB = client.AmazonCA
# # Collection = DB.addtionalInformation
# Collection = DB.ChargeCableV2



class amazonSlowScrap(object):
    def __init__(self,dbName,CollectionName,searchWordsFileName,url):
        #initiate driver
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # options.add_argument('window-size=800x600')
        caps = DesiredCapabilities().CHROME
        # caps["pageLoadStrategy"] = "normal"  #  Waits for full page load
        caps["pageLoadStrategy"] = "none"  # Do not wait for full page load
        self.driver = webdriver.Chrome(desired_capabilities=caps,
                                  executable_path='/Users/lezardvaleth/Documents/Python/chromedriver', options=options)
        self.client = MongoClient()
        self.DB = self.client[dbName]
        self.Collection = self.DB[collectionName]
        self.searchWordsFileName = searchWordsFileName
        self.url = url



    def infoGetter(self,searchKeyWord,count):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="prodDetails"]/div/div[2]/div[1]/div[2]/div/div/table/tbody/tr[1]/td[2]'))
            )
            id = self.driver.find_element_by_xpath('//*[@id="prodDetails"]/div/div[2]/div[1]/div[2]/div/div/table/tbody/tr[1]/td[2]').text
            reviews = self.driver.find_element_by_xpath('//*[@id="prodDetails"]/div/div[2]/div[1]/div[2]/div/div/table/tbody/tr[2]/td[2]/span/span[3]/a').text
            rank = self.driver.find_element_by_xpath('//*[@id="SalesRank"]/td[2]').text
            dateFirstAvailable = self.driver.find_element_by_xpath('//*[@id="prodDetails"]/div/div[2]/div[1]/div[2]/div/div/table/tbody/tr[5]/td[2]').text
            post = {
                "KeyWord":searchKeyWord,
                "ID":id,
                "Reviews":reviews,
                "Rank":rank,
                "DateFirstAvailable":dateFirstAvailable
            }
            print(post)
            self.Collection.insert_one(post)
            count += 1
            print(searchKeyWord + str(count) + "get")
        except:
            print("try other place for information")
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "content"))
                )
                tables = self.driver.find_elements_by_class_name("content")
                for each in tables:
                    if "ASIN" in each.text:
                        table = each.text
                processedTable = table.split("\n")
                id = ""
                reviews = ""
                rank = ""
                dateFirstAvailable = ""
                for item in processedTable:
                    if "ASIN" in item:
                        id = item
                    if "customer review" in item:
                        reviews = item
                    if "#" in item:
                        rank += item + " and "
                    if "Date" in item:
                        dateFirstAvailable = item
                post = {
                    "KeyWord": searchKeyWord,
                    "ID": id,
                    "Reviews": reviews,
                    "Rank": rank,
                    "DateFirstAvailable": dateFirstAvailable
                }
                print(post)
                self.Collection.insert_one(post)
                count += 1
                print(searchKeyWord + str(count) + "get")
            except:
                print("still not find addtional information")

        return count




    def amazonInfo(self,searchKeyWord,pageDepth):
        count = 0

        #show search result
        self.driver.get(self.url+searchKeyWord+"&ref=nb_sb_noss")
        try:
            WebDriverWait(self.driver,10).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME,"s-image"))
            )
        except:
            pass
        while True:
            try:
                WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="n/667823011"]/span/a/span'))
                )
                department = self.driver.find_element_by_xpath('//*[@id="n/667823011"]/span/a/span')
                department.click()
                break
            except:
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="i/electronics"]/span/a/span'))
                    )
                    department = self.driver.find_element_by_xpath('//*[@id="i/electronics"]/span/a/span')
                    department.click()
                    break
                except:
                    self.driver.refresh()


        for noUse in range(pageDepth):

            try:
                WebDriverWait(self.driver, 30).until(
                    EC.visibility_of_all_elements_located((By.CLASS_NAME, "s-image"))
                )
            except:
                print("items' image not loaded fully")

            picNum = len(self.driver.find_elements_by_class_name("s-image"))


            for i in range(picNum):
                print("------------------------------"+str(i)+"--------------------")
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "s-image"))
                    )
                    items = self.driver.find_elements_by_class_name("s-image")
                    items[i].click()
                    try:
                        count = infoGetter(searchKeyWord, count)
                        self.driver.execute_script("window.history.go(-1)")
                    except TimeoutException:
                        self.driver.execute_script("window.history.go(-1)")
                        print("Cannot find the element in time")
                except:
                    print("skip due to element is not visible")
                    continue
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,"Next"))
                )
                # WebDriverWait(self.driver, 10).until(
                #     EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT,"Next"))
                # )
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_all_elements_located((By.PARTIAL_LINK_TEXT, "Next"))
                )


                nextPage = self.driver.find_elements_by_partial_link_text("Next")[-1]
                # nextPage.click()
                nextPage.send_keys('\n')
            except:
                break


    def searchListGetter(self):
        file = openpyxl.load_workbook(self.searchWordsFileName)
        sheet = file["Sheet1"]
        columA = sheet["A"][1:]
        result = []
        for word in columA:
            result.append(word.value)
        return result


    def main(self,pageCount):
        searchList = searchListGetter()
        for word in searchList:
            amazonInfo(word,pageCount)
        self.driver.quit()


