
#  Перед запуском тестов на тестовую машину, я использовал windows, нужно установить APPIUM, предварительно
# установив node, более подробную информацию можо получить по ссылке: http://appium.io/
#  Так же должен быть установлен ADB, в зависимости от того, на виртуальном девайсе или на реальном устройстве,
# будете проводить тесты: Подготовить устройство, и настройки к нему прописать в Appium
#  Для запуска тестов и конфигурации тестового окружения я использую сервер CI Jenkins.
#  Так же тесты можно запустить из консоли или среды разработки.
#
#

import os
import unittest
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time


test_data = {}

test_data['number_phone'] = "9057142795"
test_data['code_phoneLogin'] = "1234"
test_data['first_name'] = "Игорь"
test_data['last_name'] = "Голубенков"
test_data['email'] = "i.golubenkov@mail.ru"

PATH = lambda file: os.path.join(os.path.dirname(os.path.abspath(__file__)), file)

class ContactsAndroidTests(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.1.1'
        desired_caps['deviceName'] = 'Nexus 5X API 22'
        desired_caps['app'] = PATH('app-7.3.365-dev-debug.apk')

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(7)

    def tearDown(self):
        self.driver.quit()

    def test_login(self):

        landing_goon_button = self.driver.find_element_by_id('com.wheely.wheely.dev:id/landing_goon_button')
        self.assertIsNotNone(landing_goon_button)

        action = TouchAction(self.driver)

        action.tap(landing_goon_button).perform()

        region_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/countryName')
        self.assertIsNotNone(region_field)

        text_region_field = region_field.get_attribute('text')
        if text_region_field != "Russia":
            action.tap(region_field).perform()

        el_numberphone_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/phoneField')
        self.assertIsNotNone(el_numberphone_field)

        action.tap(el_numberphone_field).perform()
        el_numberphone_field.clear()
        el_numberphone_field.send_keys(test_data['number_phone'])

        button_next = self.driver.find_element_by_accessibility_id('Далее')
        self.assertIsNotNone(button_next)

        action.tap(button_next).perform()

        message_phoneNumber_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/pin_verify_sent_sms_prompt')
        self.assertIsNotNone(message_phoneNumber_field)

        text_message_phoneNumber_field = message_phoneNumber_field.get_attribute('text')
        textRight_message_phoneNumber_field = "Мы отправили СМС с кодом на номер +7 905 714-27-95."
        self.assertEqual(textRight_message_phoneNumber_field, text_message_phoneNumber_field)

        enter_codePhoneLogin_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/pin_verify_verification_code')
        self.assertIsNotNone(enter_codePhoneLogin_field)

        enter_codePhoneLogin_field.clear()
        enter_codePhoneLogin_field.send_keys(test_data['code_phoneLogin'])

        firstName_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/userinfo_firstname')
        text_firstName_field = firstName_field.get_attribute('text')
        self.assertEqual(test_data['first_name'], text_firstName_field)

        lastName_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/userinfo_lastname')
        text_lastName_field = lastName_field.get_attribute('text')
        self.assertEqual(test_data['last_name'], text_lastName_field)

        email_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/userinfo_email')
        text_email_field = email_field.get_attribute('text')
        self.assertEqual(test_data['email'], text_email_field)

        button_next_2 = self.driver.find_element_by_accessibility_id('Далее')
        self.assertIsNotNone(button_next_2)

        action.tap(button_next_2).perform()

        el_close_cardBinding = self.driver.find_element_by_class_name('android.widget.ImageButton')
        self.assertIsNotNone(el_close_cardBinding)

        action.tap(el_close_cardBinding).perform()

        openMenu_button = self.driver.find_element_by_class_name('android.widget.ImageButton')
        self.assertIsNotNone(openMenu_button)

        action.tap(openMenu_button).perform()

        name_field_menu = self.driver.find_element_by_id('com.wheely.wheely.dev:id/drawer_list_item_subtext')
        text_name_field_menu = name_field_menu.get_attribute('text')
        self.assertEqual(test_data['first_name'] + " " + test_data['last_name'], text_name_field_menu)

        button_open_account = self.driver.find_element_by_id('com.wheely.wheely.dev:id/drawer_profile')
        self.assertIsNotNone(button_open_account)

        action.tap(button_open_account).perform()

        account_name_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/profile_customer_name')
        text_account_ame_field = account_name_field.get_attribute('text')
        self.assertEqual(test_data['first_name'] + " " + test_data['last_name'], text_account_ame_field)

        account_phoneNumber = self.driver.find_element_by_id('com.wheely.wheely.dev:id/profile_customer_phone')
        text_account_phoneNumber = account_phoneNumber.get_attribute('text')
        self.assertEqual("+7 905 714-27-95", text_account_phoneNumber)

        account_email_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/profile_customer_email')
        text_account_email_field = account_email_field.get_attribute('text')
        self.assertEqual(test_data['email'], text_account_email_field)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ContactsAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)