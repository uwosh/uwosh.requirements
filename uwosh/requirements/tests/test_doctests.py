import unittest
import doctest

from zope.testing import doctestunit
from zope.component import testing, eventtesting
from Products.PloneTestCase import PloneTestCase 
from Testing import ZopeTestCase as ztc
from uwosh.requirements.tests.base import UWOshRequirementsFunctionalTestCase

def test_suite():
    return unittest.TestSuite([

        # Demonstrate the main content types
        ztc.ZopeDocFileSuite(
            'browser.txt', package='uwosh.requirements.browser',
            test_class=UWOshRequirementsFunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        ]
        )

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
