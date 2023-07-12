from fastkml import kml
from shapely import geometry
from shapely.geometry import Point


class RoI:

    def __init__(self, shape: geometry.Polygon, name: str):
        self.shape = shape
        self.name = name
        
    def get_center(self) -> geometry.Point:
        return self.shape.centroid

    def set_shape(self, polygon) -> None:
        self.shape = polygon

    def set_name(self, name) -> None:
        self.name = name

    def get_shape(self) -> geometry.Polygon:
        return self.shape

    def get_name(self) -> str:
        return self.name

    def is_in_RoI(self, point: geometry.Point) -> bool:
        return self.shape.contains(point)

    def get_area_squared_km(self)->float:
        return self.shape.area

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if other is None or self is None:
            return False
        if type(self) != type(other):
            return False
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name


def load_RoIs(file_path):
    with open(file_path, 'r') as my_file:
        doc = my_file.read()

    rois = []
    k = kml.KML()

    k.from_string(doc)
    features = list(k.features())
    placemarks = list(features[0].features())

    for x in placemarks:
        point_list = []
        for a, b in zip(x.geometry.exterior.coords[1], x.geometry.exterior.coords[0]):
            point_list.append(Point(a, b))
        poly = geometry.Polygon([[p.x, p.y] for p in point_list])
        rois.append(RoI(poly, x.name))

    return rois
