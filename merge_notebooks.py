""" Code to merge a set of notebooks to form a full calcultion pack """

import nbformat as nbf

# Get the notebooks that will form the pack
main = nbf.read('main_calculation.ipynb')
other  = nbf.read('timber_connections.ipynb', 4)

# set the pack meta data and merge the cells
pack = nbf.v4.new_notebook(metadata=main.metadata)
pack.cells = main.cells + other.cells 

# set the pack name and write back the combined book.
nbf.write(pack, 'main_calculations.ipynb', 4)
