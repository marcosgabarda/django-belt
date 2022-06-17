.. :changelog:

History
-------

1.9.0 (2022-06-17)
++++++++++++++++++

* Feat: Support for Django 4.0

1.7.0 (2021-3-22)
+++++++++++++++++

* Feat: Added SEARCH_COMBINED_FIELDS to SearchQuerySetMixin
* Fix: SearchQuerySetMixin for nested search

1.6.0 (2020-12-1)
+++++++++++++++++

* Feat: Added ExporterModel and ImporterModel

1.5.0 (2020-12-1)
+++++++++++++++++

* Added UnaccentSearchFilter
* Migration to poetry
* Some minor fixes

1.4.0 (2020-05-25)
+++++++++++++++++

* Added AnnotatedField

1.3.1 (2019-10-21)
+++++++++++++++++

* Fixed error in update status inside a handler

1.3.0 (2019-10-18)
+++++++++++++++++

* Added simple validation mixin
* Fixed recursion problem when save in transitions handlers
* Avoid status changes in transitions

1.2.0 (2019-10-8)
+++++++++++++++++

* Added SimpleSerializationMixin
* Added SimplePaginationMixin

1.1.0 (2019-10-7)
+++++++++++++++++

* Removed non used utilities
* Added StatusMixin
* Added SearchQuerySetMixin and SearchFilter
* Added ActionSerializersMixin
* Updated UploadToDir

1.0.0 (2018-10-2)
+++++++++++++++++

* Updated UploadToDir with ``prefix`` param.
* Contrib package with Django Rest Framework utils.

1.0a2 (2017-2-21)
+++++++++++++++++

* Added generators module.
* Added admin widget fot ForeignKeys

1.0a1 (2017-2-20)
+++++++++++++++++

* First release on PyPI.
