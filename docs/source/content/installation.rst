Getting Started
================

Installation
------------

1. Install  `Python <https://www.python.org/>`_ version 3.10 or greater.

2. Install `conda <https://docs.conda.io/en/latest/miniconda.html>`_.

3. Install `git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_.

4. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/DSSGxMunich/dssgx_land_sealing_dataset_analysis

5. Create a conda environment from the environment.yml file:

   .. code-block:: bash

      conda create --name land-sealing-env


6. Activate the conda environment:

   .. code-block:: bash

      conda activate land-sealing-env

7. Install the requirements:

   .. code-block:: bash

      pip install -r requirements.txt




First Steps
------------

1. Download the `data.zip` from the `DSSGxMunich Huggingface <https://huggingface.co/DSSGxMunich>`_ .

1. a. Unzip the `data.zip` file. Place the `data` folder in the `repository root` folder.

1. b. A description of the data can be found in the Huggingface repository.

2. Run the exploratory data analysis notebooks, e.g. `explorer.ipynb`.

3. Run the execution pipeline notebooks, e.g. `src/1_execution_pipeline.ipynb`.


