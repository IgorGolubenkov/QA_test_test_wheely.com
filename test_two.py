
# -*- coding: utf-8 -*-

#  Перед запуском тестов на тестовую машину, я использовал windows, нужно установить APPIUM, предварительно
# установив node, более подробную информацию можо получить по ссылке: http://appium.io/
#  Так же должен быть установлен ADB, в зависимости от того, на виртуальном девайсе или на реальном устройстве,
# будете проводить тесты: Подготовить устройство, и настройки к нему прописать в Appium
#  Для запуска тестов и конфигурации тестового окружения обычно я использую сервер CI Jenkins.
#  Этот тест запускаю в ручну. в среде рахработки, так же тесты можно запустить из консоли.
#
#  Запускаем тестовый девайс, запускаем сессию в APPIUM, запускаем тест


import os
import unittest
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from fixture.login import LoginHelper


test_data = {}

test_data['number_phone'] = "9057142795"
test_data['code_phoneLogin'] = "1234"
test_data['first_name'] = "Игорь"
test_data['last_name'] = "Голубенков"
test_data['email'] = "i.golubenkov@mail.ru"

PATH = lambda file: os.path.join(os.path.dirname(os.path.abspath(__file__)), file)

class TestLogin(unittest.TestCase):

    # конфигурации для начала тестовой сессии
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.1.1'
        desired_caps['deviceName'] = 'Nexus 5X API 22'
        desired_caps['app'] = PATH('app-7.3.365-dev-debug.apk')

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(7)

    # метод финализации тестовой сессии
    def tearDown(self):
        self.driver.quit()

    # тест кейс авторизации
    def test_login(self):

        action = TouchAction(self.driver)

        # Находим элемент кнопка для входа в приложение и тапом входим в приложение
        landing_goon_button = self.driver.find_element_by_id('com.wheely.wheely.dev:id/landing_goon_button')
        action.tap(landing_goon_button).perform()

        # находим поле с указанием локали для отправки смс
        region_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/countryName')
        # извлекаем текст элемента
        text_region_field = region_field.get_attribute('text')
        # так  как тест для региона Россия, если стоит другая локаль соврешаем действия для выбора локали Россия
        if text_region_field != "Russ":
            action.tap(region_field).perform()
            list_region_name_field = self.driver.find_elements_by_class_name('android.widget.RelativeLayout')
            start_el_scrl = list_region_name_field[10]
            stop_el_scrl = list_region_name_field[0]
            self.driver.scroll(start_el_scrl, stop_el_scrl)