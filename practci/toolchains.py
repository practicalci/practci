import io
import os
import subprocess
import sys

from typing import List


def has_fileno(obj):
    if not hasattr(obj, 'fileno'):
        return False

    # check BytesIO case and maybe others
    try:
        obj.fileno()
    except (AttributeError, IOError, io.UnsupportedOperation):
        return False

    return True


class ToolChainExecFail(Exception):
    pass


class ToolChain:
    def __init__(self, name, project_root_dir):
        """
        Creates a toolchain, with the given name.

        @param name: the name of the toolchain, the toolchain name is composed of
        '<channel_name>/<wrapper_script_name>'.
        """
        self._name = name

        name_components = self._name.split('/')

        self._channel = name_components[0]
        self._wrapper_script_name = name_components[1]

        self._wrapper_script_path = os.path.join('.practci', 'bin', 'toolchains',
                                                 self._channel, sys.platform,
                                                 self._wrapper_script_name)

        self._project_root_dir = project_root_dir
        self._wrapper_script_abs_path = os.path.join(self._project_root_dir, self._wrapper_script_path)

    def get_name(self) -> str:
        return self._name

    def get_channel(self) -> str:
        return self._channel

    def get_wrapper_script_name(self) -> str:
        return self._wrapper_script_name

    def get_wrapper_script_path(self) -> str:
        return self._wrapper_script_path

    def get_wrapper_script_abs_path(self, project_root_dir: str) -> str:
        return os.path.join(project_root_dir, self.get_wrapper_script_path())

    def is_installed(self):
        return os.path.exists(self._wrapper_script_abs_path) and os.path.isfile(self._wrapper_script_abs_path)

    def exec_command(self, command: List[str], project_root_dir: str, cwd: str = None, stdout: io.TextIOBase = None,
                     stderr: io.TextIOBase = None) -> None:
        """
        Executes a command under the toolchain environment.

        @param command:
        @param project_root_dir:
        @param stdout:
        @param stderr:
        """

        # TODO: consider reading the output gradually as described here https://stackoverflow.com/a/923127
        toolchain_command = [self.get_wrapper_script_abs_path(project_root_dir)]
        toolchain_command += command

        # due to io.UnsupportedOperation: fileno, use this https://stackoverflow.com/a/15374306

        command_stdout = subprocess.PIPE
        command_stderr = subprocess.PIPE

        if stdout:
            if has_fileno(stdout):
                command_stdout = stdout
        elif has_fileno(sys.stdout):
            command_stdout = sys.stdout
        else:
            stdout = sys.stdout

        if stderr:
            if has_fileno(stderr):
                command_stderr = stderr
        elif has_fileno(sys.stderr):
            command_stderr = sys.stderr
        else:
            stderr = sys.stderr

        subprocess.check_output("echo hi", shell=True, universal_newlines=True)

        # TODO: no timeouts, check a solution https://docs.python.org/3/library/subprocess.html#subprocess.Popen.communicate
        # stdout_data, stderr_data = subprocess.Popen(toolchain_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                                             cwd=cwd).communicate()

        # TODO: capture the return types of failured builds to propagate the error core of the tool
        subprocess_call = subprocess.run(toolchain_command, stdout=command_stdout, stderr=command_stderr,
                                         cwd=cwd, encoding='utf-8')

        if stdout and not has_fileno(stdout):
            stdout.write(subprocess_call.stdout)

        if stderr and not has_fileno(stderr):
            stderr.write(subprocess_call.stderr)

        if subprocess_call.returncode != 0:
            raise ToolChainExecFail('execution of toolchain: {} and command: {} failed'
                                    .format(self._name, ' '.join(command)))


def get_tool_chain(name, project_root_dir='.'):
    return ToolChain(name=name, project_root_dir=project_root_dir)
