import tarfile
import os

def as_dummy(func):
    func.is_dummy = True
    return func


@as_dummy
def decompress_dummy(src: str, dest: str):
    ...

@as_dummy
def compress_dummy(src: str, dest: str):
    ...


def decompress(src: str, dest: str):
    with tarfile.open(src, "r:gz") as tar:
        tar.extractall(path=src)

    for file in os.listdir("."):
        print(file)


def compress(src: str, dest: str):
    # tar.gzファイルを書き込みモードで開く
    with tarfile.open(dest, "w:gz") as tar:
        # ソースディレクトリ内のすべてのファイルとサブディレクトリに対して
        for root, dirs, files in os.walk(src):
            for file in files:
                # ファイルへの絶対パスを取得
                file_path = os.path.join(root, file)

                # tarアーカイブにファイルを追加
                tar.add(file_path, arcname=os.path.relpath(file_path, src))
