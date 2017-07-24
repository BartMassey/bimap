# Copyright (c) 2017 Bart Massey

# Dictionary map.

class _Dict(dict):
    """Specialized dictionary used internally by BiDict for the
    keys and values mappings. Supports Python's del and
    bracket assignment appropriately.
    """
    def __init__(self):
        self.sibling = None

    def _set_sibling(self, sibling):
        self.sibling = sibling

    def __delitem__(self, key):
        if key not in self:
            raise KeyError(key)
        selfdict = super(_Dict, self)
        value = selfdict.__getitem__(key)
        selfdict.__delitem__(key)
        super(_Dict, self.sibling).__delitem__(value)

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        if value in self.sibling:
            del self.sibling[value]
        super(_Dict, self).__setitem__(key, value)
        super(_Dict, self.sibling).__setitem__(value, key)

class BiDict:
    """Two-way (bijective) dictionary map. Can lookup key by
       content, or content by key. Both content and key must be
       hashable.

       As with normal Python dictionaries, assignment is by
       replacement. If during a new mapping conflicts with
       the key or value of existing mappings the existing
       mappings will be silently replaced. This means that
       two mappings could be replaced: the one involving the
       conflicting value and and the one involving the
       conflicting key.
    """

    def __init__(self, init=None):
        """Create a new BiDict. Use the resulting .value dictionary
           for standard lookup and the .key dictionary for
           reverse lookup. The optional initializer is a
           dictionary that will be used to provide an
           initial mapping.
        """
        self.keys = _Dict()
        self.values = _Dict()
        self.keys._set_sibling(self.values)
        self.values._set_sibling(self.keys)
        if init:
            if not isinstance(init, dict):
                raise TypeError('initializer is not dictionary')
            for k, v in init.items():
                self.keys[k] = v
