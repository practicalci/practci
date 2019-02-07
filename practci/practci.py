# -*- coding: utf-8 -*-

"""Main module."""

import os
import stat
import subprocess

from enum import IntEnum, auto

from .build_tools import BuildToolType, BuildType, BuildTarget

import practci.toolchains as toolchains
import practci.build_tools as build_tools


class EnvironmentType(IntEnum):
    SINGLE_DOCKER = auto()
    MULTI_DOCKER = auto()
    NATIVE = auto()


def cmake_setup_build(build_type, build_dir):
    # type: (BuildType, str) -> None
    """
    Returns a list of parameters for the cmake command.
    @param build_type one of the values from BuildType.
    @param build_dir the directory where the build is performed
    """

    # TODO: missing profiler build type, dunno how to do that yet with cmake
    cmake_build_type = \
        {BuildType.DEBUG: '-DDCMAKE_BUILD_TYPE=Debug',
         BuildType.RELEASE: '-DCMAKE_BUILD_TYPE=Release'}

    command = ['cmake', '-G', 'Ninja']

    cmake_build_params = cmake_build_type.get(build_type, BuildTarget.UNKNOWN)
    command += cmake_build_params
    command += '..'

    subprocess.run(command, cwd=build_dir)


def build_target_none():
    # type: () -> None
    """
    Dummy target, does nothing
    """
    pass


def cmake_build(target=BuildTarget.NONE, build_dir_prefix="./", build_dir_name="", environment=EnvironmentType.NATIVE,
                toolchain=None, build_type=BuildType.DEBUG):
    build_dir = os.path.join(build_dir_prefix, build_dir_name)

    # create build dir if it does not exists.
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    # example to expand variables, using jinja https://realpython.com/primer-on-jinja-templating/#quick-examples

    targets = {
        BuildTarget.SETUP_BUILD: cmake_setup_build,
        BuildTarget.NONE: build_target_none
    }

    targets.get(target)()  # execute the proper target


def install_build_environments(dockerimages, output_dir):
    """
    Execute the images, and each of these docker images will generate a script to be executed.
    Check dockcross tutorial in https://github.com/dockcross/dockcross/blob/master/README.rst .

    @param dockerimages list of docker images for build environments to generate an installer script.
    @param output_dir directory to output the scripts.
    """
    for docker_image in dockerimages:
        docker_script_name = os.path.join(output_dir, docker_image.replace('/', '-'))
        with open(docker_script_name, "w+") as docker_script:
            subprocess.run(['docker', 'run', '--rm', docker_image], stdout=docker_script)

        # add exec permissions to the script
        output_script_stat = os.stat(docker_script_name)
        os.chmod(docker_script_name, output_script_stat.st_mode | stat.S_IEXEC)


class PractCIConfig:
    """
    Configuration class, used to load and save settings and to pass parameters to the tool class.
    """

    def __init__(self, config_file=None, environment_type=EnvironmentType.NATIVE, default_provisioning_dir=None,
                 user_provisioning_dir=None,
                 docker_images=None, work_dir=None, bin_dir=None):
        self.config_file = config_file
        self.environment_type = environment_type
        self.default_provisioning_dir = default_provisioning_dir
        self.user_provisioning_dir = user_provisioning_dir
        self.docker_images = docker_images
        self.work_dir = work_dir
        self.bin_dir = bin_dir

        self._project_root_path = None

        if self.config_file:
            self.load_config(self.config_file)

    def load_config(self, config_file=None):
        """
        Sets the config_file property and loads the configuration from the file.

        @param config_file the file to load the configuration from.
        """
        self.config_file = config_file

    def save_config(self, config_file=None):
        """
        Saves the configuration to a file
        """
        pass

    def get_project_root_dir(self):
        if self._project_root_path is None:
            self._project_root_path = os.path.dirname(self.config_file)

        return self._project_root_path


class PractCI:

    def __init__(self, config: PractCIConfig):
        self.config = config

    def setup(self, tool_type=BuildToolType.CMAKE, toolchain_name='native/identity', build_type=BuildType.DEBUG):
        project_root_dir = self.config.get_project_root_dir()
        toolchain = toolchains.get_tool_chain(toolchain_name, project_root_dir)
        build_tool = build_tools.get_build_tool(tool_type)
        build_tool.setup(project_root_dir, toolchain, build_type)

    def install_platform_dependencies(self):
        """Run platform specific scripts to install required operating system requirements for the PractCI tool.
        An example of such dependencies, are docker, and miniconda.
        Note, when installing platform dependencies, the script must execute with administrative permissions."""

        # https://bugs.python.org/issue1322#msg263896
        # platform.dist() will be deprecated, and it is not reliable
        # https://pypi.org/project/distro/

    def install_project_environment(self):
        pass

    def install_conda_dependencies(self):
        pass

    def install_conda_dev_dependencies(self):
        pass

    def install_conda_build_dependencies(self):
        pass

    def install_images(self):
        """
        Install dockcross and alike images, to be used in build environments.
        """
        install_build_environments(self.config.docker_images, self.config.bin_dir)

    def build_all(self):
        """
        Build all target environments, using cmake or python setup.py or tox or conda build.
        """

    def setup_build_environment(self):
        """ sets up the build environment """

    def render_directory_project_structure(self):
        pass
