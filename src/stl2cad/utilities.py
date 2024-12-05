import FreeCAD as App
import Part
import Mesh


def create_new_document(doc_name: str = "Unnamed"):
    """Create a new FreeCAD document."""
    doc = App.newDocument(doc_name)
    return doc


def import_stl(file_path: str, object_name: str = "ImportedMesh"):
    """Import an STL file and return a mesh object."""
    mesh_obj = App.ActiveDocument.addObject("Mesh::Feature", object_name)
    mesh_obj.Mesh = Mesh.Mesh(file_path)
    App.ActiveDocument.recompute()
    return mesh_obj


def shape_from_mesh(mesh_object, tolerance: float = 0.01, sewing: bool = True):
    """Convert a mesh object to a shape."""
    shape = Part.Shape()
    shape.makeShapeFromMesh(mesh_object.Mesh.Topology, tolerance, sewing)
    feature = App.ActiveDocument.addObject(
        "Part::Feature", mesh_object.Label + "_Shape"
    )
    feature.Shape = shape
    App.ActiveDocument.recompute()
    return feature


def make_solid(shape_object):
    """Create a solid from a shape object."""
    solid = Part.Solid(shape_object.Shape)
    solid_feature = App.ActiveDocument.addObject(
        "Part::Feature", shape_object.Label + "_Solid"
    )
    solid_feature.Shape = solid
    App.ActiveDocument.recompute()
    return solid_feature


def refine_shape(solid_object):
    """Refine a solid object."""
    refined = App.ActiveDocument.addObject(
        "Part::Refine", solid_object.Label + "_Refined"
    )
    refined.Source = solid_object
    refined.Label = solid_object.Label
    solid_object.Visibility = False
    App.ActiveDocument.recompute()
    return refined


def export_object(obj, file_path: str):
    """Export an object to STEP or IGES format."""
    file_type = file_path.split(".")[-1]
    supported_types = ["step", "iges"]
    if file_type in supported_types:
        Part.export([obj], file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def save_document(file_path: str):
    """Save the FreeCAD document."""
    App.ActiveDocument.saveAs(file_path)
