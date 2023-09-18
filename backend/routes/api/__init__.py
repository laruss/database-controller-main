import pkgutil

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __import__(module_name, globals(), locals(), [], 1)
