import json
import sys
from typing import Dict


class GenericObject:
    def __init__(self):
        pass

    def __str__(self):
        return type(self).__name__ + ": " + str(self.__dict__)

    def __repr__(self):
        return str(self)


def obj_to_json(obj):
    def default(obj) -> Dict:
        obj_type = type(obj)
        json_repr = dict(obj.__dict__) if hasattr(obj, '__dict__') else {}
        if isinstance(obj, GenericObject):
            if '__json_object_type_name__' in json_repr:
                json_repr['__json_object_type_name__'] = obj.__dict__['__json_object_type_name__']
        else:
            json_repr['__json_object_type_name__'] = obj_type.__name__
        return json_repr

    return json.dumps(obj, default=default)


def obj_from_json(json_str: str):
    def object_hook(json_dict: Dict):
        json_repr = dict(json_dict)
        obj = None
        if '__json_object_type_name__' in json_dict:
            obj_class_name = json_dict['__json_object_type_name__']
            try:
                obj_class = getattr(sys.modules[__name__], obj_class_name)
                obj = obj_class()
                del json_repr['__json_object_type_name__']
            except AttributeError:
                pass
        #                print('WARNING: class \'' + obj_class_name + '\' was not found in the Python environment. ' +
        #                       'Loading as a '+GenericObject.__name__+'...')
        else:
            pass
        #            print('WARNING: field __json_object_type_name__ was not found in for a JSON object. '
        #                  'Loading as a JsonObject...')

        if obj is None:
            obj = GenericObject()

        obj.__dict__ = json_repr
        return obj

    return json.loads(json_str, object_hook=object_hook)


if __name__ == '__main__':
    class Test1:
        def __init__(self):
            self.test1_field1 = ''

        def __str__(self):
            return 'Test1{test1_field1=' + self.test1_field1 + '}'

        def __repr__(self):
            return str(self)


    loaded_json = obj_from_json('{'
                                '"test2_field1": "test2", '
                                '"test2_field2": {"test1_field1": "test1", "__json_object_type_name__": "Test1"}, '
                                '"__json_object_type_name__": "Test2"'
                                '}')
    print('loaded_json:', loaded_json)

    dumped_json = obj_to_json(loaded_json)
    print('dumped_json:', dumped_json)
