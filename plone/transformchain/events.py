# -*- coding: utf-8 -*-
from plone.transformchain.interfaces import IAfterSingleTransformEvent
from plone.transformchain.interfaces import IAfterTransformsEvent
from plone.transformchain.interfaces import IBeforeSingleTransformEvent
from plone.transformchain.interfaces import IBeforeTransformsEvent
from zope.interface import implementer


class BaseTransformEvent(object):

    def __init__(self, request):
        self.request = request


class BaseSingleTransformEvent(BaseTransformEvent):

    def __init__(self, request, name, handler):
        super(BaseSingleTransformEvent, self).__init__(request)
        self.name = name
        self.handler = handler


@implementer(IBeforeTransformsEvent)
class BeforeTransforms(BaseTransformEvent):
    pass


@implementer(IAfterTransformsEvent)
class AfterTransforms(BaseTransformEvent):
    pass


@implementer(IBeforeSingleTransformEvent)
class BeforeSingleTransform(BaseSingleTransformEvent):
    pass


@implementer(IAfterSingleTransformEvent)
class AfterSingleTransform(BaseSingleTransformEvent):
    pass
