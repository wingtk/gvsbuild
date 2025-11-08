import importlib
import pkgutil

for module_info in pkgutil.iter_modules(__path__):
    importlib.import_module(f"{__name__}.{module_info.name}")
