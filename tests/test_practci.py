#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `practci` package."""

import os
import shutil
import unittest

from click.testing import CliRunner


from practci.practci import PractCIConfig, PractCI, BuildTarget, BuildType, BuildToolType
from practci import cli

from tests.project_templates import cmake as cmake_template


class TestPractci(unittest.TestCase):
    """Tests for `practci` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.cli)
        self.assertEqual(result.exit_code, 0)
        self.assertIn('--version', result.output)
        self.assertIn('--help', result.output)

        help_result = runner.invoke(cli.cli, ['--help'])
        self.assertEqual(help_result.exit_code, 0)
        self.assertIn('--help     Show this message and exit.', help_result.output)

        help_result = runner.invoke(cli.cli, ['--help', '--version'])
        print(help_result.output)

    def test_config(self):
        """Test something."""
        runner = CliRunner()
        config_result = runner.invoke(cli.cli, ['config', '--show'])
        #self.assertEqual(config_result.exit_code, 0)
        #print(config_result.output)


    # def test_install(self):
        # docker_images_names = ['linux-s390x', 'android-arm', 'android-arm64',
        #                  'linux-x86', 'linux-x64', 'linux-arm64', 'linux-armv5',
        #                  'linux-armv6', 'linux-armv7', 'linux-mips', 'linux-mipsel',
        #                  'linux-ppc64le', 'windows-x86', 'windows-x64', 'windows-x64-posix']
        #
        # docker_images_names = ['linux-x64']
        #
        # docker_images = ['dockcross/' + image_name for image_name in docker_images_names]
        #
        # output_dir = './'
        #
        # practci.install_build_environments(docker_images, output_dir)

    def test_load_config(self):
        config = PractCIConfig()

        template_project_root_dir = os.path.dirname(cmake_template.__file__)
        config_file = os.path.join(template_project_root_dir, '.practci.cfg')

        config.load_config(config_file=config_file)
        self.assertEqual(template_project_root_dir, config.get_project_root_dir())

    def test_constructor_load_config(self):

        template_project_root_dir = os.path.dirname(cmake_template.__file__)
        config_file = os.path.join(template_project_root_dir, '.practci.cfg')

        config = PractCIConfig(config_file=config_file)
        self.assertEqual(template_project_root_dir, config.get_project_root_dir())


    def test_build_setup(self):
        project_root_dir = os.path.dirname(cmake_template.__file__)

        config_file = os.path.join(project_root_dir, '.practci.cfg')

        config = PractCIConfig(config_file=config_file)

        practci = PractCI(config)

        practci.setup(tool_type=BuildToolType.CMAKE, toolchain_name='native/identity', build_type=BuildType.DEBUG)

        build_dir = os.path.join(project_root_dir, 'build')
        install_dir = os.path.join(project_root_dir, 'install')

        self.assertTrue(os.path.exists(build_dir))
        self.assertTrue(os.path.isdir(build_dir))

        self.assertTrue(os.path.exists(install_dir))
        self.assertTrue(os.path.isdir(install_dir))

        shutil.rmtree(build_dir)
        shutil.rmtree(install_dir)






