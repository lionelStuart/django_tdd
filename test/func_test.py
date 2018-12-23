from selenium import webdriver
import unittest

HOST = 'http://localhost:8000'


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
       #self.browser.quit()
        pass

    def test_can_start_with_a_list_and_retrieve_late(self):
        self.browser.get(HOST)
        self.assertIn('To-DO', self.browser.title)
        self.fail('finish the test')


if __name__ == "__main__":
    unittest.main(warnings='ignore')
