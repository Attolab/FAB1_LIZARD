import os,fnmatch
import importlib
path=os.path.abspath(__file__)
(path,tail)=os.path.split(path)

files=list();
for file in os.listdir(path):
    if fnmatch.fnmatch(file, "*.py"):
        files.append(file)
        
if '__init__.py' in files:
    files.remove('__init__.py')

__all__=[file[:-3] for file in files]
for mod in __all__:
    try:
        importlib.import_module('.' + mod, 'pymodaq_plugins.daq_viewer_plugins.plugins_2D')
    except Exception as e:
        print("{:} plugin couldn't be loaded due to some missing packages or errors: {:}".format(mod,str(e)))
        pass
#from PyMoDAQ.plugins.DAQ_Viewer_plugins.plugins_2D import *