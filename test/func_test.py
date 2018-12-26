import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

#
# HOST = 'http://localhost:8000'

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows], "fail text {}".format(rows))
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def tearDown(self):
        # self.browser.quit()
        pass

    def test_can_start_with_a_list_and_retrieve_late(self):
        """
        1.使用本地url
        :return:
        """
        self.browser.get(self.live_server_url)
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
        self.wait_for_row_in_list_table(test_to_do)

        test_to_do = "use peacock feather to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(test_to_do)
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(test_to_do)

    def test_multi_users_can_start_list_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        test_to_do = "1:buy peacock feathers"
        inputbox.send_keys(test_to_do)
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table(test_to_do)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/list/.+")

        self.browser.quit()
        ## a new vistor
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn(test_to_do, page_text)

