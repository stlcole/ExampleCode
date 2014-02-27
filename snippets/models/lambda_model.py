__author__ = 'cole'

from django.db import models
from django.db.models.loading import get_model

from picklefield import PickledObjectField  # pip install django-picklefield


class LambdaCode(models.Model):
    '''
    LambdaCode is a model for a lambda and its associated variables.

    lambda_string is the one required field and is used as follows:
            _calculator = eval(lambda_string)

      If an assignable lambda is written in the form
      (lambda *args: value_from_calculation), e.g. l = (lambda _: True),
      m = l, l(5) == m(False) == True, where 'l' is the name and
      '(lambda _: True)' is the expression, then
      lambda_string is the expression in QUOTATION MARKS, e.g.
      "(lambda _: True)", which makes a lambda_string 'eval()-able'

    string_args is a list of inputs for lambda_string.format()
    each arg will correspond to a '{}' in the lambda_string, which allows

            lambda_string = lambda_string.format(*string_args)
            _calculator = eval(lambda_string)

      e.g. lambda_string = "(lambda _: {})", string_args = (3,)
      lambda_string.format(*string_args) = "(lambda _: 3)"

    lambda_variables provides a list of variable attribute names
    to be converted into values for input into the lambda function; e. g.

            lambda_string = "(lambda x: x * 2)"
            lambda_variables = "['foo']",
            getattr(model, 'foo') = 24,
            _inputs = [getattr(model, v) for v in lambda_variables]
            _calculator = eval(lambda_string)
            _calculator(*_inputs) = 42

    app_model_name is a string in the form "app.model"

    model_get_key_value is a dict for the parameter and value
    used to get a specific model instance. So if
    inst = model.objects.get('id'=1), then
    model_get_key_value = {'id': 1}. All kwargs used by
    models.objects.get('k1'=v1, 'k2'=v2, ...) must be in
    model_get_key_value

    A model can call a LambdaCode lambda, and provide inputs directly
    to the lambda, getting the appropriate return value.

    Alternatively, by providing 'model_app_string' and
    'model_get_key_value' a LambdaCode object can
    create the lambda, get its needed inputs and return its value
    '''

    name = models.CharField(max_length=80, unique=True)
    lambda_string = models.TextField()
    string_args = PickledObjectField(blank=True, null=True)
    lambda_variables = PickledObjectField(blank=True, null=True)
    lambda_doc = models.TextField(blank=True, null=True)
    app_model_name = models.CharField(max_length=80, blank=True, null=True)
    model_get_key_value = PickledObjectField(blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def _complete_lambda_string(self):
        if self.string_args:
            return self.lambda_string.format(*self.string_args)
        else:
            return self.lambda_string

    def get_lambda(self):
        return eval(self._complete_lambda_string)

    @property
    def _lambda(self):
        return self.get_lambda()

    def set_instance(self, inst):
        self._model_instance = inst

    @property
    def app_model(self):
        return get_model(*self.app_model_name.split('.', 1))

    @property
    def model_instance(self):
        if not hasattr(self, '_model_instance'):
            self._model_instance = self.app_model.objects.get(**self.model_get_key_value)
        return self._model_instance

    def _attribute_lookup(self, components, lookup_object=None):
        '''
        _attribute_lookup takes a list of related keywords (i.e. attributes of attributes),
        and constructs the object which has the final component keyword.
        e.g. ['user', 'name'] constructs the object self.user
        and then returns the value of self.user.name

        recursion is used to handle a component list of length n.
        '''

        component = components.pop(0)
        lookup_value = getattr(lookup_object or self.model_instance, component)

        if components:
            lookup_value = self._attribute_lookup(components, lookup_value)

        return lookup_value

    def set_variables(self, variables):
        self._variables_list = variables

    def variables_list(self, variables=None):
        '''
        returns a list of values for each variable listed in inputs
        '''

        if hasattr(self, '_variables_list'):
            return self._variables_list

        variables = variables or self.lambda_variables
        variable_list = []
        if isinstance(variables, list or tuple):
            for v in variables:
                variable_list.append(self._attribute_lookup(v.split('.')))

        else:
            variable_list = [variables]

        self._variables_list = variable_list
        return self._variables_list

    def _calculate(self):

        ### WORKFLOW ###################################################
        # 1. create a _calculator by evaling the appropriate
        #    lambda code string, which defines the actual calculation
        # 2. get the list of input values from a list of variables
        #
        # NOTE: the combination of #1 and #2 allows for unique
        # calculations for each individual ltip award,
        # providing needed flexibility should the ltip plan change
        #
        # 3. return the value created by the lambda and variable values
        ################################################################

        _calculator = self.get_lambda()
        _inputs = self.variables_list(self.lambda_variables)
        return _calculator(*_inputs)

    @property
    def value(self):
        return self._calculate()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.model_get_key_value:
            assert isinstance(self.model_get_key_value, dict), \
                'A dict is required for this model_get_key_value'

        try:
            _ = eval(self.lambda_string)

        except:
            assert False, "lambda string is un-eval()-able"

        super(LambdaCode, self).save(force_insert=False, force_update=False, using=None,
                                     update_fields=None)

    def __unicode__(self):
        return self.name