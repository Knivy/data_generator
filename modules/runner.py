"""Модуль с вызовами других модулей."""

from typing import Generator

from .params import ParamsObject

# Собирает все параметры и создает объекты классов.
params_object: ParamsObject = ParamsObject()

# Отдает данные построчно списками строк.
data_source: Generator = params_object.data_source.get_data()
