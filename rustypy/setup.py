import os
from setuptools import Command
from setuptools.command.develop import develop
from setuptools.command.install_lib import install_lib
import subprocess
import sys
from typing import List, Optional

from rustypy.module import RustyModule


class RustCommand(Command):

    description = "build rust extension"
    user_options = [
        ('modules=', None, 'list of rust modules'),
        ('release=', None, 'boolean for --release flag')
    ]

    def initialize_options(self) -> None:
        self.modules: Optional[List[RustyModule]] = None
        self.release = True

    def finalize_options(self) -> None:
        pass

    def run(self) -> None:
        if self.modules is None:
            return
        for module in self.modules:
            self.compile(module)
        for module in self.modules:
            self.deploy(module)

    def compile(self, module: RustyModule) -> None:
        args = ['Cargo', 'build']
        if self.release is True:
            args.append('--release')
        args.extend([
            '--manifest-path',
            '{}'.format(os.path.join(module.path, 'Cargo.toml')),
            '--color',
            'always',
        ])
        print((
            "[rustypy] Compiling rust extension module '{}'"
            .format(module.name))
        )
        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',
        )
        for line in iter(process.stderr.readline, ''):
            sys.stderr.write(line)
            sys.stderr.flush()
        process.wait()
        if process.returncode != 0:
            raise Exception(
                "Failed to compile '{}' module".format(module.name)
            )

    def deploy(self, module: RustyModule) -> None:
        mode = 'release' if self.release else 'debug'
        lib_path = os.path.join(
            module.path,
            'target',
            mode,
            module._lib_name
        )
        build_ext = self.get_finalized_command('build_ext')
        ext_fullpath = build_ext.get_ext_fullpath(module.name)
        self.mkpath(os.path.dirname(ext_fullpath))
        self.copy_file(lib_path, ext_fullpath)

build_rust = RustCommand


class develop_with_rust(develop):
    def run(self) -> None:
        super().run()
        self.run_command('build_rust')


class install_lib_with_rust(install_lib):
    def build(self) -> None:
        install_lib.build(self)
        self.run_command('build_rust')
