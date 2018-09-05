import requests

class MockResponse(requests.Response):
  def __init__(self, status_code=None, json=None, url=None, reason=None):
    self.status_code = status_code
    self._json = json or {}
    self.reason = reason or 'OK'
    self.url = url

  def json(self):
    return self._json
