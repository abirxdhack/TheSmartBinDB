Luhn validation
===============

The Luhn algorithm is the standard checksum used to detect single-digit
errors and most adjacent transpositions in card numbers. SmartBinDB exposes
the ``"Luhn": true`` flag on every successful response to indicate that the
returned BIN is part of a Luhn-conformant card numbering scheme.

Reference implementation
------------------------

.. code-block:: python

    def luhn_ok(pan: str) -> bool:
        digits = [int(c) for c in pan if c.isdigit()]
        checksum = 0
        for i, d in enumerate(reversed(digits)):
            if i % 2 == 1:
                d *= 2
                if d > 9:
                    d -= 9
            checksum += d
        return checksum % 10 == 0

    print(luhn_ok("4571730000000000"))

Generate a Luhn-valid PAN from a BIN
------------------------------------

.. code-block:: python

    import random

    def make_pan(bin_value: str, length: int = 16) -> str:
        body = bin_value + "".join(str(random.randint(0, 9)) for _ in range(length - len(bin_value) - 1))
        digits = [int(c) for c in body]
        checksum = 0
        for i, d in enumerate(reversed(digits)):
            if i % 2 == 0:
                d *= 2
                if d > 9:
                    d -= 9
            checksum += d
        check = (10 - (checksum % 10)) % 10
        return body + str(check)

    print(make_pan("457173"))
