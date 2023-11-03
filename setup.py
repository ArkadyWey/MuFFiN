from setuptools import setup

setup(name='MuFFiN',
      version='0.1.0',
      description='A package to simulate Multiscale Fluid Flow in Networks.',
      url='https://github.com/ArkadyWey/MuFFiN/',
      author='Arkady Wey',
      packages=['muffin'],
      install_requires = 
      ["numpy", 
       "matplotlib"],
      license='GPLv3')