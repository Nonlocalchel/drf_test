import sys


def get_model_fields(model) -> list:
    return [field.name for field in model._meta.fields]  # картв с типами и именами полей?еще одна утилита в services?


def get_class_by_name(name, module_name=__name__) -> object:
    module = sys.modules[module_name]
    class_ = getattr(module, name.capitalize())
    return class_


def get_dict_instance(model) -> dict:
    instance = model()
    result_instance_dict = {}
    instance_dict = instance.__dict__
    for field_key, field_value in instance_dict.items():
        if not (field_key.startswith('_') or field_key.endswith('id')):
            result_instance_dict[field_key] = field_value

    return result_instance_dict
