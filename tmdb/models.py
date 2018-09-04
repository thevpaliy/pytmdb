# -*- coding: utf-8 -*-
class resource(object):
  def __init__(self, **data):
    for key, value in data.items():
      if isinstance(value, list):
        self.__dict__[key] = [resource.create(item) for item in value]
      else:
        self.__dict__[key] = value

  @staticmethod
  def create(container):
    result = resource()
    result.__dict__.update(container)
    return result
