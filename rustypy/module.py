import sys


class RustyModule:

    def __init__(self, name: str, path: str) -> None:
        self.name = name
        self.path = path

    @property
    def lib_name(self) -> None:
        prefix = {'win32': ''}.get(sys.platform, 'lib')
        extension = (
            {'darwin': '.dylib', 'win32': '.dll'}
            .get(sys.platform, '.so')
        )
        return prefix + self.name + extension
