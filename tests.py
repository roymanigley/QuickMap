import unittest
from quickmap import mapping


class MapToComplexTestCase(unittest.TestCase):

    def test_complex_from_object(self):
        # GIVEN

        class Address:
            street: str
            zip: str
            city: str

        class Customer:
            name: str
            address: Address

        class Order:
            name: str
            customer: Customer

        address = Address()
        address.street = 'Evergreen 22'
        address.zip = '0815'
        address.city = 'Springfield'

        customer = Customer()
        customer.name = 'alpha corp'
        customer.address = address

        order = Order()
        order.name = 'order_01'
        order.customer = customer

        @mapping(target='name', source='order.name')
        @mapping(target='customer_name_uppercase', source='order.customer.name', function=str.upper)
        @mapping(target='customer.name', source='order.customer.name')
        @mapping(target='customer.address.street', source='order.customer.address.street')
        @mapping(target='customer.address.zip', source='order.customer.address.zip')
        @mapping(target='customer.address.city', source='order.customer.address.city')
        def do_mapping(order: Order) -> dict:
            pass

        # WHEN
        value: dict = do_mapping(order=order)
        # THEN
        self.assertEqual(type(value), dict)
        self.assertEqual(value['name'], 'order_01')
        self.assertEqual(value['customer_name_uppercase'], 'ALPHA CORP')
        self.assertEqual(value['customer']['name'], 'alpha corp')
        self.assertEqual(value['customer']['address']
                         ['street'], 'Evergreen 22')
        self.assertEqual(value['customer']['address']['zip'], '0815')
        self.assertEqual(value['customer']['address']['city'], 'Springfield')

    def test_complex_from_dict(self):
        # GIVEN
        source = {
            'name': 'order_01',
            'customer': {
                'name': 'alpha corp',
                'address': {
                    'street': 'Evergreen 22',
                    'zip': '0815',
                    'city': 'Springfield'
                }
            }
        }

        class Address:
            street: str
            zip: str
            city: str

        class Customer:
            name: str
            address: Address

        class Order:
            name: str
            customer: Customer
            customer_name_uppercase: str

        @mapping(target='name', source='order.name')
        @mapping(target='customer_name_uppercase', source='order.customer.name', function=str.upper)
        @mapping(target='customer.name', source='order.customer.name')
        @mapping(target='customer.address.street', source='order.customer.address.street')
        @mapping(target='customer.address.zip', source='order.customer.address.zip')
        @mapping(target='customer.address.city', source='order.customer.address.city')
        def do_mapping(order: dict) -> Order:
            pass

        # WHEN
        value: Order = do_mapping(order=source)
        # THEN
        self.assertEqual(type(value), Order)
        self.assertEqual(value.name, 'order_01')
        self.assertEqual(value.customer_name_uppercase, 'ALPHA CORP')
        self.assertEqual(value.customer.name, 'alpha corp')
        self.assertEqual(value.customer.address.street, 'Evergreen 22')
        self.assertEqual(value.customer.address.zip, '0815')
        self.assertEqual(value.customer.address.city, 'Springfield')


class MapToNestedTestCase(unittest.TestCase):

    def test_dict_nested_to_dict_nested(self):
        # GIVEN
        source = {'_a': 'a'}

        @mapping(target='b._b', source='a._a')
        def do_mapping(a: str) -> dict:
            pass

        # WHEN
        value = do_mapping(a=source)
        # THEN
        self.assertEqual(type(value), dict)
        self.assertEqual(value['b']['_b'], 'a')

    def test_dict_nested_to_object_nested(self):
        # GIVEN
        source = {'_a': 'a'}

        class DummyInner:
            _b: str

        class Dummy:
            b = None

        @mapping(target='b._b', source='a._a')
        def do_mapping(a: str) -> Dummy:
            pass

        # WHEN
        value = do_mapping(a=source)
        # THEN
        self.assertEqual(type(value), Dummy)
        self.assertEqual(value.b._b, 'a')


class MapToPrimitiveTestCase(unittest.TestCase):

    def test_primitive_types_to_dict(self):
        # GIVEN
        @mapping(target='b', source='a')
        def do_mapping(a: str) -> dict:
            pass

        # WHEN
        value = do_mapping(a='a')
        # THEN
        self.assertEqual(type(value), dict)
        self.assertEqual(value['b'], 'a')

    def test_primitive_types_nested_to_dict(self):
        # GIVEN
        @mapping(target='b', source='a._a')
        def do_mapping(a: str) -> dict:
            pass

        # WHEN
        value = do_mapping(a={'_a': 'a'})
        # THEN
        self.assertEqual(type(value), dict)
        self.assertEqual(value['b'], 'a')

    def test_primitive_types_to_object(self):
        # GIVEN
        class Dummy:
            b: str

        @mapping(target='b', source='a')
        def do_mapping(a: str) -> Dummy:
            pass

        # WHEN
        value = do_mapping(a='a')
        # THEN
        self.assertEqual(type(value), Dummy)
        self.assertEqual(value.b, 'a')

    def test_primitive_types_nested_to_object(self):
        # GIVEN
        class Dummy:
            b: str

        @mapping(target='b', source='a._a')
        def do_mapping(a: str) -> dict:
            pass

        # WHEN
        value = do_mapping(a={'_a': 'a'})
        # THEN
        self.assertEqual(type(value), dict)
        self.assertEqual(value['b'], 'a')


class MapWithMultipleArgumentsTestCase(unittest.TestCase):

    def test_multiple_object_arguments(self):
        # GIVEN
        class Dummy:
            name: str

        dummy_1 = Dummy()
        dummy_1.name = 'alpha'
        dummy_2 = Dummy()
        dummy_2.name = 'bravo'

        @mapping(target='name_1', source='dummy_1.name')
        @mapping(target='name_2', source='dummy_2.name')
        def do_mapping(dummy_1: Dummy, dummy_2: Dummy) -> dict:
            pass

        # WHEN
        dummy = do_mapping(dummy_1=dummy_1, dummy_2=dummy_2)
        # THEN
        self.assertEqual(dummy['name_1'], 'alpha')
        self.assertEqual(dummy['name_2'], 'bravo')

    def test_multiple_dict_arguments(self):
        # GIVEN
        class Dummy:
            name_1: str
            name_2: str

        dummy_1 = {'name': 'alpha'}
        dummy_2 = {'name': 'bravo'}

        @mapping(target='name_1', source='dummy_1.name')
        @mapping(target='name_2', source='dummy_2.name')
        def do_mapping(dummy_1: dict, dummy_2: dict) -> Dummy:
            pass

        # WHEN
        dummy = do_mapping(dummy_1=dummy_1, dummy_2=dummy_2)
        # THEN
        self.assertEqual(dummy.name_1, 'alpha')
        self.assertEqual(dummy.name_2, 'bravo')


if __name__ == '__main__':
    unittest.main()
