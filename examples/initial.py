from stl2cad.utilities import (
    create_new_document,
    import_stl,
    shape_from_mesh,
    make_solid,
    refine_shape,
    export_object,
    save_document,
)

# File paths
stl_path = "/home/kieran/Documents/packages/hypervehicle/cube.stl"
step_path = "cube.step"
iges_path = "cube.iges"
fcstd_path = "cube.FCStd"

# Workflow
doc = create_new_document()
mesh = import_stl(stl_path)
shape = shape_from_mesh(mesh)
solid = make_solid(shape)
refined = refine_shape(solid)

# Export and save
export_object(refined, step_path)
export_object(refined, iges_path)
save_document(fcstd_path)
