"""
@author: Sean Wang: xiao.wang@symbio.com

This demo is written according to the two demos in selenium AndroidDriver wiki:

http://code.google.com/p/selenium/wiki/AndroidDriver#Run_the_Tests
and
http://code.google.com/p/selenium/wiki/AndroidDriver#Using_the_Android_Test_Framework

to demostrate that why I implement Selenium AndroidDriver for  Python Client:
Python is so simple and elegant 
"""

import unittest
from selenium import webdriver

class Test(unittest.TestCase):

    def setUp(self):
        self.driver=webdriver.Android()        
        self.driver.implicitly_wait(30)
        self.driver.get("http://www.google.com.hk")

    def tearDown(self):
        self.driver.quit()

    def testDemo(self):
        searchBox=self.driver.find_element_by_name('q')
        searchBox.send_keys("Symbio")
        searchBox.submit()
        print "Page title is: %s"%self.driver.title
        #Ensure the title contains "Google"
        self.assertTrue("Google" in self.driver.title)
        #Ensure that there is at least one link with the keyword "Symbio"
        self.assertTrue(len(self.driver.find_elements_by_partial_link_text("Symbio"))>0)

if __name__ == "__main__":
    unittest.main()
