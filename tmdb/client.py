# -*- coding: utf-8 -*-
import requests
import logging
import os
import time
import functools
import numbers
import tmdb
from tmdb.models import resource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Client(object):
  host = 'api.themoviedb.org/3'
  methods = ('get', 'post', 'put', 'head', 'delete')
  use_ssl = True

  def __init__(self, **kwargs):
    r"""
    :param use_ssl (optional): use HTTP or HTTPS for requests. Default: True
    :type use_ssl: bool
    :param host (optional): host for every request. Default: `api.themoviedb.org/3`
    :param allow_redirects (optional): enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection.
    :type allow_redirects (optional): bool
    :param api_key: a mandatory API key for every request.
    :param timeout:how many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
    :type timeout: float or tuple
    :param access_token: a valid access token that will allow us to create a session id.
    :param username (optional): a username with which we can verify an access token in order to obtain a session id.
    :param password (optional): a password with which we can verify an access token in order to obtain a session id.
    :param session id (optional): a session id with which we can make DELETE, PUT, requests, etc.
    """
    self._use_ssl = kwargs.get('use_ssl', self.use_ssl)
    self._host = kwargs.get('host', self.host)
    self._api_key = kwargs.get('api_key', os.environ.get('api_key', None))
    self._scheme = 'https' if self._use_ssl else 'http'
    self._debug = kwargs.get('debug', False)
    self._allow_redirects = kwargs.get('allow_redirects', False)
    self._timeout = kwargs.get('timeout', None)
    self._access_token = kwargs.get('access_token', None)
    self._authorize_url = kwargs.get('authorize_url', None)
    self._session_id = kwargs.get('session_id', None)
    if not self._authorize_url and not self._session_id:
      if any([key in kwargs for key in ('redirect_uri', 'redirect_url')]):
        self.redirect_uri = kwargs.get('redirect_uri', kwargs['redirect_url'])
    if (not self._session_id and
          ('username' in kwargs and 'password' in kwargs)):
        self.login(kwargs['username'], kwargs['password'])

  def _generate_access_token(self):
    resource = self.get(path='/authentication/token/new')
    self.__log(resource.request_token)
    return resource.request_token

  def _create_session_id(self):
    resource = self.post(path='/authentication/session/new',
        json=dict(request_token=self._access_token))
    self.__log(resource.session_id)
    return resource.session_id

  @property
  def authorize_url(self):
    if not self._authorize_url:
      self._access_token = self._generate_access_token()
      url = self._build_url(path='www.themoviedb.org/')
      self._authorize_url = '%s/%s' % (url, self._access_token)
      if hasattr(self, 'redirect_uri'):
        self._authorize_url = '%s?%s' % (self._authorize_url, self.redirect_uri)
      self.__log(self._authorize_url)
    return self._authorize_url

  @authorize_url.setter
  def authorize_url(self, url):
    self._authorize_url = url

  @property
  def session_id(self):
    if not self._session_id:
      self._session_id = self._create_session_id()
    return self._session_id

  @property
  def api_key(self):
    if self.api_key is None:
      self._api_key = os.environ['api_key']
    return self._api_key

  @api_key.setter
  def api_key(self, api_key):
    self._api_key = api_key
    os.environ['api_key'] = api_key

  def __getattr__(self, method, **kwargs):
    if method.lower() not in self.methods:
      raise AttributeError
    return functools.partial(self._request, method, **kwargs)

  def _build_url(self, path):
    url = '%s://%s%s' % (self._scheme, self._host, path)
    self.__log(url)
    return url

  def _build_options(self):
    return {
      'allow_redirects': self._allow_redirects,
      'timeout': self._timeout,
      'headers': {
        'User-Agent': tmdb.USER_AGENT
      }
    }

  def logout(self):
    if self._session_id:
      self.delete('/authentication/session',
        json=dict(session_id=self._session_id))

  def login(self, username, password):
    if not self._access_token:
      self._access_token = self._generate_access_token()
    # verify the generated token
    body = dict(request_token=self._access_token,
          username=username, password=password)
    self.post('/authentication/token/validate_with_login', json=body)
    # create a session id if the verification was successful
    self._session_id = self._create_session_id()

  def _request(self, method, path, query=None, data=None, json=None):
    request = getattr(requests, method, None)
    if request is None:
      raise TypeError('%s is not  an HTTP method' % method)
    kwargs = self._build_options()
    url = self._build_url(path)
    params = {'api_key':self._api_key}
    if query:
      params.update(query)
    kwargs['params'] = params
    if method == 'get':
      kwargs['headers']['Accept'] = 'application/json'
      response = request(url, **kwargs)
    else:
      kwargs['data'] = data
      kwargs['json'] = json
      if self._session_id:
        kwargs['params']['session_id'] = self._session_id
      response = request(url, **kwargs)
    self.__log('status code:%s' % (response.status_code))
    response.raise_for_status()
    content = response.json()
    self.__log('%s\n' % (content))
    return resource(status_code = response.status_code, **content)

  def __log(self, info):
    if self._debug:
      logger.info(info)
