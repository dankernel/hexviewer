
import os
import numpy as np
from termcolor import colored


class HexViewer:

    def __init__(self, input_array):
        
        terminal_rows, terminal_columns = map(int, os.popen('stty size', 'r').read().split())
        self.terminal_rows = terminal_rows
        self.terminal_columns = terminal_columns
        self.input_array = input_array

        self.is_ellipsis_rows = None
        self.is_ellipsis_columns = None

    def format_replication(self, msgs, hex_columns, hex_rows):

        # columns(X-axis) extend
        for i in range(len(msgs)):
            for j in range(hex_columns):
                if i == 0:
                    msgs[i] = msgs[i][:7] + ' dd' + msgs[i][7:]
                elif i == 1 or i == 3:
                    msgs[i] = msgs[i][:7] + '───' + msgs[i][7:]
                else:
                    msgs[i] = msgs[i][:7] + ' xx' + msgs[i][7:]

        # rows(Y-axis) extend
        for i in range(hex_rows):
            msgs.insert(2, msgs[2])

        return msgs

    def format_replace(self, msgs):

        for i in range(len(msgs)):
            # dddd -> {:4} 
            msgs[i] = msgs[i].replace('dddd', colored('{:4}', 'green'))

            # xx -> {:02X}
            # xx xx -> {:02X} {:02X}
            if self.input_array.dtype == np.int8 or self.input_array.dtype == np.uint8:
                temp = colored('{:02X} ', 'green') + colored('{:02X}', 'red')
                msgs[i] = msgs[i].replace('xx xx', temp)
            elif self.input_array.dtype == np.int16 or self.input_array.dtype == np.uint16:
                temp = colored('{:02X} {:02X} ', 'green') + colored('{:02X} {:02X}', 'red')
                msgs[i] = msgs[i].replace('xx xx xx xx', temp)

            # dd -> {:02}
            msgs[i] = msgs[i].replace('dd', '{:02}')

        return msgs

    def format_print(self, msgs, array, print_hex_columns, print_hex_rows):

        # print all
        ellipsis_line = -3
        for i in range(len(msgs)):
            if i == 0:
                # columns index
                temp = list(range(print_hex_columns + 1))
                temp.append(array.shape[1])
                print(msgs[i].format(*temp))
            elif i == len(msgs) - 1:
                # rows index
                print(msgs[i].format(array.shape[0]))
            else:
                # data
                if self.is_ellipsis_columns:
                    if len(msgs) + ellipsis_line - 1 == i:
                        # ellipsis line ('..')
                        msgs[i] = msgs[i].replace('{:02X}', '..')
                        temp.insert(0, i - 2) # index
                    elif len(msgs) + ellipsis_line - 2 < i:
                        # afterword (-n)
                        temp = list(array[i - print_hex_rows - 3]) # Hex datas
                        temp.insert(0, i - print_hex_rows - 3) # index
                    else:
                        # general data (+n)
                        temp = list(array[i-2]) # Hex datas
                        temp.insert(0, i - 2) # index
                else:
                    temp = list(array[i-2])
                    temp.insert(0, i - 2)

                print(msgs[i].format(*temp))


    def show(self):
        """
        Print HEX

        :param np.ndarray array: input array
        :return: None
        """
        array = self.input_array.view(dtype=np.uint8)

        print_hex_rows = min(array.shape[0] - 1, self.terminal_rows - 5)
        print_hex_columns = min(array.shape[1] - 1, (self.terminal_columns - 16) // 3)

        if self.input_array.dtype == np.int8 or self.input_array.dtype == np.uint8:
            # AA BB AA -> AA BB
            print_hex_columns -= (print_hex_columns + 1) % 2
        elif self.input_array.dtype == np.int16 or self.input_array.dtype == np.uint16:
            # AA AA BB BB AA AA -> AA AA BB BB 
            print_hex_columns -= (print_hex_columns + 1) % 4

        self.is_ellipsis_rows = array.shape[0] - 1 > self.terminal_rows - 5
        self.is_ellipsis_columns = array.shape[1] - 1 > (self.terminal_columns - 16) // 3

        if __debug__:
            print('print_hex_rows :', print_hex_rows)
            print('print_hex_columns :', print_hex_columns)
            print('is_ellipsis_rows :', self.is_ellipsis_rows)
            print('is_ellipsis_columns :', self.is_ellipsis_columns)

        msgs = []
        # ..........0.........1....
        # ..........01234567890123
        msgs.append('        dd dddd ') # 0
        msgs.append('      ┌────┐') # 1
        msgs.append('   dd │ xx │') # 2
        msgs.append(' dddd └────┘') # 3

        # Format Replication
        msgs = self.format_replication(msgs, print_hex_columns, print_hex_rows)

        # Format Replace
        msgs = self.format_replace(msgs)

        self.format_print(msgs, array, print_hex_columns, print_hex_rows)


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

    test()

