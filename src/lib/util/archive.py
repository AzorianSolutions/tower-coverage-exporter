from pathlib import Path
from typing import Union


class ArchiveUtil:

    @staticmethod
    def create_archive(sources: list, target: Union[Path, str]) -> bool:
        from zipfile import ZipFile

        if not isinstance(target, Path):
            target = Path(target)

        with ZipFile(target, 'w') as zip_archive:
            for source in sources:
                if not isinstance(source, Path):
                    source = Path(source)
                zip_archive.write(source, source.name)
            zip_archive.close()

        return True
