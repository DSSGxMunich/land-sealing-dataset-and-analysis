Getting Started
================

Installation
------------

1. Install  `Python <https://www.python.org/>`_ version 3.9 or greater.

2. Install `conda <https://docs.conda.io/en/latest/miniconda.html>`_.

3. Install `git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_.

4. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/DSSGxMunich/dssgx_land_sealing_dataset_analysis

5. Create a conda environment from the environment.yml file:

   .. code-block:: bash

      conda create --name land-sealing-env --file environment.yml


6. Activate the conda environment:

   .. code-block:: bash

      conda activate land-sealing-env



First Steps
------------

1. Download the data from the `DSSGxMunich Cloud Storage <fakelink.com>`_ and place it in the `data` folder.

2. Run the exploratory data analysis notebooks in the `src` folder, e.g. `src/explorer.ipynb`.