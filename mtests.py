import unittest
from find_store_lib import *

class FindStoreTests(unittest.TestCase):
  def test_find_store_address(self):
    self.assertEqual(find_store("600 California Street, San Francisco, CA 94108")[0], "225 Bush St")

  def test_find_store_zip(self):
    self.assertEqual(find_store("94117")[0], '2675 Geary Blvd')

if __name__ == '__main__':
  unittest.main()
