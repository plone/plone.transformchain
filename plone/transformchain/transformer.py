# -*- coding: utf-8 -*-
from plone.transformchain import events
from plone.transformchain.interfaces import DISABLE_TRANSFORM_REQUEST_KEY
from plone.transformchain.interfaces import ITransform
from plone.transformchain.interfaces import ITransformer
from ZODB.POSException import ConflictError
from zope.component import getAdapters
from zope.event import notify
from zope.interface import implementer
from ZServer.FTPRequest import FTPRequest

import logging


LOGGER = logging.getLogger('plone.transformchain')


def _order_getter(pair):
    return pair[1].order


@implementer(ITransformer)
class Transformer(object):
    """Delegate the opportunity to transform the response to multiple,
    ordered adapters.
    """

    def __call__(self, request, result, encoding):
        if isinstance(request, FTPRequest):
            # Don't transform FTP requests
            return None
        if request.environ.get(DISABLE_TRANSFORM_REQUEST_KEY, False):
            # Off switch
            return None
        notify(events.BeforeTransforms(request))
        try:
            published = request.get('PUBLISHED', None)
            handlers = sorted(
                getAdapters((published, request,), ITransform),
                key=_order_getter
            )
            for name, handler in handlers:
                notify(events.BeforeSingleTransform(request, name, handler))
                if isinstance(result, unicode):
                    newResult = handler.transformUnicode(result, encoding)
                elif isinstance(result, str):
                    newResult = handler.transformBytes(result, encoding)
                else:
                    newResult = handler.transformIterable(result, encoding)

                if newResult is not None:
                    result = newResult
                notify(events.AfterSingleTransform(request, name, handler))
            notify(events.AfterTransforms(request))
            return result
        except ConflictError:
            raise
        except Exception:
            LOGGER.exception(
                u"Unexpected error whilst trying to apply transform chain"
            )
