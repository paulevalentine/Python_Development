""" Code to merge a set of notebooks to form a full calcultion pack """

import nbformat as nbf

# Get the notebooks that will form the pack
snow = nbf.read('snow_loading.ipynb', 4)
loading = nbf.read('beams.ipynb', 4)

# set the pack meta data and merge the cells
pack = nbf.v4.new_notebook(metadata=snow.metadata)
pack.cells = snow.cells + loading.cells

# set the pack name and write back the combined book.
nbf.write(pack, 'pack.ipynb')