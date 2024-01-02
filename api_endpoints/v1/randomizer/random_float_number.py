from random import uniform, randint, choice
from typing import Union


def main(min_value: float, max_value: float) -> Union[float, None]:
    try:
        max_value_decimal_cases = len(str(max_value).split('.')[1])

        if max_value_decimal_cases == 0:
            generated_number = float(randint(int(min_value), int(max_value)))
        else:
            generated_number = float(round(uniform(min_value, max_value), choice(range(1, max_value_decimal_cases + 1))))
    except Exception:
        return None

    return generated_number
