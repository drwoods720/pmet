#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

R = TypeVar("R")  # return type


class Parser(ABC, Generic[R]):
    @abstractmethod
    def parse(self, filepath: str) -> R: ...
