import os
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
  def mock_request(self, request, status=None, json=None, url=None):
    response = MockResponse(status, json, url)
    request.return_value = response
    request.expects_call().returns(response)
    yield

  @mock.patch('requests.get')
  def test_get_request_fails(self, fake):
    client = Client(raise_for_status=True)
    for status in (500, 501, 502, 504, 505):
      with self.mock_request(fake, status):
        self.assertRaises(HTTPError, lambda: client.get('/path'))

  @mock.patch('requests.post')
  def test_post_request_fails(self, fake):
    client = Client(raise_for_status=True)
    for status in (500, 501, 502, 504, 505):
      with self.mock_request(fake, status):
        self.assertRaises(HTTPError, lambda: client.post('/path'))

  @mock.patch('requests.delete')
  def test_delete_request_fails(self, fake):
    client = Client(raise_for_status=True)
    for status in (500, 501, 502, 504, 505):
      with self.mock_request(fake, status):
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
      with self.mock_request(fake, status):
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
      with self.mock_request(fake, status):
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
      with self.mock_request(fake, status):
        try:
          client.delete('/path')
          Client().delete('path') # test the default version
        except HTTPError:
          self.fail('client.delete() raises an exception when'
            '``raise_for_status`` is set to False')

  @mock.patch('requests.get')
  def test_authorize_url(self, fake):
    client = Client(host='host.com', raise_for_status=False)
    base_url = client._build_url(path='www.themoviedb.org/')
    with self.mock_request(fake, json=dict(request_token='token')):
      expected_url = '%s/%s' % (base_url, 'token')
      self.assertEqual(client.authorize_url, expected_url)
      # check if this works with a redirect_uri
      client = Client(host='host.com', redirect_url='/redirect.com')
      expected_url = '%s?%s' % (expected_url, '/redirect.com')
      self.assertEqual(client.authorize_url, expected_url)

  @mock.patch('requests.post')
  def test_session_id(self, fake):
    client = Client(access_token='token')
    with self.mock_request(fake, json={'session_id':'id'}):
      self.assertEqual(client.session_id, 'id')

  @mock.patch.dict(os.environ,{'api_key':'key'})
  def test_api_key(self):
    client = Client()
    self.assertEqual(client.api_key, 'key')
    

def main():
  support.run_unittest(ClientTestCase)

if __name__ == '__main__':
  main()
