# QuickMap
![Unit-Tests](https://github.com/roymanigley/QuickMap/actions/workflows/test.yml/badge.svg)  
![Published Python Package](https://github.com/roymanigley/QuickMap/actions/workflows/publish.yml/badge.svg)

> Quick and Simple Class-to-Dict Mapping for Python using decorators  

Welcome to QuickMap, your go-to library for fast and straightforward mapping between Python classes and dictionaries. QuickMap is designed to make the process of serializing and deserializing data between classes and dictionaries as seamless and efficient as possible.  

With QuickMap, you can:

- Quickly Convert Classes to Dictionaries: Serialize your class instances into dictionaries effortlessly, capturing all attributes and their values.
- Easily Recreate Classes from Dictionaries: Deserialize dictionaries back into class instances with ease, ensuring your data maintains its structure and type integrity.
- Customize Your Mappings: Define custom conversion rules and transformations for specific use cases, giving you the flexibility to handle complex scenarios.
- Enhance Your Workflow: Save development time and reduce boilerplate code with QuickMap’s intuitive and easy-to-use API.
Built with speed and simplicity in mind, QuickMap integrates seamlessly into any Python project. Whether you're an experienced developer or new to Python, QuickMap's comprehensive documentation and practical examples will help you get started quickly.


## Installation
```
pip install quickmap
```
or from Github:
```
git clone https://github.com/roymanigley/quickmap.git
cd quickmap
pip install -r requirements.txt
python setup.py install
```
## Usage

### map from `object` to `dict`
```python
from quickmap import mapping

class Dummy:
    name: str

# define the mapping
@mapping(target='name', source='dummy.name')
# define the source type using the type hint on the `do_mapping` function
# define the target type using the return type hint
def do_mapping(dummy: Dummy) -> dict:
    pass

# call then mapping function
dummy = Dummy()
dummy.name = 'alpha'
dummy = do_mapping(dummy)
print(dummy['name'])
```

### map from `dict` to `object`
```python
from quickmap import mapping

class Dummy:
    name: str

# define the mapping
@mapping(target='name', source='dummy.name')
# define the source type using the type hint on the `do_mapping` function
# define the target type using the return type hint
def do_mapping(dummy: dict) -> Dummy:
    pass

# call then mapping function
dummy = do_mapping({'name': 'alpha'})
print(dummy.name)
```

### map from multiple arguments
```python
from quickmap import mapping

class Dummy:
    name_1: str
    name_2: str

# define the mapping
@mapping(target='name_1', source='dummy_1.name')
@mapping(target='name_2', source='dummy_2.name')
# define the source type using the type hint on the `do_mapping` function
# define the target type using the return type hint
def do_mapping(dummy_1: dict, dummy_2: dict) -> Dummy:
    pass

# call then mapping function
dummy = do_mapping(dummy_1={'name': 'alpha'}, dummy_2={'name': 'bravo'})
print(dummy.name_1, dummy.name_2)
```

### Example
```python
import unittest
from quickmap import mapping

class MapToComplexTestCase(unittest.TestCase):

    def test_from_dict(self):
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


if __name__ == '__main__':
    unittest.main()
```
