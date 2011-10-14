#!/usr/bin/python
#
# Copyright 2011 Webdriver_name committers
# Copyright 2011 Google Inc.
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
import subprocess
from subprocess import PIPE
import time
import os
import signal
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common import utils

class Service(object):
    """ Object that manages the starting and stopping of the AndroidDriver """


    def __init__(self,device):
        """ Creates a new instance of the Service
            Args:
                device: serial ID of the Android device. \
                        Could be seen by command android devices. \
                        If only one device connected. you do not need to assign
        """

        self.device = device 
    def start(self):
        """ Starts the AndroidDriver Service. 
            @Exceptions
                WebDriverException : Raised either when it can't start the service
                    or when it can't connect to the service"""

        try:
            self.process = subprocess.Popen(r'adb forward tcp:8080 tcp:8080',stdout=PIPE, stderr=PIPE)
        except:
            raise WebDriverException(
                "AndroidDriver needs Android SDK. \
                Please download from http://developer.android.com/sdk/index.html\
                and add directories 'tools' and 'platform-tools' in PATH.")

        try:
            self.process = subprocess.Popen(r'adb shell am start -n org.openqa.selenium.android.app/.MainActivity ',
                    stdout=PIPE, stderr=PIPE)
        except:
            raise WebDriverException(
                "AndroidDriver needs to be installed on device.\
                Download android-server-2.x.apk \
                from http://code.google.com/p/selenium/downloads/list")
        count = 0
        while not utils.is_connectable(8080):
            count += 1
            time.sleep(1)
            if count == 30:
                 raise WebDriverException("Can not connect to the AndroidDriver")
    @property
    def service_url(self):
        """ Gets the url of the ChromeDriver Service """
        return "http://localhost:8080/wd/hub"

    def stop(self):
        """ Close AndroidDriver by sending BACK keyevent to device"""
        try:
            self.process = subprocess.Popen(r'adb shell input keyevent 4',stdout=PIPE, stderr=PIPE)
        except:
            print 'AndroidDriver was not closed, close by yourself by tapping back key to exit AndroidDriver on device.'


