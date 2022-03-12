
# Python - installation

Integrated Development Environment IDE - software used to develop programs.

For most of the classes we will use:
* `Spyder` as a bit more advanced IDE
* `VSCode` or `Jupyter Lab` (its predecessor, `Jupyter Notebook` is also fine) for jupyter notebooks.

Please install `spyder` and `VSCode`/`jupyter`.

## with Anaconda

They can be installed as a part of all-in-one, heavy, enviroment known as [anaconda](https://www.anaconda.com/).

## or without anaconda

They can be installed separately:

* [spyder](https://www.spyder-ide.org/)  -->  [installation](https://docs.spyder-ide.org/current/installation.html)

* [jupyter](https://jupyter.org/index.html) --> [installation](https://jupyter.org/install)

`pip`, is a tool for installing Python packages.
Please install the commonly used libraries.

```.sh
$pip install -r requirements.txt
```

Where the content of the requirements file is:

```.txt
jupyterlab
ipywidgets
numpy
sympy
scipy
matplotlib
pandas
ipython
ipympl
```

Depending on the type of installation, the jupyter lab/notebook server can be run from anaconda enviroment or straight from the command line by typing:

```.sh
$jupyter-lab
```

### VSCode

Visual Studio Code us available at:

<https://code.visualstudio.com/>
<https://marketplace.visualstudio.com/items?itemName=ms-python.python>

### Nice to have

To separate enviroments between projects, the `virtualenv` is commonly used:
<https://virtualenvwrapper.readthedocs.io/>

An addon allowing to inspect variables in the jupyter lab:

<https://github.com/lckr/jupyterlab-variableInspector>
