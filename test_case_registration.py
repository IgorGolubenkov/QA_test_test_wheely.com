
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
from fixture.email_temporary import TempMail
from fixture.registration import RegistrationHelper
import time

helper_data = RegistrationHelper()

test_data = {}

test_data['number_phone'] = helper_data.get_phone_number(10)
test_data['code_phoneLogin'] = "1234"
test_data['first_name'] = helper_data.get_first_and_last_name(5)
test_data['last_name'] = helper_data.get_first_and_last_name(5)
test_data['email'] = TempMail().get_email_address()

PATH = lambda file: os.path.join(os.path.dirname(os.path.abspath(__file__)), file)

class TestRegistration(unittest.TestCase):

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

            while True:

                for el_region in self.driver.find_elements_by_id('com.wheely.wheely.dev:id/item_country_displayname'):
                    if el_region.get_attribute('text') == "Бенин":
                        action.tap(el_region).perform()
                        break
                list_region_name_field = self.driver.find_elements_by_class_name('android.widget.RelativeLayout')
                if list_region_name_field == []:
                    break
                start_el_scrl = list_region_name_field[1]
                stop_el_scrl = list_region_name_field[0]
                self.driver.scroll(start_el_scrl, stop_el_scrl)


        # находим поле для ввоода номера телефона, тап по полю, и вводим номер телефона
        el_numberphone_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/phoneField')
        action.tap(el_numberphone_field).perform()
        el_numberphone_field.clear()
        el_numberphone_field.send_keys(test_data['number_phone'])

        # кнопка далее появляется после ввода номера телефона, поэтому проверяем появляется ли кнопка "Далее"
        button_next = self.driver.find_element_by_accessibility_id('Далее')
        self.assertIsNotNone(button_next)

        # тапаем по кнопке далее
        action.tap(button_next).perform()

        # находим поле в котором отображается номер телефона на который был оправлен код для входа
        # сверяем что номера телефона верный
        message_phoneNumber_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/pin_verify_sent_sms_prompt')
        text_message_phoneNumber_field = message_phoneNumber_field.get_attribute('text')
        textRight_message_phoneNumber_field = "Мы отправили СМС с кодом на номер +7 %s %s." % (helper_data.get_prefix_phone_number(test_data['number_phone']),
                                                                                               helper_data.get_phoneNumber_for_comparison(test_data['number_phone']))
        self.assertEqual(text_message_phoneNumber_field, textRight_message_phoneNumber_field)

        # форма для заполнения данных о пользователе.
        enter_codePhoneLogin_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/pin_verify_verification_code')
        enter_codePhoneLogin_field.clear()
        enter_codePhoneLogin_field.send_keys(test_data['code_phoneLogin'])

        # Заполняем поле Имя пользователя
        firstName_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/userinfo_firstname')
        action.tap(firstName_field).perform()
        firstName_field.clear()
        firstName_field.send_keys(test_data['first_name'])

        # Заполняем поле Фамилия пользователя
        lastName_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/userinfo_lastname')
        action.tap(lastName_field).perform()
        lastName_field.clear()
        lastName_field.send_keys(test_data['last_name'])

        # Заполняем поле Фамилия емейл пользователя
        email_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/userinfo_email')
        action.tap(email_field).perform()
        email_field.clear()
        email_field.send_keys(test_data['email'])

        # находим кнопку "Далее" и тапаем по ней
        button_next_2 = self.driver.find_element_by_accessibility_id('Далее')
        action.tap(button_next_2).perform()

        # Находим крестик для закрытия формы привязки банковской карты и тапаем по нему
        el_close_cardBinding = self.driver.find_element_by_class_name('android.widget.ImageButton')
        action.tap(el_close_cardBinding).perform()

        # Находим кнопку открытия меню и тапаем по ней
        openMenu_button = self.driver.find_element_by_class_name('android.widget.ImageButton')
        action.tap(openMenu_button).perform()

        # Находим поле в котором отображается имя и фамилия пользователя
        # сверяем верно ли
        name_field_menu = self.driver.find_element_by_id('com.wheely.wheely.dev:id/drawer_list_item_subtext')
        text_name_field_menu = name_field_menu.get_attribute('text')
        self.assertEqual(test_data['first_name'] + " " + test_data['last_name'], text_name_field_menu)

        # находим кнопку открытия входа в раздел аккаунт и тапаем по кнопке
        button_open_account = self.driver.find_element_by_id('com.wheely.wheely.dev:id/drawer_profile')
        action.tap(button_open_account).perform()

        # сверяем верно ли отображаются данные о пользователе на основе этих данных окончательно убеждаемся
        # что процесс регистрации пройден корректно. завершен позитивный тест кейс
        account_name_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/profile_customer_name')
        text_account_ame_field = account_name_field.get_attribute('text')
        self.assertEqual(test_data['first_name'] + " " + test_data['last_name'], text_account_ame_field)

        account_phoneNumber = self.driver.find_element_by_id('com.wheely.wheely.dev:id/profile_customer_phone')
        text_account_phoneNumber = account_phoneNumber.get_attribute('text')
        correct_value = "+7 %s %s" % (helper_data.get_prefix_phone_number(test_data['number_phone']),
                                      helper_data.get_phoneNumber_for_comparison(test_data['number_phone']))
        self.assertEqual(correct_value, text_account_phoneNumber)

        account_email_field = self.driver.find_element_by_id('com.wheely.wheely.dev:id/profile_customer_email')
        text_account_email_field = account_email_field.get_attribute('text')
        self.assertEqual(test_data['email'], text_account_email_field)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRegistration)
    unittest.TextTestRunner(verbosity=2).run(suite)


