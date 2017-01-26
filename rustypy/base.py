import cffi

from rustypy.module import RustyModule


class RustyBase():

    def __init__(self, rusty_module: RustyModule) -> None:
        self.module = rusty_module
        self.ffi = cffi.FFI()
        self.ffi.cdef(self.module._header_str)
        self.lib = self.ffi.dlopen(self.module._lib_path)
