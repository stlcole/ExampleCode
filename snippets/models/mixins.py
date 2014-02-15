__author__ = 'cole'

from django.db import models


class LambdaMixin(models.Model):
    lambda_code = models.TextField
    lambda_variables = models.TextField


    def _attribute_lookup(self, components, lookup_object=None):
        '''
        _attribute_lookup takes a list of related keywords (i.e. attributes of attributes),
        and constructs the object which has the final component keyword.
        e.g. ['profile', 'birthday'] constructs the object self.quarter
        and then returns the value of self.profile.birthday

        recursion is used to handle a component list of length n.
        '''

        component = components.pop(0)
        lookup_value = getattr(lookup_object or self, component)

        if components:
            lookup_value = self._attribute_lookup(components, lookup_value)

        return lookup_value

    def _input_list(self, input_items):
        '''
        returns a list of values for each variable listed in inputs
        '''

        input_list = []
        if isinstance(input_items, list or tuple):
            for item in input_items:
                input_components = item.split('.')
                input_list.append(self._attribute_lookup(input_components))

        else:
            input_list = [input_items, ]

        return input_list

    def _calculate(self, lambda_expression, lambda_variables):

        ### WORKFLOW ###################################################
        # 1. create the scaling function by evaling the appropriate
        #    lambda string, which defines the actual scaling calculation
        # 2. get the list of input values from a list of variables
        #
        # NOTE: the combination of #1 and #2 allows for a unique
        # scaling calculation for each individual ltip award,
        # providing needed flexibility should the ltip plan change
        #
        # 3. return the value created by the lambda and variable values
        ################################################################

        _calculator = eval(lambda_expression)
        _inputs = self._input_list(lambda_variables)
        return _calculator(*_inputs)