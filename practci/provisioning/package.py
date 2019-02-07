from enum import IntEnum, auto()

class InstallMode(IntEnum):
    USER = auto()
    SYSTEM = auto()


class PackageType(IntEnum):
    BASH = auto()
    REMOTE = auto() # remote script, this should be a set of flags

class package:

    def __init__(self, name, version, url):
        self._name = name

    def name(self):
        pass

    def version(self):
        pass

    def install(self, mode=InstallMode.USER):
        pass


class bash_package(package):
    def __init__(self):
        pass

class batch_package(package):
    def __init__(self):
        pass

class powershell_package(package):
    def __init__(self):
        pass

class executable_package(package):
    def __init__(self):
        pass
