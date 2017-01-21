from distutils.cmd import Command
from distutils.command.install_lib import install_lib
import os
import subprocess
import sys

from rustypy.module import RustyModule


class RustCommand(Command):

    description = "rust build command"
    user_options = [
        ('modules=', None, 'list of rust modules'),
        ('release=', None, 'boolean for --release flag')
    ]

    def initialize_options(self) -> None:
        self.modules = []
        self.release = True
        self.build_temp = None

    def finalize_options(self) -> None:
        self.set_undefined_options(
            'build',
            ('build_temp', 'build_temp'),
        )

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
            module.lib_name
        )
        build_ext = self.get_finalized_command('build_ext')
        ext_fullpath = build_ext.get_ext_fullpath(module.name)
        self.mkpath(os.path.dirname(ext_fullpath))
        self.copy_file(lib_path, ext_fullpath)

    def run(self) -> None:
        for module in self.modules:
            self.compile(module)
        for module in self.modules:
            self.deploy(module)


build_rust = RustCommand


class install_with_rust(install_lib):
    def build(self) -> None:
        install_lib.build(self)
        self.run_command('build_rust')
