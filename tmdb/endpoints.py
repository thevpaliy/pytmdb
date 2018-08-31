from functools import wraps

def construct(method='GET', path):
  def decorator(function):
    @wraps(function)
    def get(*args, **kwds):
      options = function(*args, **kwds)
      return {'path':path % (options.args),
          'query':dict(options.query)}
    @wraps(function)
    def post(*args, **kwds):
      pass
    @wraps(function)
    def delete(*args, **kwds):
      pass
    return {'GET':get,'POST':post,
        'DELETE':delete }[method.upper()]
  return decorator

class OptionsWrapper(object):
  def __init__(self, *args, **query):
    self.args = args
    self.query = query

class Movie(object):

  @staticmethod
  @construct(path='/movie/%s')
  def details(id):
    return OptionsWrapper(id)

  @staticmethod
  @construct(path='/movie/%s/reviews')
  def reviews(id):
    return OptionsWrapper(id)

  @staticmethod
  @construct(path='/movie/%s/lists')
  def lists(id):
    return OptionsWrapper(id)

  @staticmethod
  @construct(path='/movie/%s/videos')
  def videos(id):
    return OptionsWrapper(id)

  @staticmethod
  @construct(path='/movie/%s/recommendations')
  def recommendations(id):
    return OptionsWrapper(id)

  @staticmethod
  @construct(path='/movie/latest')
  def latest(page=1):
    return OptionsWrapper(page=page)

  @staticmethod
  @construct(path='/movie/now_playing')
  def now_playing(page=1):
    return OptionsWrapper(page=page)

  @staticmethod
  @construct(path='/movie/top_rated')
  def top_rated(page=1):
    return OptionsWrapper(page=page)

  @staticmethod
  @construct(path='/movie/upcoming')
  def upcoming(page=1):
    return OptionsWrapper(page=page)

  @staticmethod
  @construct(path='/movie/popular')
  def popular(page=1):
    return OptionsWrapper(page=page)

  @staticmethod
  @construct(path='/search/movie')
  def search(query, page=1):
    return OptionsWrapper(query, page=page)

  @staticmethod
  @construct(path='/movie/%s/credits')
  def credits(id):
    return OptionsWrapper(id)

  @staticmethod
  @construct(path='/movie/%s/similar')
  def similar(id):
    return OptionsWrapper(id)

  @staticmethod
  @construct(path='/movie/%s/images')
  def images(id):
    return OptionsWrapper(id)

  @staticmethod
  @construct(method='POST', path='/movie/%s/rating')
  def rate(id, rating):
    pass

  @staticmethod
  @construct(method='DELETE', path='/movie/%s/delete')
  def delete(id):
    pass

class TV(object):

  @staticmethod
  @construct(path='/TV/%s')
  def details(id):
    return OptionsWrapper(id)

  @staticmethod
  @construct(path='/TV/%s/reviews')
  def reviews(id):
    return OptionsWrapper(id)

  @staticmethod
  @construct(path='/TV/%s/videos')
  def videos(id):
    return OptionsWrapper(id)

  @staticmethod
  @construct(path='/TV/%s/recommendations')
  def recommendations(id):
    return OptionsWrapper(id)

  @staticmethod
  @construct(path='/TV/latest')
  def latest(page=1):
    return OptionsWrapper(page=page)

  @staticmethod
  @construct(path='/TV/now_playing')
  def now_playing(page=1):
    return OptionsWrapper(page=page)

  @staticmethod
  @construct(path='/TV/top_rated')
  def top_rated(page=1):
    return OptionsWrapper(page=page)

  @staticmethod
  @construct(path='/TV/upcoming')
  def upcoming(page=1):
    return OptionsWrapper(page=page)

  @staticmethod
  @construct(path='/TV/popular')
  def popular(page=1):
    return OptionsWrapper(page=page)

  @staticmethod
  @construct(path='/search/TV')
  def search(query, page=1):
    return OptionsWrapper(query, page=page)

  @staticmethod
  @construct(path='/TV/%s/credits')
  def credits(id):
    return OptionsWrapper(id)

  @staticmethod
  @construct(path='/TV/%s/similar')
  def similar(id):
    return OptionsWrapper(id)

  @staticmethod
  @construct(path='/TV/%s/images')
  def images(id):
    return OptionsWrapper(id)
