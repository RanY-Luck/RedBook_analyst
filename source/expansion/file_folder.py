import os
from contextlib import suppress
from pathlib import Path


def file_switch(path: Path) -> None:
    if path.exists():
        path.unlink()
    else:
        path.touch()


def remove_empty_directories(path: Path) -> None:
    exclude = {
        "\\.",
        "\\_",
        "\\__",
    }
    for dir_path, dir_names, file_names in os.walk(
        str(path),  # 转换Path对象为字符串
        topdown=False,
    ):
        if any(i in dir_path for i in exclude):
            continue
        if not dir_names and not file_names:
            with suppress(OSError):
                Path(dir_path).rmdir()  # 将字符串路径转回Path对象
