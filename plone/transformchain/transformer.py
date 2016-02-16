# -*- coding: utf-8 -*-
from operator import attrgetter
from plone.transformchain.interfaces import DISABLE_TRANSFORM_REQUEST_KEY
from plone.transformchain.interfaces import ITransform
from plone.transformchain.interfaces import ITransformer
from ZODB.POSException import ConflictError
from zope.component import getAdapters
from zope.interface import implementer
from ZServer.FTPRequest import FTPRequest

import logging


LOGGER = logging.getLogger('plone.transformchain')


@implementer(ITransformer)
class Transformer(object):
    """Delegate the opportunity to transform the response to multiple,
    ordered adapters.
    """

    def __call__(self, request, result, encoding):
        # Don't transform FTP requests
        if isinstance(request, FTPRequest):
            return None

        # Off switch
        if request.environ.get(DISABLE_TRANSFORM_REQUEST_KEY, False):
            return None

        try:
            published = request.get('PUBLISHED', None)
            handlers = (
                v[1] for v in getAdapters((published, request,), ITransform)
            )
            for handler in sorted(handlers, key=attrgetter('order')):
                if isinstance(result, unicode):
                    newResult = handler.transformUnicode(result, encoding)
                elif isinstance(result, str):
                    newResult = handler.transformBytes(result, encoding)
                else:
                    newResult = handler.transformIterable(result, encoding)

                if newResult is not None:
                    result = newResult

            return result
        except ConflictError:
            raise
        except Exception:
            LOGGER.exception(
                u"Unexpected error whilst trying to apply transform chain"
            )
