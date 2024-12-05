import os
import FreeCAD as App
import Part
import Mesh


def create_new_document(doc_name: str = "Unnamed"):
    """Create a new FreeCAD document."""
    doc = App.newDocument(doc_name)
    return doc


def import_stl(
    file_path: str, object_name: str = "ImportedMesh", verbose: bool = False
):
    """Import an STL file and return a mesh object."""
    mesh_obj = App.ActiveDocument.addObject("Mesh::Feature", object_name)
    mesh_obj.Mesh = Mesh.Mesh(file_path)
    App.ActiveDocument.recompute()
    if verbose:
        print(f"STL imported: {file_path}.")
    return mesh_obj


def shape_from_mesh(
    mesh_object, tolerance: float = 0.01, sewing: bool = True, verbose: bool = False
):
    """Convert a mesh object to a shape."""
    shape = Part.Shape()
    shape.makeShapeFromMesh(mesh_object.Mesh.Topology, tolerance, sewing)
    feature = App.ActiveDocument.addObject(
        "Part::Feature", mesh_object.Label + "_Shape"
    )
    feature.Shape = shape
    App.ActiveDocument.recompute()
    if verbose:
        print("Shape created from mesh.")
    return feature


def make_solid(shape_object, verbose: bool = False):
    """Create a solid from a shape object."""
    solid = Part.Solid(shape_object.Shape)
    solid_feature = App.ActiveDocument.addObject(
        "Part::Feature", shape_object.Label + "_Solid"
    )
    solid_feature.Shape = solid
    App.ActiveDocument.recompute()
    if verbose:
        print("Solid object created from shape object.")
    return solid_feature


def refine_shape(solid_object, verbose: bool = False):
    """Refine a solid object."""
    refined = App.ActiveDocument.addObject(
        "Part::Refine", solid_object.Label + "_Refined"
    )
    refined.Source = solid_object
    refined.Label = solid_object.Label
    solid_object.Visibility = False
    App.ActiveDocument.recompute()
    if verbose:
        print("Shape refinements complete.")
    return refined


def export_object(obj, file_path: str, verbose: bool = False):
    """Export an object to STEP or IGES format."""
    file_type = file_path.split(".")[-1]
    supported_types = ["step", "iges"]
    if file_type in supported_types:
        Part.export([obj], file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    if verbose:
        print(f"Shape exported: {file_path}")


def save_document(file_path: str, verbose: bool = False):
    """Save the FreeCAD document."""
    App.ActiveDocument.saveAs(file_path)
    if verbose:
        print(f"CAD project saved: {file_path}")


def convert(infile: str, outfile: str, cadfile: bool = False, verbose: bool = False):
    # Workflow
    doc = create_new_document()  # noqa: F841
    mesh = import_stl(infile, verbose)
    shape = shape_from_mesh(mesh, verbose)
    solid = make_solid(shape, verbose)
    refined = refine_shape(solid, verbose)

    # Save new file
    export_object(refined, outfile, verbose)
    if cadfile:
        filename = os.path.basename(os.path.abspath(infile))
        fcstd_path = f"{''.join(filename.split('.')[:-1])}.FCStd"
        save_document(fcstd_path, verbose)
