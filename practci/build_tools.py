import logging
import os
import shutil

from abc import ABCMeta, abstractmethod
from enum import IntEnum, auto

from .toolchains import ToolChain

logger = logging.getLogger(__name__)


class BuildToolType(IntEnum):
    CMAKE = auto()
    CONDA = auto()
    CONAN = auto()
    SCONS = auto()
    MAKE = auto()
    PYTHON_SETUP = auto()
    UNKNOWN = auto()


class BuildType(IntEnum):
    RELEASE = auto()
    DEBUG = auto()
    PROFILER = auto()



class BuildTarget(IntEnum):
    """



    """
    SETUP_BUILD = auto()  # initialize build directories and files and configurations
    PURGE = auto()  # deletes directories created by the build tool, such as install, build, other ...
    COMPILE = auto() #
    INSTALL = auto()
    TEST = auto()
    STATIC_CHECKS = auto()
    RUNTIME_CHECKS = auto()
    CLEAN = auto() # clean files from build
    COMMIT = auto()
    PUBLISH = auto()
    MERGE_UPSTREAM = auto()
    NONE = auto()
    UNKNOWN = auto()


class BuildTool(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def setup(self, project_root_dir: str, toolchain: ToolChain, build_type: BuildType = BuildType.DEBUG):
        pass

    @abstractmethod
    def install(self, project_root_dir: str, toolchain: ToolChain):
        pass

    @abstractmethod
    def purge(self, project_root_dir: str, toolchain: ToolChain):
        pass

    @abstractmethod
    def purge_all(self, project_root_dir: str):
        pass

class NoneBuildTool(BuildTool):
    """
    Class that does nothing, this is the "null" build tool.
    """

    def __init__(self):
        pass

    def setup(self, project_root_dir: str, toolchain: ToolChain, build_type: BuildType = BuildType.DEBUG):
        logger.warning('setup build is taking place with a dummy build tool, that will result in nothing.')

    def install(self, project_root_dir: str, toolchain: ToolChain):
        logger.warning('install is taking place with a dummy build tool, that will result in nothing.')

    def purge(self, project_root_dir: str, toolchain: ToolChain):
        logger.warning('purge is taking place with a dummy build tool, that will result in nothing.')

    def purge_all(self, project_root_dir: str):
        pass


class CMakeBuildTool(BuildTool):
    def __init__(self):
        pass

    @staticmethod
    def _get_toolchain_install_dir(project_root_dir, toolchain: ToolChain):
        return os.path.join(project_root_dir, 'install', toolchain.get_name())

    @staticmethod
    def _get_toolchain_build_dir(project_root_dir, toolchain: ToolChain):
        return os.path.join(project_root_dir, 'build', toolchain.get_name())

    @staticmethod
    def _get_install_dir(project_root_dir):
        return os.path.join(project_root_dir, 'install')

    @staticmethod
    def _get_build_dir(project_root_dir):
        return os.path.join(project_root_dir, 'build')

    def setup(self, project_root_dir: str, toolchain: ToolChain, build_type: BuildType = BuildType.DEBUG):

        build_dir = self._get_toolchain_build_dir(project_root_dir=project_root_dir, toolchain=toolchain)
        install_dir = self._get_toolchain_install_dir(project_root_dir=project_root_dir, toolchain=toolchain)

        os.makedirs(build_dir, exist_ok=True)
        os.makedirs(install_dir, exist_ok=True)

        cmake_install_prefix = '-DCMAKE_INSTALL_PREFIX={}'.format(install_dir)

        rel_project_dir = os.path.relpath(project_root_dir, build_dir)

        command = ['cmake', '-LAH', cmake_install_prefix, rel_project_dir]

        toolchain.exec_command(command, project_root_dir=project_root_dir, cwd=build_dir)

    def install(self, project_root_dir: str, toolchain: ToolChain):
        command = ['cmake', '--build', '.', '--target', 'install']

        build_dir = self._get_toolchain_build_dir(project_root_dir=project_root_dir, toolchain=toolchain)

        toolchain.exec_command(command, project_root_dir=project_root_dir, cwd=build_dir)

    def purge(self, project_root_dir: str, toolchain: ToolChain = None):
        build_dir = self._get_toolchain_build_dir(project_root_dir=project_root_dir, toolchain=toolchain)
        install_dir = self._get_toolchain_install_dir(project_root_dir=project_root_dir, toolchain=toolchain)
        shutil.rmtree(build_dir)
        shutil.rmtree(install_dir)

    def purge_all(self, project_root_dir: str):
        build_dir = self._get_build_dir(project_root_dir=project_root_dir)
        install_dir = self._get_install_dir(project_root_dir=project_root_dir)
        shutil.rmtree(build_dir)
        shutil.rmtree(install_dir)


build_tools = {
    BuildToolType.CMAKE: CMakeBuildTool()
}


def get_build_tool(build_tool_type: BuildToolType) -> BuildTool:
    return build_tools.get(build_tool_type, NoneBuildTool())
