##############################################################################
# COPYRIGHT Ericsson AB 2013
#
# The copyright to the computer program(s) herein is the property of
# Ericsson AB. The programs may be used and/or copied only with written
# permission from Ericsson AB. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################


import unittest
from dnsclient_extension.dnsclientextension import DNSClientExtension
from dnsclient_extension.dnsclientextension import MaxCountValidator
from dnsclient_extension.dnsclientextension import MaxLengthValidator
from litp.core.validators import ValidationError


class TestDNSClientExtension(unittest.TestCase):

    def setUp(self):
        self.ext = DNSClientExtension()

    def test_property_types_registered(self):
        # Assert that only extension's property types
        # are defined.
        prop_types_expected = ['position_value','comma_separated_domain_names']
        prop_types = [pt.property_type_id for pt in
                      self.ext.define_property_types()]
        self.assertEquals(prop_types_expected, prop_types)

    def test_item_types_registered(self):
        # Assert that only extension's item types
        # are defined.
        item_types_expected = ['dns-client','nameserver']
        item_types = [it.item_type_id for it in
                      self.ext.define_item_types()]
        diff = [x for x in item_types_expected if x not in item_types]
        self.assertEquals(len(diff), 0)

    def test_max_length_items(self):
        # Assert that only extension's item types
        # are defined.
        validator = MaxLengthValidator(12)
        error = validator.validate("property_value_string_more_than_12")
        ref_errors = ValidationError(error_message = ("Length of property cannot be more than 12 characters"))

        self.assertEquals(error,ref_errors)

        correct = validator.validate("less_than_12")
        self.assertEquals(None,correct)

    def test_max_count_items(self):
        # Assert that only extension's item types
        # are defined.
        validator = MaxCountValidator(3,6,',')
        error_max = validator.validate("test1.com,test2.com,test3.com,test4.com,test5.com,test6.com,test7.com")
        ref_errors_max = ValidationError(error_message = ("A maximum of 6 domains per search may be specified"))
        self.assertEquals(error_max,ref_errors_max)

        error_min = validator.validate("test1.com,test2.com")
        ref_errors_min = ValidationError(error_message = ("A minium of 3 domains per search may be specified"))
        self.assertEquals(error_max,ref_errors_max)
        
        correct = validator.validate("test1.com,test2.com,test3.com")
        self.assertEquals(None,None)

if __name__ == '__main__':
    unittest.main()
