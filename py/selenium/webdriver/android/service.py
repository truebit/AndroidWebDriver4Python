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
import subprocess
from subprocess import PIPE
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common import utils



class Service(object):
    """ Object that manages the starting and stopping of the AndroidDriver """
    CMD_NOT_IN_PATH = """Could not find adb command, AndroidDriver needs Android SDK.
            Please download from http://developer.android.com/sdk/index.html
            and add directories 'tools' and 'platform-tools' in PATH."""

    ANDROID_DRIVER_CLIENT_APP_CMP= r'org.openqa.selenium.android.app/.MainActivity'

    def __init__(self,device=None):
        """ Creates a new instance of the Service
            Args:
                device: serial ID of the Android device.
                        Could be seen by command 'android devices'.
                        If only one device connected. you do not need to assign it
        """
        self.device= Service.initDevice(device)
        self.adbCmd= r'adb -s %s '%self.device

    @staticmethod
    def initDevice(deviceID=None):
        deviceInfo = []
        # as adb server launching process made the script stuck,
        # so I use hard-coded wait time to make it through
        # I do not know why subprocess could not get output in such situation
        cmd1= 'adb kill-server'
        cmd2= 'adb start-server'
        cmd3= 'adb devices'
        ret=subprocess.call(cmd1,stdout=PIPE, stderr=PIPE,shell=True)
        if ret:
            raise WebDriverException(Service.CMD_NOT_IN_PATH)
        p=subprocess.Popen(cmd2,stdout=PIPE, stderr=PIPE,shell=True)
        count=0
        while count<30:
            time.sleep(1)
            if p.poll() is 0:
                break
        else:
            raise WebDriverException("adb could not get device info after 30 seconds.")
        output=subprocess.check_output(cmd3,shell=True).split()[4:]
        for i, v in enumerate(output):
            if i + 1 < len(output) and i % 2 == 0:
                deviceInfo.append((v, output[i + 1]))
        if deviceInfo:
            # check if all devices are online
            if 'device' not in [i[1] for i in deviceInfo]:
                raise WebDriverException( """No device is good to go.
                Reconnect devices and retry.
                Only a deviceID followed with 'device' would work.""")
            if deviceID:
                # check if device with given deviceID is connected
                if deviceID in [i[0] for i in deviceInfo]:
                    #print "Connected to %s..." % deviceID
                    return deviceID
                else:
                    raise WebDriverException("""No device with serial ID '%s' found.
                    Plz make sure you got the right ID."""%deviceID)
            else:
                for i in deviceInfo:
                    if i[1] =='device':
                        #print "Connected to %s..." % i[0]
                        return i[0] 
        else:
            raise WebDriverException("""No devices found.
            plz make sure you have attached devices""")

    def start(self):
        """ Starts the AndroidDriver Service. 
            @Exceptions
                WebDriverException : Raised either when it can't start the service
                    or when it can't connect to the service"""

        #print 'start tcp port 8080 forwarding'
        subprocess.call('%s forward tcp:8080 tcp:8080'%self.adbCmd,shell=True)

        #print 'stop existing android server by sending back key'
        # this is not mandatory as we already killed adb server, but could this
        # decrease the webview created in andriod server application. maybe
        # it's a bug to create one webview per launch of app?
        for i in xrange(4):
            subprocess.call(r'%s shell input keyevent 4'%self.adbCmd,shell=True)

        #print 'start android server activity'
        output=subprocess.check_output(r'%s shell am start -n %s'%(self.adbCmd,
            Service.ANDROID_DRIVER_CLIENT_APP_CMP),
            stderr=subprocess.STDOUT,shell=True).split()
        if len(output)> 5: #if app not installed, there would be error messages
            raise WebDriverException("""AndroidDriver needs to be installed on device.
            Download android-server-2.x.apk from
            http://code.google.com/p/selenium/downloads/list""")
        # wait for WebDriver Client to be launched completely
        time.sleep(2)
        #print "Device %s is ready." % repr(self.device)

    @property
    def service_url(self):
        """ Gets the url of the ChromeDriver Service """
        return "http://127.0.0.1:8080/wd/hub"

    def stop(self):
        """ Close AndroidDriver by sending BACK keyevent to device"""
        try:
            print 'stopping AndroidDriver'
            subprocess.Popen(r'%s shell input keyevent 4'%self.adbCmd,
                    stdout=PIPE, stderr=PIPE)
        except:
            print """AndroidDriver was not closed. Close by yourself by tapping
            back key to exit AndroidDriver on device."""
