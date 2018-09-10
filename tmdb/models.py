# -*- coding: utf-8 -*-
class Resource(object):
  def __init__(self, **data):
    for key, value in data.items():
      if isinstance(value, list):
        self.__dict__[key] = [Resource.create(item) for item in value]
      else:
        self.__dict__[key] = value

  @staticmethod
  def create(fields):
    result = Resource()
    result.__dict__.update(fields)
    return result
