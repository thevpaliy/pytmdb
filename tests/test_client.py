import requests
import mock
from utils import MockResponse
from unittest import TestCase
from test import support
try:
  from tmdb.client import Client
except ImportError:
  import os, sys
  sys.path.insert(0, '..')
  from tmdb.client import Client
from contextlib import contextmanager
from requests.exceptions import HTTPError

class ClientTestCase(TestCase):

  @contextmanager
  def response_status(self, request, status=None, json=None, url=None):
    response = MockResponse(status, json, url)
    request.return_value = response
    request.expects_call().returns(response)
    yield

  @mock.patch('requests.get')
  def test_get_request_fails(self, fake):
    client = Client(raise_for_status=True)
    for status in (500, 501, 502, 504, 505):
      with self.response_status(fake, status):
        self.assertRaises(HTTPError, lambda: client.get('/path'))

  @mock.patch('requests.post')
  def test_post_request_fails(self, fake):
    client = Client(raise_for_status=True)
    for status in (500, 501, 502, 504, 505):
      with self.response_status(fake, status):
        self.assertRaises(HTTPError, lambda: client.post('/path'))

  @mock.patch('requests.delete')
  def test_delete_request_fails(self, fake):
    client = Client(raise_for_status=True)
    for status in (500, 501, 502, 504, 505):
      with self.response_status(fake, status):
        self.assertRaises(HTTPError, lambda: client.delete('/path'))

  def test_method_does_not_exist(self):
    with self.assertRaises(AttributeError):
      Client().method()
    with self.assertRaises(TypeError):
      Client()._request('unknown')

  @mock.patch('requests.get')
  def test_ignore_failing_get_request(self, fake):
    client = Client(raise_for_status=False)
    for status in (500, 501, 502, 504, 505):
      with self.response_status(fake, status):
        try:
          client.get('/path')
          Client().get('path') # test the default version
        except HTTPError:
          self.fail('client.get() raises an exception when'
            '``raise_for_status`` is set to False')

  @mock.patch('requests.post')
  def test_ignore_failing_post_request(self, fake):
    client = Client(raise_for_status=False)
    for status in (500, 501, 502, 504, 505):
      with self.response_status(fake, status):
        try:
          client.post('/path')
          Client().post('path') # test the default version
        except HTTPError:
          self.fail('client.post() raises an exception when'
            '``raise_for_status`` is set to False')

  @mock.patch('requests.delete')
  def test_ignore_failing_delete_request(self, fake):
    client = Client(raise_for_status=False)
    for status in (500, 501, 502, 504, 505):
      with self.response_status(fake, status):
        try:
          client.delete('/path')
          Client().delete('path') # test the default version
        except HTTPError:
          self.fail('client.delete() raises an exception when'
            '``raise_for_status`` is set to False')

def main():
  support.run_unittest(ClientTestCase)

if __name__ == '__main__':
  main()
