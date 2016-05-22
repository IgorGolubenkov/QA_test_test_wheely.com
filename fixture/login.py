
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction



class LoginHelper:

    def generator_region_name_list(self, reg_name_lest):
        for el in reg_name_lest:
            yield el