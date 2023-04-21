import hashlib

class Md5Digest:
    def __init__(self, buf=b""):
        self.md5 = hashlib.md5()
        self._size = 0
        self.update(buf)

    def update(self, buf: bytes):
        self.md5.update(buf)
        self._size += len(buf)

    def hexdigest(self):
        return self.md5.hexdigest()

    @staticmethod
    def hexdigest_empty():
        return "d41d8cd98f00b204e9800998ecf8427e"

    @property
    def size(self):
        return self._size

    def is_invalid(self, md5: str = None, size: int = None):
        if size is not None:
            if self.size != int(size):
                return Exception(
                    f"Mismatch file size. expect: {size} actual: {self.size}"
                )

        if md5 is not None:
            if self.hexdigest() != md5:
                return Exception(
                    f"Mismatch file hash. expect: {md5} actual: {self.hexdigest()}"
                )

    @classmethod
    def from_file(cls, file_path, callback = lambda x: x):
        with open(file_path, "rb") as f:
            digest = cls()
            block_size = 1024 * 1024 * 128

            while True:
                buf = f.read(block_size)
                if not buf:
                    break

                digest.update(buf)
                callable(buf)

        return digest
