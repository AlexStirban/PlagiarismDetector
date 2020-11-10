import pathlib

from collections import Counter
from errors import *
from errno import ENOENT
from os import strerror


# TODO:
#   - Add proper documentation to methods

class DependencyRelations:
    def __init__(self, obj, nlp, from_dep=False):
        self._nlp = nlp
        if from_dep:
            self.__list = obj
        else:
            self.__list = self._dep_rel_as_list(obj)

    def __repr__(self):
        head = "\n".join(str(x) for x in self.__list[:5])
        return "DependecyRelations\nHead:\n{}\n ...".format(head)

    def __getitem__(self, item):
        return self.__list[item]

    def __iter__(self):
        return iter(self.__list)

    def _dep_rel_as_list(self, text):
        dependencies = []
        doc = self._nlp(text)

        for s in doc.sentences:
            for w in s.words:
                dependencies.append((w.text,
                                     s.words[w.head - 1].text if w.head > 0 else "root",
                                     w.deprel))
        return dependencies

    @classmethod
    def from_txt_file(cls, file_path: pathlib.PurePath, nlp):
        # Check if we have a PurePath object
        if not isinstance(file_path, pathlib.PurePath):
            raise NotPurePathError

        # Check if path exists, if not raise exception
        if not (file_path.exists()):
            raise FileNotFoundError(ENOENT, strerror(ENOENT), file_path)

        with open(file_path, "r", encoding="utf-8-sig") as f:
            return cls(f.read(), nlp)

    @classmethod
    def from_dep_file(cls, file_path: pathlib.PurePath, nlp):
        # Check if we have a PurePath object
        if not isinstance(file_path, pathlib.PurePath):
            raise NotPurePathError

        # Check if path exists, if not raise exception
        if not (file_path.exists()):
            raise FileNotFoundError(ENOENT, strerror(ENOENT), file_path)

        with open(file_path, "r", encoding="utf-8-sig") as f:
            return cls([tuple(line.rstrip().split("~")) for line in f.readlines()], nlp, from_dep=True)

    @classmethod
    def from_str(cls, text_str: str, nlp):
        return cls(text_str, nlp)

    def save(self, file_path: pathlib.PurePath):
        # Check if we have a PurePath object
        if not isinstance(file_path, pathlib.PurePath):
            raise NotPurePathError

        with open(file_path, "w", encoding="utf-8-sig") as f:
            f.write("\n".join(["~".join(x) for x in self.__list]))

    def similarity(self, dep):
        a = Counter(self.__list)
        b = Counter(list(dep))

        return len(a & b) / len(a)
