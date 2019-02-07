=====================
Practical CI workflow
=====================


.. image:: https://img.shields.io/pypi/v/practci.svg
        :target: https://pypi.python.org/pypi/practci

.. image:: https://img.shields.io/travis/mjscosta/practci.svg
        :target: https://travis-ci.org/mjscosta/practci

.. image:: https://readthedocs.org/projects/practci/badge/?version=latest
        :target: https://practci.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Command line tool to support TDD development workflow.


* Free software: BSD license
* Documentation: https://practci.readthedocs.io.


Features
--------

* TODO

Project Folder Structure
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

    <project_dir>
                 + condaenv_dev.yaml
                 + condaenv_build.yaml
                 +
                 + .practci.cfg # configuration
                 + .practci
                           + bin
                                + dockcross
                                           + linux-64 ?
                                           + linux-native-gcc5
                                           + windows-native-vc14
                                + dockcheck
                                           + linux-64 ?
                                           + linux-native-clang-4.8
                                           + windows-native-??
                           + provision
                                      + conda
                                      + linux
                                      |      + all
                                      |      + debian
                                      |      + ubuntu
                                      + windows
                                               + all
                                               + 10
                                               + 7



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

References
----------

https://cmake.org/cmake/help/v3.12/variable/MSVC_VERSION.html
