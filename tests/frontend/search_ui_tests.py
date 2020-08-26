import os
import shutil
import unittest
from pathlib import Path

import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from src.backend import MockQuery
from tests.frontend.ui_tests_base import UITestsBase


class SearchUITests(UITestsBase):
    """Search UI tests.
    Tests that the search bar works as expected.
    """

    def setUp(self):
        """Setup
        """
        self.output_path = str(Path('tests/frontend/queries/').absolute())
        shutil.rmtree(self.output_path, ignore_errors=True)
        self.query = MockQuery()

        for _ in range(10):
            self.full_filename = self.query.query_and_update(self.output_path)[
                0]

        self.filename = Path(self.full_filename).name
        super().setUp()
        self.search_input = self.driver.find_element_by_id('input-search-logs')

    def tearDown(self):
        """Teardown
        """
        shutil.rmtree(self.output_path, ignore_errors=True)
        super().tearDown()

    def search(self, path: str):
        """Clears and searches using the search bar
        """
        self.search_input.clear()
        self.search_input.send_keys(path)
        self.wait_for_ajax_to_complete()

    @unittest.skip("Not debugging currently.")
    def test_searching_logs(self):
        """Test searching for the mock logs.
        """
        self.search(self.output_path)
        self.wait_for_element(By.ID, self.filename)

        path_ending_on_slash = os.path.join(self.output_path, '')
        self.search(path_ending_on_slash)
        self.wait_for_element(By.ID, self.filename)

        self.search('    ' + path_ending_on_slash + '     ')
        self.wait_for_element(By.ID, self.filename)

        incomplete_path = self.output_path[:-2]
        self.search(incomplete_path)
        with self.assertRaises(TimeoutException):
            self.wait_for_element(By.ID, self.filename)

    @unittest.skip("Not debugging currently.")
    def test_indices_and_values_correct_displayed(self):
        """Test searching for the mock logs and that the selectable indices and values are displayed.
        """
        self.search(self.output_path)
        self.click_element(By.ID, self.filename)
        nav_items_indices = self.wait_for_element(By.CLASS_NAME, 'nav-item-indices',
                                                  condition=EC.visibility_of_all_elements_located)

        expected_nav_item_ids = [f'nav-item-indices-{i}' for i in range(10)]
        for nav_item in nav_items_indices:
            element_id = nav_item.get_attribute('id')
            self.assertIn(element_id, expected_nav_item_ids)

        nav_item_values = self.wait_for_element(By.CLASS_NAME, 'nav-item-values')
        self.assertEqual(nav_item_values.get_attribute('id'), 'nav-item-values-values')

    def test_selection_of_indices_and_values(self):
        """Test searching for the mock logs.
        """
        self.search(self.output_path)
        self.click_element(By.ID, self.filename)
        nav_items_indices = self.wait_for_element(By.CLASS_NAME, 'nav-item-indices',
                                                  condition=EC.visibility_of_all_elements_located)

        for nav_item in nav_items_indices:
            self.assertFalse(self.is_active(nav_item))
            nav_item.click()
            self.assertTrue(self.is_active(nav_item))

        nav_item_values = self.wait_for_element(By.CLASS_NAME, 'nav-item-values')
        self.assertFalse(self.is_active(nav_item_values))
        nav_item_values.click()
        self.assertTrue(self.is_active(nav_item_values))


if __name__ == "__main__":
    unittest.main()
