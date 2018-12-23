import time

from selenium import webdriver
import unittest

from selenium.webdriver.common.keys import Keys

HOST = 'http://localhost:8000'


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        pass

    def test_can_start_with_a_list_and_retrieve_late(self):
        self.browser.get(HOST)
        self.assertIn('TO-DO', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('to-do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do list'
        )

        test_to_do = "1:buy peacock feathers"
        inputbox.send_keys(test_to_do)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_element_by_tag_name('tr')
        self.assertTrue(
            any(row.text == test_to_do for row in rows)
        )

        self.fail('finish test')


if __name__ == "__main__":
    unittest.main(warnings='ignore')
