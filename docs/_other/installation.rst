.. _installation:

############
Installation
############

There are several different ways that you can install ``MuFFiN``!

You can install ``MuFFiN`` using ``PIP``, or else directly from 
its source code, which is hosted on ``GitHub``.

Before you get started with installing ``MuFFiN`` though, we recommended that you 
get to grips with using a virtual environment. 

This will ensure that your installation does not interact with other Python packages that you've previously installed
in your default Python environment, 
and will help you keep track of your project. 

Creating and activating your virtual environment 
################################################

You can follow a more detailed tutorial on virtual environments `here <https://docs.python.org/3/tutorial/venv.html>`__.
But here is a brief summary.

Python applications will often use packages that don't come as part of the default library.
This means it will not be possible for one Python installation to meet the requirements of every application.

To solve this problem, the best thing to do is to create a virtual environment. 
This is just a self-contained directory tree that
contains an installation of a particular Python version, 
plus a number of necessary additional packages.

To create a virtual environment, start by deciding upon a directory where you want to place it, 
and, in your terminal, run Python's venv module: ::

   python -m venv <your-chosen-path>/env

This creates a virtual environment, in this case called ``env``.
The directories inside this mean that is really is a virtual environment 
(and not just a directory).  
These contain a copy of the Python interpreter that you used to create the 
virtual environment, as well as various other supporting files.

Once you have created your virtual environment, you may activate it by running: ::

   source <your-chosen-path>/bin/activate

You should see your command prompt is now appended with (env), which means 
your virtual environment is active!

Once activated, using Python will call the interpreter local  
to this environment (rather than your machine's default interpreter). 

To check that you are really using the local version of ``Python``, 
run: ::

   which python

This should return a location inside your virtual environment. 

You can now install packages into your virtual environment.
For example, you could install ``NumPy`` by running: ::

   python -m pip install numpy 


Don't worry if you no longer want to use your vritual environment, and want to use your 
defualt Python interpreter! 
You can deactivate the virtual environment at any time by simply running: ::

   deactivate env

Of course, there are many alternatives to venv for environment management. 
One example is `conda environments <https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment>`__.


Install MuFFiN from PIP
############################

``PIP`` is a package manager for Python packages, or modules if you like.

A package is just a directory that contains a collection of Python modules relevant to a particular task. 
For example, MuFFiN is a package that contains Python modules for simulating Multiscale Fluid Flow in Networks!

You can think of ``PIP`` as a shop for Python packages, and so you can download MuFFiN from ``PIP``.


With your virtual environment active (see above), in your terminal, run: ::

   python -m pip install MuFFiN

You can check that this has installed MuFFiN 
by running a python script (for example, ``test.py``) 
containing the code: ::

   import muffin


.. Install using ``conda`` 
.. #######################

.. Once you've installed Anaconda you can then install ``openpnm``. It is
.. available on `conda-forge <https://anaconda.org/conda-forge/openpnm>`__ 


..    conda install -c conda-forge MuFFiN

Installing MuFFiN from source code
##################################

Our source code is stored in a repository on GitHub.

We will publish new releases to ``PIP`` every so often, but we are updating the source code all the time. 
Therefore, if you want to use the latest features available (but not yet officially released), you have two options:

The easy way
------------
One way to get the latest features is to use your terminal to run: ::

   pip install git+https://github.com/ArkadyWey/MuFFiN.git@dev

This might not be the right solution for you though!

.. warning::
   This approach is not recommended if you plan to contribute to MuFFiN, or
   get new updates dynamically. 
   You will need to uninstall your current version of MuFFiN and then rerun this command everytime
   you want to check for updates.

The hard way
------------
A safer way to keep up to date dynamically, or contribute to MuFFiN (which we are happy to help with!), 
is to clone our GitHub repository and install it locally.

This sounds complicated, but it't not!

Open up a terminal and change directory to the directory where you want to clone ``MuFFiN``: ::

   cd <your-directory>

Now clone our repository by running: ::

   git clone https://github.com/arkadywey/MuFFiN

Next, change directory to the root folder of ``MuFFiN``::

   cd MuFFiN

You now need to install ``MuFFiN`` dependencies. 
These are just the packages that are used in ``MuFFiN``. 

Of course, you can install these using ``PIP`` (make sure you have your virtual environment active!) by running: ::

   python -m pip install -r requirements.txt

You're now ready to install ``MuFFiN``. 
You should do this in "editable" mode. 
To do this (with your virtual environment active), run: ::

   pip install -e .

This adds the directory ``MuFFiN`` as a Python package, which is what we wanted.

You now have a virtual environment set up, with ``MuFFiN`` installed, as well 
as all of its dependencies!

Because you installed the package as editable, you can update your local version to reflect our version at 
any time by changing directory to the root directory containing ``MuFFiN``, and 
running: :: 

   git pull


Scared of ``Git``? Don't be! There are loads of great resources online to help you to use ``Git`` for version control. 
GUIs (Graphical User Interfaces) like ``GitKraken`` or ``GitFork`` might make this easier.

.. warning::
   A word of caution. If you tried installing ``MuFFiN`` using ``PIP`` or using 'the easy way', 
   then you will need to uninstall it before you install the development version!
   
Luckily, un-installation is straightforward! This can be achieved by opening a terminal and running: ::
   
   python -m pip uninstall MuFFiN
