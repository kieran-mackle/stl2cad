# STL2CAD

A lightweight utility to convert STL files into CAD formats.


## Dependencies
The `stl2cad` package depends on [FreeCAD](https://www.freecad.org/), which can be downloaded 
[here](https://www.freecad.org/downloads.php).
The FreeCAD Python modules must also be on the Python path for `stl2cad` to work.

An example script of downloading and setting up FreeCAD in a Linux environment is provided below.

```
mkdir freecad
cd freecad

wget https://github.com/FreeCAD/FreeCAD/releases/download/1.0.0/FreeCAD_1.0.0-conda-Linux-x86_64-py311.AppImage

chmod -v +x ~/Downloads/FreeCAD_*.AppImage
./FreeCAD_*.AppImage --appimage-extract
```


## To Do
- clarify and test example install script (need to add to path)
- add better examples
- add tests
