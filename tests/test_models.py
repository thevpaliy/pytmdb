import unittest

from test import test_support
from tmdb.models import Resource

class ResourceTest(unittest.TestCase):
  pass

def main():
  test_support.run_unittest(ResourceTest)

if __name__ == '__main__':
  main()
