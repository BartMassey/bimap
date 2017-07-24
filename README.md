# BiMap - Bijective Dictionary for Python
Copyright (c) 2017 Bart Massey

The `bimap` module provides a `BiMap` class that
maintaings a bijective mapping between its keys and values
through the use of two separate dictionaries. A bijective
mapping is one in which each key uniquely corresponds to a
value, and each value uniquely corresponds to a key. This
data structure thus provides a way to efficiently map
between, for example, symbolic names and integer ids.

## Description

A `BiMap` has a `keys` field and a `values` field.  These
are used just like ordinary Python `dict`s: reference,
assignment and deletion are as expected.

Addition or deletion of a mapping in the `keys` dictionary
of a `BiMap` will be reflected in its `values` dictionary,
and vice-versa. If adding a mapping would break the
bijection, existing conflicting mappings will first be
deleted to preserve the bijection. This could be cause two
existing mappings to be deleted: see the example below.

## Example

    >>> from bimap import *
    >>> d = BiMap({"hello":1, "goodbye":2})
    >>> d.keys
    {'hello': 1, 'goodbye': 2}
    >>> d.values
    {1: 'hello', 2: 'goodbye'}
    >>> d.keys['goodbye'] = 1
    >>> d.keys
    {'goodbye': 1}
    >>> d.values
    {1: 'goodbye'}
    >>> d.values[1]
    'goodbye'

## License

This work is available under the "MIT License." Please see
the file COPYING in this distribution for license terms.
