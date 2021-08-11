#!/usr/bin/env python3

import os
import numpy as np
import sys

from termcolor import colored


class HexViewer:

    def __init__(self, input_array):
        """
        :param numpy.ndarray input_array: input array
        """
        
        terminal_rows, terminal_columns = map(int, os.popen('stty size', 'r').read().split())
        self.terminal_rows = terminal_rows
        self.terminal_columns = terminal_columns
        self.input_array = input_array

        self.hex_rows = min(input_array.shape[0] - 1, self.terminal_rows - 5)
        self.hex_columns = min(input_array.shape[1] - 1, (self.terminal_columns - 16) // 3)

        self.is_ellipsis_rows = None
        self.is_ellipsis_columns = None

    def format_replication(self, print_format_string):
        """
        Duplicate the default format to fit the size.

        :print_format_string list(str) print_format_string : format string
        """

        """
        columns(X-axis) extend.

               dd dddd            dd dd dddd
             ┌────┐             ┌───────┐
          dd │ xx │    ->    dd │ xx xx │
        dddd └────┘        dddd └───────┘
        """
        for i in range(len(print_format_string)):
            for j in range(self.hex_columns):
                if i == 0:
                    print_format_string[i] = print_format_string[i][:7] + ' dd' + print_format_string[i][7:]
                elif i == 1 or i == 3:
                    print_format_string[i] = print_format_string[i][:7] + '───' + print_format_string[i][7:]
                else:
                    print_format_string[i] = print_format_string[i][:7] + ' xx' + print_format_string[i][7:]

        """
        rows(Y-axis) extend.

               dd dddd            dd dddd
             ┌────┐             ┌────┐
          dd │ xx │    ->    dd │ xx │
        dddd └────┘    ->    dd │ xx │
                           dddd └────┘
        """
        for i in range(self.hex_rows):
            print_format_string.insert(2, print_format_string[2])

        return print_format_string

    def format_replace(self, print_format_string):
        """
        Custom format to Python standard format.

        :print_format_string list(str) print_format_string : custom format string
        :return: standard format string
        """

        for i in range(len(print_format_string)):
            # dddd -> {:4} 
            print_format_string[i] = print_format_string[i].replace('dddd', colored('{:4}', 'green'))

            if self.input_array.dtype == np.int8 or self.input_array.dtype == np.uint8:
                # xx xx -> {:02X} {:02X}
                temp = colored('{:02X} ', 'green') + colored('{:02X}', 'red')
                print_format_string[i] = print_format_string[i].replace('xx xx', temp)
            elif self.input_array.dtype == np.int16 or self.input_array.dtype == np.uint16:
                # xx xx xx xx -> {:02X} {:02X} {:02X} {:02X}
                temp = colored('{:02X} {:02X} ', 'green') + colored('{:02X} {:02X}', 'red')
                print_format_string[i] = print_format_string[i].replace('xx xx xx xx', temp)

            # dd -> {:02}
            print_format_string[i] = print_format_string[i].replace('dd', '{:02}')

        return print_format_string

    def format_print(self, print_format_string, array):
        """
        Print the array to fit the format.

        :print_format_string list(str) print_format_string : format string
        :param numpy.ndarray input_array: input array
        """

        # print all
        ellipsis_line = -3
        for i in range(len(print_format_string)):
            if i == 0:
                # columns index
                temp = list(range(self.hex_columns + 1))
                temp.append(array.shape[1])
                print(print_format_string[i].format(*temp))
            elif i == len(print_format_string) - 1:
                # rows index
                print(print_format_string[i].format(array.shape[0]))
            else:
                # data
                if self.is_ellipsis_rows:
                    if len(print_format_string) + ellipsis_line - 1 == i:
                        # ellipsis line ('..')
                        print_format_string[i] = print_format_string[i].replace('{:02X}', '..')
                        temp.insert(0, i - 2) # index
                    elif len(print_format_string) + ellipsis_line - 2 < i:
                        # afterword (-n)
                        temp = list(array[i - self.hex_rows - 3]) # Hex datas
                        temp.insert(0, i - self.hex_rows - 3) # index
                    else:
                        # general data (+n)
                        temp = list(array[i-2]) # Hex datas
                        temp.insert(0, i - 2) # index
                else:
                    temp = list(array[i-2])
                    temp.insert(0, i - 2)

                print(print_format_string[i].format(*temp))

    def show(self):
        """
        Print HEX
        """
        array = self.input_array.view(dtype=np.uint8)

        if self.input_array.dtype == np.int8 or self.input_array.dtype == np.uint8:
            # AA BB AA -> AA BB
            self.hex_columns -= (self.hex_columns + 1) % 2
        elif self.input_array.dtype == np.int16 or self.input_array.dtype == np.uint16:
            # AA AA BB BB AA AA -> AA AA BB BB 
            self.hex_columns -= (self.hex_columns + 1) % 4

        self.is_ellipsis_rows = array.shape[0] - 1 > self.terminal_rows - 5
        self.is_ellipsis_columns = array.shape[1] - 1 > (self.terminal_columns - 16) // 3

        if __debug__:
            print('hex_rows :', self.hex_rows)
            print('hex_columns :', self.hex_columns)
            print('is_ellipsis_rows :', self.is_ellipsis_rows)
            print('is_ellipsis_columns :', self.is_ellipsis_columns)

        print_format_string = []
        # ..........0.........1....
        # ..........01234567890123
        print_format_string.append('        dd dddd ') # 0
        print_format_string.append('      ┌────┐')     # 1
        print_format_string.append('   dd │ xx │')     # 2
        print_format_string.append(' dddd └────┘')     # 3

        # Format Replication
        print_format_string = self.format_replication(print_format_string)

        # Format Replace
        print_format_string = self.format_replace(print_format_string)

        # Print format
        self.format_print(print_format_string, array)

def test():

    # test mode
    TEST_MODE = 'NPY' # INT8 / INT16 / NPY
    
    # Init or Load
    if TEST_MODE == 'INT8':
        array = np.random.randint(0xFF, size=(500, 3000), dtype=np.uint8)
    elif TEST_MODE == 'INT16':
        array = np.random.randint(0xFFFF, size=(500, 3000), dtype=np.uint16)
    elif TEST_MODE == 'NPY':
        array = np.load('bin/FC1.npy')

    # Test
    print(array)
    hex_viewer = HexViewer(array)
    hex_viewer.show()
    pass

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('input npy file')
        sys.exit(-1)

    path = sys.argv[1]
    if os.path.isfile(path):

        if os.path.splitext(path)[-1].lower() != '.npy':
            print('input npy file')
            exit(-1)

        array = np.load(path)
        hex_viewer = HexViewer(array)
        hex_viewer.show()

    exit()

