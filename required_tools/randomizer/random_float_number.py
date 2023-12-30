from random import uniform, choice
from typing import Union


def run(min_value: float, max_value: float) -> Union[float, None]:
    try:
        max_cases = len(str(max_value).split('.')[1])
        _ = len(str(min_value).split('.')[0])
        generated_number = float(round(uniform(float(min_value), float(max_value)), choice(range(1, max_cases + 1))))
    except Exception:
        return None

    return generated_number
