import typing as _
if _.TYPE_CHECKING:
    from pathlib import Path


class Log:
    @classmethod
    def log(cls, message: str, tp: str = None) -> None:
        if tp:
            print(f'[{tp.upper()}] {message}')
        else:
            print(message)

    @classmethod
    def info(cls, message: str) -> None:
        cls.log(message, 'info')

    @classmethod
    def warning(cls, message: str) -> None:
        cls.log(message, 'warning')

    @classmethod
    def error(cls, message: str) -> None:
        cls.log(message, 'error')


class Folder:
    @classmethod
    def _delete(cls, root: 'Path') -> None:
        if root.is_file():
            root.unlink()
        else:
            for path in root.iterdir():
                cls._delete(path)
            root.rmdir()

    @classmethod
    def delete(cls, dir_name: 'Path') -> None:
        cls._delete(dir_name)

    @classmethod
    def create(cls, dir_name: 'Path') -> None:
        dir_name.mkdir(exist_ok=True)
