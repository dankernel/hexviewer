
from hexviewer import HexViewer
import numpy as np


def _test(TEST_MODE, size):

    # Init or Load
    if TEST_MODE == 'INT8':
        array = np.random.randint(0xFF, size=size, dtype=np.uint8)
    elif TEST_MODE == 'INT16':
        array = np.random.randint(0xFFFF, size=size, dtype=np.uint16)
    elif TEST_MODE == 'NPY':
        array = np.load('npy/FC1.npy')

    # Test
    print('==== original data ====')
    print(array)
    print('==== original data ====')
    hex_viewer = HexViewer(array)
    hex_viewer.show()


def test():

    # test mode
    # TEST_MODE = ['INT8', 'INT16', 'NPY']
    TEST_OPTIONS = [('INT8', 15, 15), 
                    ('INT8', 15, 300),
                    ('INT8', 300, 15),
                    ('INT8', 300, 300),
                    ('INT16', 15, 15),
                    ('INT16', 15, 300),
                    ('INT16', 300, 15),
                    ('INT16', 300, 300),
                    ]
    
    for test_option in TEST_OPTIONS:
        test_dtype, rows, columns = test_option

        _test(test_dtype, (rows, columns))


if __name__ == '__main__':

    test()

