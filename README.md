# MuFFiN

MuFFiN is an Open Source Python package for solving and analysing Multiscale Fluid Flow in Networks.

## Using MuFFiN

Solving your first model with ``MuFFiN`` is straightforward!

First, import the necessary subpackages from ``muffin``:

```python
    import muffin.parameters.parameters as parameters 
    import muffin.cells.cells as cells
    import muffin.equations_preprocess.equations_preprocess as equations_preprocess
    import muffin.equations_flow.equations_flow as equations_flow
    import muffin.models.models as models
```

Next, define the 'ingredients' of the model. 

The first 'ingredient' is the parameters:

```python
    parameters = parameters.Parameters()
```

The second 'ingredient' is the cell:

```python
    cell = cells.FourRegular(parameters=parameters)
```

The third 'ingredient' is the equations. We needs two sets of equations (see Model for details):

```python   
    equations_preprocess = equations_preprocess.Deposition(parameters=parameters)
    equations_flow = equations_flow.Base(parameters=parameters)
```

Next, we load these 'ingredients' into our model:

```python
    model = models.Model(parameters=parameters, 
                         cell=cell, 
                         equations_preprocess=equations_preprocess, 
                         equations_flow=equations_flow)
```

We can then solve this model in one line:

```
    model.solve()
```