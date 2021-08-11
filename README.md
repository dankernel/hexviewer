
# hexviewer
This utility prints a pretty `numpy.ndarray`.

Useful for work with HEX (image processing, embedded programming, etc.).

![image](./res/uint8_15_15.png)

# Install

```
# install via pypi
$ pip3 install hexviewer

# install via pypi (-m pip)
$ python3 -m pip install hexviewer

# manual installation
$ git clone https://github.com/dankernel/hexviewer
$ python3 setup.py install

```

# How to use
```
$ hexviewer data/data.npy
```

The output is as follows:

![image](./res/uint16_300_30.png)

# Supported file formats

| format | support |
|--------|---------|
| INT8   | ✔️       |
| UINT8  | ✔️       |
| UINT16 | ✔️       |
| INT16  | ✔️       |
| UINT32 | ✖️       |
| INT32  | ✖️       |



