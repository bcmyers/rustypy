import os
import site
import sys
from typing import Optional


class RustyModule:

    def __init__(self, name: str, path: Optional[str] = None) -> None:
        self.name = name
        self.path = path

    @property
    def _header_str(self) -> str:
        header_path = os.path.join(
            self._venv_dir,
            self.name,
            self.name + '.h'
        )
        with open(header_path, 'r') as f:
            header_str = f.read()
        return header_str

    @property
    def _lib_name(self) -> str:
        prefix = {'win32': ''}.get(sys.platform, 'lib')
        extension = (
            {'darwin': '.dylib', 'win32': '.dll'}
            .get(sys.platform, '.so')
        )
        return prefix + self.name + extension

    @property
    def _lib_path(self) -> str:
        return os.path.join(
            self._venv_dir,
            self.name,
            self._lib_name,
        )

    @property
    def _venv_dir(self) -> str:
        site_path = site.getsitepackages()[0]
        return os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    site_path
                )
            )
        )
