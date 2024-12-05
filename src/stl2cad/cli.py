import os
import click
from stl2cad import utilities


@click.command()
@click.argument(
    "infile",
    type=click.Path(exists=True),
)
@click.option(
    "--outfile",
    "-o",
    help="The output filepath.",
    default=None,
    show_default=True,
    type=click.Path(exists=False),
)
@click.option(
    "--cadfile",
    "-c",
    help="Save the FreeCAD project file.",
    default=False,
    show_default=True,
    type=click.BOOL,
    is_flag=True,
)
def main(infile: str, outfile: str, cadfile: bool):
    # Get base filename
    filename = os.path.basename(os.path.abspath(infile))

    # Check outfile specification
    if outfile is None:
        # Convert to STEP by default
        outfile = f"{''.join(filename.split('.')[:-1])}.step"

    # Workflow
    doc = utilities.create_new_document()  # noqa: F841
    mesh = utilities.import_stl(infile)
    shape = utilities.shape_from_mesh(mesh)
    solid = utilities.make_solid(shape)
    refined = utilities.refine_shape(solid)

    # Export and save
    utilities.export_object(refined, outfile)
    if cadfile:
        fcstd_path = f"{''.join(filename.split('.')[:-1])}.FCStd"
        utilities.save_document(fcstd_path)
