Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

3.0.0 (2023-04-27)
------------------

Breaking changes:


- Drop Python 2 and Plone 5.2 compatibility.
  [gforcada] (#6)


Internal:


- Update configuration files.
  [plone devs] (3333c742)


2.0.2 (2020-04-22)
------------------

Bug fixes:


- Minor packaging updates. (#1)


2.0.1 (2018-11-04)
------------------

Bug fixes:

- More py3 test and functionality fixes.
  [pbauer, thet]


2.0.0 (2018-06-20)
------------------

Breaking changes:

- Drop support for Python 2.6.
  [jensens]

New features:

- Make ZServer optional

Bug fixes:

- More fixes for Python 2 / 3 compatibility.
  [pbauer, thet]


1.2.2 (2018-02-11)
------------------

Bug fixes:

- Add Python 2 / 3 compatibility
  [vincero]


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
