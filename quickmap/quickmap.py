from dataclasses import dataclass
from types import SimpleNamespace
from typing import Optional


def __is_dict(c: type) -> bool:
    return c == dict


def __extract_value(*, source: str, function: callable, **kwargs) -> any:
    attribute_path = source.split('.')
    value = kwargs
    for attribute in attribute_path:
        if __is_dict(type(value)):
            value = value.get(attribute)
        else:
            value = getattr(value, attribute)
    return function(value) if function else value


def __set_value(*, target: str, target_instance: any, value: any) -> None:
    attribute_path = target.split('.')
    for i in range(len(attribute_path) - 1):
        if __is_dict(type(target_instance)):
            target_instance = __get_next_value_dict(
                target_instance, attribute_path[i])
        else:
            target_instance = __get_next_value_object(
                target_instance, attribute_path[i])

    if __is_dict(type(target_instance)):
        target_instance[attribute_path[-1]] = value
    else:
        setattr(target_instance, attribute_path[-1], value)


def __get_next_value_dict(target_instance: dict, attribute: str) -> any:
    value = target_instance.get(attribute)
    if value is None:
        target_instance[attribute] = {}
    return target_instance[attribute]


def __get_next_value_object(target_instance: object, attribute: str) -> any:
    if hasattr(target_instance, attribute):
        value = getattr(target_instance, attribute)
    else:
        value = None
    if value is None:
        target_type = __identify_object_attribute_type(
            target_instance, attribute)
        setattr(target_instance, attribute, target_type())
    return getattr(target_instance, attribute)


def __identify_object_attribute_type(target_instance: object, attribute: str) -> type:
    default_type = SimpleNamespace
    if hasattr(target_instance, '__annotations__'):
        return target_instance.__annotations__.get(attribute, default_type)
    else:
        return default_type


@dataclass
class MappingDescription:
    source: str
    target: str
    function: Optional[callable]


def mapping(*, source: str, target: str, function: callable = None):

    def wrapper(func: callable):
        return_type = func.__annotations__.get('return')
        if return_type is None:
            raise Exception(f'missing return type hint on "{func.__name__}"')

        if not hasattr(func, '__mapping_descriptions'):
            func.__mapping_descriptions = []
        func.__mapping_descriptions.append(
            MappingDescription(source=source, target=target, function=function)
        )

        def inner(**kwargs):
            required_kwargs = set([md.source.split('.')[0]
                                  for md in func.__mapping_descriptions])
            missing_kwargs = [kw for kw in list(
                required_kwargs) if kw not in kwargs.keys()]
            if missing_kwargs:
                raise Exception(
                    f'missing kwargs in "{func.__name__}": {missing_kwargs}')
            mapped_value = return_type()
            for mapping_description in func.__mapping_descriptions:
                try:
                    value = __extract_value(
                        source=mapping_description.source,
                        function=mapping_description.function,
                        **kwargs
                    )
                    __set_value(
                        target=mapping_description.target,
                        target_instance=mapped_value,
                        value=value
                    )
                except Exception as e:
                    raise Exception(
                        f'unexpected error in "{func.__name__} during the mapping: {mapping_description}', e
                    ) from e
            return mapped_value

        inner.__annotations__['return'] = return_type
        inner.__mapping_descriptions = func.__mapping_descriptions
        inner.__name__ = func.__name__
        return inner

    return wrapper
