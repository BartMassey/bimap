# Copyright (c) 2017 Bart Massey
# This program is licensed under the "MIT License".
# Please see the file COPYING in the source
# distribution of this software for license terms.


"""Bijective map."""

class BiDict(dict):
    """Specialized subclass of dict() used internally by BiMap
    its keys and values mappings. This class overrides
    Python's del and bracket assignment to maintaing the
    bijection.

    """

    def __init__(self):
        self.codict = None

    def _set_codict(self, codict):
        self.codict = codict

    def __delitem__(self, key):
        """Delete the mapping with the given key from the
        BiDict. Also delete the mapping whose key
        corresponds to the value mapped by this key from the
        co-mapping.

        Raises KeyError(key) if the key to be deleted is not
        present.
        """
        if key not in self:
            raise KeyError(key)
        value = dict.__getitem__(self, key)
        dict.__delitem__(self, key)
        dict.__delitem__(self.codict, value)

    def __setitem__(self, key, value):
        """Add a mapping of the given key to the given value from
        the dictionary. Also add a mapping of the given
        value to the given key to the co-mapping. Adding
        these mappings may involve calling __delitem__ to
        delete conflicting mappings.
        """
        if key in self:
            del self[key]
        if value in self.codict:
            del self.codict[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self.codict, value, key)

    def pop(self, key, *args):
        """Remove specified key and return the
        corresponding value.  If key is not found, d is
        returned if given, otherwise KeyError is raised.
        """
        if len(*args) > 1:
            raise TypeError(
                'pop() takes 1 optional argument but more were given')
        if key not in self:
            if len(args) == 0:
                raise KeyError(key)
            else:
                return args[0]
        value = self[key]
        del self[key]
        return value

    def popitem(self):
        """Remove and return some (key, value) pair as a 2-tuple;
        but raise KeyError if empty.
        """
        k, v = dict.popitem(self)
        dict.__delitem__(self.codict, v)
        return (k, v)

    def setdefault(k, *args):
        """Defaulting a BiDict is disallowed as useless and error-prone."""
        raise AttributeError('BiDict cannot be defaulted')

class BiMap:

    """Two-way (bijective) dictionary map. Can lookup by key or
    by value. Both keys and values must be hashable.

    As with normal Python dictionaries, assignment is by
    replacement. If a newly-added mapping conflicts with the
    key or value of existing mappings the existing mappings
    will be silently replaced. This means that two mappings
    could be replaced: the one involving the conflicting
    value and and the one involving the conflicting key.

    Fields:

    keys -- BiDict mapping keys to values.
    values -- BiDict mapping values to keys.

    """

    def __init__(self, init=None):
        """Create a new BiMap. The optional initializer is a
        dictionary that will be used to provide an initial
        mapping.

        BiMap() -> new empty bimap
        BiMap(d), BiMap(init=d) ->
          new bimap initialized from dictionary d. The
          mappings of d will be inserted in an unknown
          order, so d should be a bijection.

        """
        self.keys = BiDict()
        self.values = BiDict()
        self.keys._set_codict(self.values)
        self.values._set_codict(self.keys)
        if init:
            if not isinstance(init, dict):
                raise TypeError('initializer is not dictionary')
            for k, v in init.items():
                self.keys[k] = v
