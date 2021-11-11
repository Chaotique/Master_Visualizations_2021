"""
To make your code executable on any machine,
use relative paths instead of absolute paths
"""

import os

here = os.path.dirname(__file__)
print("here: ", here)
filename = os.path.join(here, "some_file.csv")
print("here: ", filename)


"""
Also,

* store all files necessary for execution in the git repository, so the code can really be run from other machines
* avoid using spaces or special characters in filenames. They make it harder to use them in programs on different operating systems
* instead, use _ (hello_world.py); python programs should only contain small letters by the norm https://www.python.org/dev/peps/pep-0008/
* NEVER use python library module names as filenames, e.g. plotly.py

"""
