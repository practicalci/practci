import logging
import os

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
    SETUP_BUILD = auto()
    COMPILE = auto()
    INSTALL = auto()
    TEST = auto()
    STATIC_CHECKS = auto()
    RUNTIME_CHECKS = auto()
    CLEAN = auto()
    COMMIT = auto()
    PUBLISH = auto()
    MERGE_UPSTREAM = auto()
    NONE = auto()
    UNKNOWN = auto()


class BuildTool(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def build(self, project_root_dir: str, target: BuildTarget = BuildTarget.SETUP_BUILD,
              build_type: BuildType = BuildType.DEBUG,
              toolchain: ToolChain = None, checkchain: BuildTarget = None):
        pass


class NoneBuildTool(BuildTool):
    """
    Class that does nothing, this is the "null" build tool.
    """

    def __init__(self):
        pass

    def build(self, project_root_dir: str, target: BuildTarget = BuildTarget.SETUP_BUILD,
              build_type: BuildType = BuildType.DEBUG,
              toolchain: ToolChain = None, checkchain: BuildTarget = None):

        logger.warning('build is taking place with a dummy build tool, that will result in nothing.')


class CMakeBuildTool(BuildTool):
    def __init__(self):
        self._generator = '\"Unix Makefiles\"'

    def build(self, project_root_dir: str, target: BuildTarget = BuildTarget.SETUP_BUILD,
              build_type: BuildType = BuildType.DEBUG,
              toolchain: ToolChain = None, checkchain: BuildTarget = None):

        build_dir = os.path.join(project_root_dir, 'build')

        os.makedirs(build_dir, exist_ok=True)

        # command = ['cmake', '-G', self._generator, '..']
        command = ['cmake', '-LAH', '..']

        toolchain.exec_command(command, project_root_dir=project_root_dir, cwd=build_dir)


build_tools = {
    BuildToolType.CMAKE: CMakeBuildTool()
}


def get_build_tool(build_tool_type: BuildToolType) -> BuildTool:
    return build_tools.get(build_tool_type, NoneBuildTool())
