import doctest
import iwlibs
import pyiwconfig

def _test_pyiwconfig():
    return doctest.testmod(pyiwconfig)

def _test_iwlibs():
    return doctest.testmod(iwlibs)

if __name__ == "__main__":
    _test_iwlibs()
    _test_pyiwconfig()
