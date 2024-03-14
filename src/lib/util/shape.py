from rasterio.transform import AffineTransformer
from shapely.geometry import MultiPolygon


class ShapeUtil:

    @staticmethod
    def create_multipolygon_from_mask(mask, transformer: AffineTransformer) -> MultiPolygon:
        import shapely
        from numpy import int16
        from rasterio import features
        polygons: list = []

        for shape, value in features.shapes(mask.astype(int16), mask=(mask > 0), transform=transformer):
            polygons.append(shapely.geometry.shape(shape))

        result: MultiPolygon = shapely.geometry.MultiPolygon(polygons)

        if not result.is_valid:
            result = result.buffer(0)

        if not isinstance(result, MultiPolygon):
            result = shapely.geometry.MultiPolygon([result])

        return result
