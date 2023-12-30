from random import randint
from typing import Union


def run(min_value: int, max_value: int) -> Union[int, None]:
    try:
        generated_number = int(randint(int(min_value), int(max_value)))
    except Exception:
        generated_number = None

    return generated_number
