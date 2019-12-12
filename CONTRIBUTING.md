

# Contributing

If you feel like contributing to this open-source project, this section contains some useful information to get started.
</br>
</br>
## Setting things up
There is some stuff you should get:

### Python 3.4
First of all, if you haven't noticed yet, it's a Python project, so you should get that! Most decent operating systems come shipped with it, but in case you don't have it installed on your system, go here [here](https://www.python.org/downloads/). Make sure that you have at least Python version 3.4.  

### Pip
Then you will have to get pip, check out this [link](https://pip.pypa.io/en/stable/installing/).

### Graphviz
You will need to install Graphviz on your system in order to render generated **dot** source code by the Python Graphviz library. Get it [here](https://pypi.org/project/graphviz/).

### Virtual environment
It's advisable to create a Python virtual environment for this open-source project, as you don't want other libraries to cause dependency issue in this project. Take a look at this [link](https://docs.python.org/3/library/venv.html#module-venv).
</br>
</br>

## Getting the source 
OK, so get the source of this project: Fork the repository and clone it to your system.
</br>
</br>
## Running the tests
Before you start, just make sure that the test cases work! 

### Activate your virtual environment
Go to your virtual environment directory and activate it:

* ```source \<venv\>/bin/activate``` (unix and mac) or
* ```\<venv\>\Scripts\activate``` (windows) 

### Run the tests
In the root of the *py-viz-algs* project, run the test cases:

 ```python setup.py test```

