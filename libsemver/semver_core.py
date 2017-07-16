"""
SemVerCore top level class
"""

class SemVerCore(object):
    """
    Core Semantic Version class
    """

    def __init__(self, major, minor, patch, prerelease=None, build_meta=None):
        """
        Initialize a SemVerCore class by providing the attributes
        """
        assert isinstance(major, int) and major >= 0
        self._major = major

        assert isinstance(minor, int) and minor >= 0
        self._minor = minor

        assert isinstance(patch, int) and patch >= 0
        self._patch = patch

        self._prerelease = None
        self.prerelease = prerelease

        self._build_meta = None
        self.build_metadata = build_meta


    def __str__(self):
        """
        Print a string representation of the SemVerCore object
        """
        version_str = '%d.%d.%d' % (self._major, self._minor, self._patch)

        if self._prerelease is not None:
            version_str += '-' + '.'.join([str(e) for e in self._prerelease])

        if self._build_meta is not None:
            version_str += '+' + '.'.join([str(e) for e in self._build_meta])

        return version_str


    @staticmethod
    def _compare_semvers(rel1, rel2):
        """
        Compare two SemVerCore objects, returns negative, 0 or positive
        depending on the ordering
        """

        def py3cmp(obj1, obj2):
            """
            Local function to replace cmp
            """
            return (obj1 > obj2) - (obj1 < obj2)

        # Assume the two are equal
        _cmp = 0

        if rel1.major != rel2.major:
            _cmp = py3cmp(rel1.major, rel2.major)
        elif rel1.minor != rel2.minor:
            _cmp = py3cmp(rel1.minor, rel2.minor)
        elif rel1.patch != rel2.patch:
            _cmp = py3cmp(rel1.patch, rel2.patch)

        if _cmp != 0:
            return _cmp

        # Prereleases have a lower precedence than the normal version
        if rel1.prerelease is None:
            if rel2.prerelease is not None:
                _cmp = 1
        else:
            if rel2.prerelease is None:
                _cmp = -1

        if _cmp != 0:
            return _cmp

        # Both objects have prerelease lists, start iterating them
        for el_r1, el_r2 in zip(rel1.prerelease, rel2.prerelease):
            # Compare if the types are identical
            if type(el_r1) == type(el_r2):
                _cmp = py3cmp(el_r1, el_r2)
                if _cmp != 0: break
            else:
                # The types can only be int or str
                # int's compare lower than str's
                if isinstance(el_r1, int):
                    _cmp = -1
                    break
                else:
                    _cmp = 1
                    break

        if _cmp == 0:
            # At this point, we've compared two lists and all the elements up
            # to the length of the shorter list are identical. The only
            # possible difference now is the size of the lists. The longer list
            # is the greater one.
            _cmp = len(rel1) - len(rel2)

        return _cmp


    def __lt__(self, other):
        """
        Return True if `self` < `other, False otherwise

        Compare using standard Semantic Version comparision rules
        """
        return SemVerCore._compare_semvers(self, other) in [-1]


    def __le__(self, other):
        """
        Return True if `self` <= `other, False otherwise

        Compare using standard Semantic Version comparision rules
        """
        return SemVerCore._compare_semvers(self, other) in [-1, 0]


    def __gt__(self, other):
        """
        Return True if `self` > `other, False otherwise

        Compare using standard Semantic Version comparision rules
        """
        return SemVerCore._compare_semvers(self, other) in [1]


    def __ge__(self, other):
        """
        Return True if `self` >= `other, False otherwise

        Compare using standard Semantic Version comparision rules
        """
        return SemVerCore._compare_semvers(self, other) in [0, 1]


    def __eq__(self, other):
        """
        Return True if `self` == `other, False otherwise

        Compare using standard Semantic Version comparision rules
        """
        return SemVerCore._compare_semvers(self, other) in [0]


    def __ne__(self, other):
        """
        Return True if `self` != `other, False otherwise

        Compare using standard Semantic Version comparision rules
        """
        return SemVerCore._compare_semvers(self, other) in [-1, 1]


    @property
    def major(self):
        """
        Return the major version from the SemVerCore object
        """
        return self._major


    @major.setter
    def major(self, value):
        """
        Set the major number in the SemVerCore object
        """
        try:
            _major = int(value)
        except TypeError:
            raise TypeError('major number must be an integer')

        if _major < 0:
            raise TypeError('major number must be a positive integer')

        self._major = _major


    @property
    def minor(self):
        """
        Return the minor version from the SemVerCore object
        """
        return self._minor


    @minor.setter
    def minor(self, value):
        """
        Set the minor number in the SemVerCore object
        """
        try:
            _minor = int(value)
        except TypeError:
            raise TypeError('minor number must be an integer')

        if _minor < 0:
            raise TypeError('minor number must be a positive integer')

        self._minor = _minor


    @property
    def patch(self):
        """
        Return the patch version from the SemVerCore object
        """
        return self._patch


    @patch.setter
    def patch(self, value):
        """
        Set the patch number in the SemVerCore object
        """
        try:
            _patch = int(value)
        except TypeError:
            raise TypeError('patch number must be an integer')

        if _patch < 0:
            raise TypeError('patch number must be a positive integer')

        self._patch = _patch


    @property
    def prerelease(self):
        """
        Return the prerelease information from the SemVerCore object
        """
        return self._prerelease


    @prerelease.setter
    def prerelease(self, value):
        """
        Set the prerelease information in the SemVerCore object

        value must be a list of strings and/or integers. If an element
        is a string representation of an integer, it is converted to the
        integer representation in base 10.
        """
        assert value is None or isinstance(value, list)
        # Convert integer portions of prerelease strings to integer
        if value is not None:
            parsed = []
            for elem in value:
                try:
                    elem = int(elem)
                except ValueError:
                    assert '.' not in elem
                parsed.append(elem)

            if len(parsed) == 0:
                parsed = None
        else:
            parsed = None

        self._prerelease = parsed


    @property
    def build_metadata(self):
        """
        Return the build metatdata information from the semver object
        """
        return self._build_meta


    @build_metadata.setter
    def build_metadata(self, value):
        """
        Set the build metadata in the SemVerCore object

        value must be a list. Elements of the list are converted to
        their corresponding string representations
        """
        assert value is None or isinstance(value, list)

        if value is not None:
            if len(value) == 0:
                _build_meta = None
            else:
                _build_meta = [str(e) for e in value]
                assert all(['.' not in e for e in _build_meta])
        else:
            _build_meta = None

        self._build_meta = _build_meta


