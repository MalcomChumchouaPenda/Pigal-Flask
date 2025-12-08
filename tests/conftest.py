
import os
import sys

root_dir = os.path.dirname(__file__)
while 'tests' in root_dir:
    root_dir = os.path.dirname(root_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)

