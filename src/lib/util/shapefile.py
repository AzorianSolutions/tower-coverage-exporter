from pathlib import Path
from shapely.geometry import MultiPolygon
from typing import Union


class EsriShapefileUtil:

    @staticmethod
    def create_from_multipolygon(path: Union[Path, str], mp: MultiPolygon) -> bool:
        import shapefile
        from random import randrange
        from src.lib.util.archive import ArchiveUtil

        if not isinstance(path, Path):
            path = Path(path)

        w = shapefile.Writer(path)
        w.field('id', 'I')
        w.field('tier', 'I')

        rid: int = 0
        for geom in mp.geoms:
            rid += 1
            tier: int = randrange(1, 9, 1)
            w.shape(geom)
            w.record(id=rid, tier=tier)

        w.close()

        prj_path: Path = path.with_suffix('.prj')

        with prj_path.open('w') as prj_file:
            prj_file.write('GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,'
                           + 'AUTHORITY["EPSG","7030"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY["EPSG","6326"]],'
                           + 'PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,'
                           + 'AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]')
            prj_file.close()

        archive_path: Path = path.with_suffix('.zip')
        source_paths: list = [
            path.with_suffix('.dbf'),
            path.with_suffix('.prj'),
            path.with_suffix('.shp'),
            path.with_suffix('.shx'),
        ]

        ArchiveUtil.create_archive(source_paths, archive_path)

        for source_path in source_paths:
            source_path.unlink()

        return True
