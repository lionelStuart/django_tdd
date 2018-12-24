import time

from selenium import webdriver
import unittest

from selenium.webdriver.common.keys import Keys

HOST = 'http://localhost:8000'


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows],"fail text {}".format(rows))

    def tearDown(self):
        # self.browser.quit()
        pass

    def test_can_start_with_a_list_and_retrieve_late(self):
        self.browser.get(HOST)
        self.assertIn('TO-DO', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('to-do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'enter a to-do list'
        )

        test_to_do = "1:buy peacock feathers"
        inputbox.send_keys(test_to_do)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table(test_to_do)

        #table = self.browser.find_element_by_id('id_list_table')

        test_to_do = "use peacock feather to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(test_to_do)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table(test_to_do)

        #rows = table.find_elements_by_tag_name('tr')
        # self.assertTrue(
        #     any(row.text == test_to_do for row in rows),
        #     "new to-do item not appear in table"
        # )

        self.fail('finish test')


if __name__ == "__main__":
    unittest.main(warnings='ignore')
