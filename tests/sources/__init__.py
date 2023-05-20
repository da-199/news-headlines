import sys
import os
# append the path of the
# parent directory
module_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(os.path.dirname(module_path))
sys.path.append(root_path)
sys.path.append(os.path.join(root_path, 'sources'))