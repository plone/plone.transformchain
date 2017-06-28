Changelog
=========

1.2.1 (2017-06-28)
------------------

Bug fixes:

- Remove unittest2 dependency
  [kakshay21]


1.2.0 (2016-06-21)
------------------

New:

- Added events to notify before/after all/single transform(s) are executed.
  [jensens]


1.1.0 (2016-02-21)
------------------

New:

- Require Zope2 >= 2.13.23
  [jensens]

Fixes:

- PEP8 et al. use zca decorators, ...
  [jensens]


1.0.4 (2015-05-11)
------------------

- Minor cleanup: whitespace, git ignores, rst.
  [gforcada, rnix, maurits]


1.0.3 (2013-01-13)
------------------

- There was a problem with the charset regular expression, it expected one
  space, and only one, between mimetype and charset. So a valid values like
  "text/html;charset=utf-8" didn't match and default_encoding was returned.
  We fixed it by allowing any number of spaces (including zero).
  [jpgimenez]


1.0.2 (2012-01-26)
------------------

- Fix packaging error.
  [esteele]


1.0.1 (2012-01-26)
------------------

- Compute error_status and store it on request.
  Work around bug with Zope 2.13 publication events :
  response.status is not set when IPubBeforeAbort is notified.
  [gotcha]

- Don't transform FTP requests
  [rochecompaan]

1.0 - 2011-05-13
----------------

- Release 1.0 Final.
  [esteele]

1.0b1 - 2010-04-21
------------------

- Initial release
