from abc import ABCMeta, abstractmethod
from pprint import pprint
from typing import List, Tuple, Set, Dict, Union
import json
import pickle


class SerializationInterface(metaclass=ABCMeta):

    @abstractmethod
    def save_to_file(self):
        ...

    @abstractmethod
    def read_from_file(self):
        ...


class Serialization_json(SerializationInterface):
    def __init__(self, file_name="python_data_containers.json") -> None:
        self.file_name = file_name

    def save_to_file(self, value: Union[List[Union[str, int, float, bool]], Tuple[Union[str, int, float, bool]], Set[Union[str, int, float, bool]], Dict[Union[str, int, float, bool], Union[str, int, float, bool]]]):

        with open(self.file_name, "w") as fh:
            json.dump(value, fh)

    def read_from_file(self):

        with open(self.file_name, "r") as fh:
            unpacked = json.load(fh)

        return unpacked


class Serialization_bin(metaclass=ABCMeta):
    def __init__(self, file_name="python_data_containers.bin") -> None:
        self.file_name = file_name

    def save_to_file(self, value: Union[List[Union[str, int, float, bool]], Tuple[Union[str, int, float, bool]], Set[Union[str, int, float, bool]], Dict[Union[str, int, float, bool], Union[str, int, float, bool]]]):

        with open(self.file_name, "wb") as fh:
            pickle.dump(value, fh)

    def read_from_file(self):

        with open(self.file_name, "rb") as fh:
            unpacked = pickle.load(fh)

        return unpacked


class Meta(type):

    children_number = 0

    def __new__(mcs, name, bases, namespace, **kwargs):
        new_cls = super().__new__(mcs, name, bases, namespace)
        new_cls.class_number = mcs.children_number
        mcs.children_number += 1
        return new_cls

    # def __call__(cls, *args, **kwargs):
    #    print(f'{cls} __call__ metaclass called')
    #    return super().__call__(*args, **kwargs)


class Cls1(metaclass=Meta):
    def __init__(self, data):
        self.data = data


class Cls2(metaclass=Meta):
    def __init__(self, data):
        self.data = data


if __name__ == '__main__':

    assert (Cls1.class_number, Cls2.class_number) == (0, 1)
    a, b = Cls1(''), Cls2('')
    assert (a.class_number, b.class_number) == (0, 1)

    some_data = {
        'tuple': 'tuple',
        2: [1, 2, 3],
        'a': {'key': 'value'}
    }

    serialization_json = Serialization_json()
    serialization_json.save_to_file(some_data)
    pprint(serialization_json.read_from_file())

    serialization_bin = Serialization_bin()
    serialization_bin.save_to_file(some_data)
    pprint(serialization_bin.read_from_file())
