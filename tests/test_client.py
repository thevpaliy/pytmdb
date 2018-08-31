from unittest import TestCase
from mockito import when, mock, unstub, verify, never, spy
from test import support
from tmdb.client import Client
import requests

class ClientTestCase(TestCase):

  def build_response(self,**kwargs):
    response = mock({}.update(kwargs),
        spec=requests.Request)
    when(response).json().thenReturn({})
    return response

  def mock_calls(self, **kwargs):
    if 'all' in kwargs:
      for method in 'get post delete'.split():
        kwargs[method] = kwargs['all']
    if 'get' in kwargs:
      when(requests).get(...).thenReturn(kwargs['get'])
    if 'delete' in kwargs:
      when(requests).delete(...).thenReturn(kwargs['post'])
    if 'post' in kwargs:
      when(requests).post(...).thenReturn(kwargs['delete'])

  def setUp(self):
    self.mock_calls(all=self.build_response())

  def tearDown(self):
    unstub()

  def test_getattr_invalid_method(self):
    client = Client(unknown='unknown')
    with self.assertRaises(AttributeError):
      client.unknown

  def test_logout_nothing(self):
    Client().logout()
    verify(requests, times=never).delete(...)

  def test_logout_success(self):
    client = Client(session_id='session_id')
    client.logout()
    verify(requests, times=1).delete(...)

  # TODO: provide a bit more comprehensive testing
  def test_login_nothing(self):
    Client(access_token='token').login('username', 'password')
    verify(requests, times=1).get(...)
    verify(requests, times=1).post(...)

def main():
  support.run_unittest(ClientTestCase)

if __name__ == '__main__':
  main()
