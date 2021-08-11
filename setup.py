import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hexviewer", # Replace with your own username
    version="0.1.0",
    author="dankernel",
    author_email="dkdkernel@gmail.com",
    description="hexviewer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dankernel/hexviewer",
    packages=setuptools.find_packages(),
    install_requires = ['python-telegram-bot'],
    scripts=['hexviewer/hexviewer', 'hexviewer/hexviewer.py'],
    package_data = {'': ['hexviewer/config.ini']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
