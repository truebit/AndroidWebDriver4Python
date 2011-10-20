#!/usr/bin/python
#
# Copyright 2011 Webdriver_name committers
# Copyright Sean Wang : xiao.wang@symbio.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.command import Command
from service import Service

class WebDriver(RemoteWebDriver):

    def __init__(self,deviceID=None,port=0):
        self.service = Service(deviceID,port=port)
        self.service.start()
        RemoteWebDriver.__init__(self,
            command_executor=self.service.service_url,
            desired_capabilities=DesiredCapabilities.ANDROID)

    def quit(self):
        """ Close AndroidDriver application on device"""
        try:
            RemoteWebDriver.quit(self)
        except httplib.BadStatusLine:
            pass
        finally:
            self.service.stop()
if __name__ == '__main__':
    #driver= WebDriver('emulator-5554')
    driver= WebDriver()
    driver.get("http://www.symbio.com")
    driver.quit()
