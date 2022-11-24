# THE WORLD DIRECTORY
This directory is where we put the files describing how to represent virtual worlds.



## OVERLAYS DIRECTORY
This folder contains what is needed to display a layer over the 3d virtual world scenes.


### HUD FILES
Those files are describing how to play and display the icons and sounds of the overlay.
*.css* format is a good choice because widely supported since long time ago.


### BITMAPS DIRECTORY
Contains images icons files to display over the 3d virtual world scenes.

The format of these files must support alpha and should be free to use :

 - tga
	The opening with gimp of tga image in color mode indexed with alpha channel, does not work well and is not enough commonly recognized

 - jpg
	may in some cases be preferable

 - png/mng
	is the preferred format

 - gif
	outdated

 - tiff
	is not enough commonly recognized

*.png* seems a well choice


### NOISES DIRECTORY
Contains sounds files to play with images icons.
The format of these files should be free to use, for that *.wav* is a fine choice.



## SCENES DIRECTORY
This folder contains what is needed to display a 3d virtual world by rendering engine.


### SCENES FILES
Each of these files is the description of a virtual world containing 3d virtual objects.
The format is the common *.yml* because of the ability of hierarchical description.


### ITEMS DIRECTORY
Contains items files describing how to represent each 3d objects.
The format is also the common *.yml* because of the ability of hierarchical description.


### MODELS DIRECTORY
In this folder are grouped all the necessary files for the virtual objects.
 - **common** subdirectory contains files shared by many objects.
 - **specific** subdirectory contains files of unique object. 

#### 3d mesh files
Files describing three-dimensional forms shapes of objects should contains :
 - points,lines,curves,faces
 - normals for the inside and the outside
 - uv Mapping (textures coordinates) allow to know how to apply an image on the mesh
 - ability to assign material for each face

(These files must be able to be associated with any material or texture files)

It is preferable to let the graphics engine manage/generate the necessary *L.O.D.*(level of detail) of meshes.
(less work for the graphic designers)

The file format must be free to use and widely supported by common 3d modlers apps (Blender,FreeCad,...)

 - *.poly* TetGen,
	a 3d PLC is described by a boundary.(B-Rep) Freecad can export it, But no texture/materials informations.
	
 - BRep Format (Open Cascade)
	txt format,Freecad can export, But no texture/materials informations.
	
 - 3D Studio files *.3ds*
	a binary file format, can be exported from Blender, Not open source.
	
 - Milkshape 3D *.ms3d*
	binary, unofficial specification, Blender can export it.
	
 - JT
	Is a very sophisticated 3D format including mesh LOD,  Developed by Siemens PLM Software, But not enough supported by the modelers softwares
	
 - OpenCTM
	Is open 3D geometry technology for storing triangle-based meshes in a compressed format, But not enough supported by the modelers softwares
	
 - Object File Format *.off*
	a geometry definition file format, containing the description of the polygons of 3D object. natif geomview but Freecad can export it,
	
 - Wavefront *.obj*
	open source, text format, very common with 3d modlers softwares, including Blender/Freecad

 - STL (STereoLithography) *.stl*  *.ast*
	ASCII or binary, contains no other info than vertices forming triangular surface and normals, exported by Blender/Freecad, stl is best for real object scanning or 3D printing, but does not save enough data for virtual object rendering.

 - PLY (Polygon File Format) or the Stanford Triangle Format
	ASCII or binary(not xml), contains the description of exactly one object, vertex/normal/uv/color. is an export of Blender/Freecad, its a complex format, which can be customized to incorporate all sorts of additional data.

 - COLLADA (COLLAborative Design Activity) *.dae*
	XML structure, not in export of Blender but in export of FreeCad

 - Extensible 3D (X3D)  (VRML 2.0/97 succesor)
	XML structure, in Blender export

 - Additive Manufacturing File Format (AMF)
	stl successor, XML structure

 - 3D Manufacturing Format or 3MF
	XML-based data format, includ information about materials, colors, and other information that cannot be represented in the STL format.

 - Virtual Reality Modeling Language (VRML) *.wrl* renamed VRML97(VRML 2.0) in 1996
	X3D precursor, XML textformat,including: textures, points, lines, polygons, spheres, cubes, cones, cylinders, text, images, animations, lighting, sounds, hyperlinks, colors, material, scripts, fog, extrusion, video..., Blender/freecad

After studying the *.obj* format with *.mtl* seems to be currently the most appropriate format
(in Blender the mesh must be exported in *.obj* format with **Yup** and **-Z forward** to be represented correctly by the *zVs engine*)

#### materials files
For example, gold, silver, stone, plastic, glass,
and even non-isotropic materials like wood, machine, or body.
these materials description files give the different color effects to the objects and then their color rendered on screen.
But this type of file must only contain the graphic representation of materials.
The physical properties of the materials are described outside.
It means that density of materials(kg/m3) is excluded contrary to :

 - radiance
	specify the the color of emitted light.
	So, even if the object is in the dark, non-black color appears on it
	the RGBA values of this parameter are the color of the light emitting from the object.
	For example a bulb or neon can be painted in red but with yellow emit parameter simulating internal illuminating
	(The alpha component is used to decide whether the object's material is transparent)

 - diffusion
	Specify the diffused color,
	can be considered as a layer of paint covering the the object.
	The RGB components of this represent the color diffused by the paint during fullspectral illuminance(pure white light) and maximum intensity (inverse of absolute darkness)
	The alpha component represents the transparency of the paint layer.
	The paint goes from totally transparent to unable to let the material surface to appear, totally opaque.

 - reflection
	This defines the intensity of the specular highlight due to the roughness of the material.
	It can be considered as a matte to gloss variation of the paint,
	Normally the color of the specular reflection is always equal to the color of the lighting.

 - transparency
	Any light passing through an object not totally opaque is filtered.
	This parameter allows the specify the color passing through.

 - refraction
	Light change direction and disperse when passing from one transparent medium to another(prism, rainbow,...)

There are only few 3d materials file format available currently,
*.mtl* is the only one i know enough recognized that is suitable for this task.

#### textures files
Are images applied to the faces of objects.
These images (animated or not) modify the basic color resulting from the parameters of the object material.
(Not all 3D objects need textures, this is optional)

It's possible to apply multi layers of textures of the same type to form a final texture.
For example, we can have a body texture on which a tattoo texture is added.
The share of textures for any additional detail is easier and spare more.
But if we dont want waste memory with the space of the images not used at texture compilation, it's necessary to indicate textures position.
Also there is  a disadvantage, because it is more convenient to visualize and manipulate the final texture with softwares, like Gimp.

At the moment i think procedural textures should be generated as a series of image files which can be treated as normal texture files.
It is possible to obtain the illusion of procedural textures by generating a large number of files of different textures, exceeding the limit of human memory and therefore its recognition.

The flaw of RGBA images (red,green,blue+transparency) is the difficulty to distinguish transparency pixels in the image.
Because the transparency must necessarily be replaced by a color or a checkerboard pattern.
For example if the transparency is represented by the white color, it is difficult to know if a pixel is gray or half-transparent black.
This is why it may be preferable to have images in RGB mode instead, with an additional image in grayscale mode for the transparency.
Using RGB+grayscale images saves memory space, because if no transparency is needed a place for 4th component does not need to exist in the image files.
But in practice when creating a semi-transparent textures it is useful to be able to test it easily on different backgrounds.

Previously the Phong rendering type was used and the textures files was adapted for that.
But now the rendering system commonly used is PBR(more commonly known as Physically Based Rendering)
So, its necessary to have textures images matching the new system.

 - emit
	To represent, for example, small lamps or an incandescent glow.

 - albedo
	Can be considered as colors of the coat of paint.

 - normal
	The normal map texture derivated from bump map gives the object's faces orientations.

 - metallic
	If the object have some metallic surface a specific texture map can be added.

 - smoothness
	Or roughness map instead(which some find more intuitive), specifies the specular effect on the object surface.

 - ao:
	The ambient occlusion or AO map specifies an extra shadowing factor of the surface. If we have a brick surface for instance the albedo texture should have no shadowing information. the AO map will specify darkened edges where it's more difficult for light to escape.

There is a lot of available images formats for textures.
Most image formats are using 8bits color components, but it would be fair to use much more bits.

 - tga
	The opening with gimp of tga image in color mode indexed with alpha channel, does not work well and is not enough commonly recognized

 - jpg
	may in some cases be preferable

 - png/mng
	is the preferred format
	
 - gif
	outdated
	
 - tiff
	is not enough commonly recognized

*.png* or *.jpg* are well choices.

#### sound files
Are files of the different sound effects emitted/produced by the objects.
The virtual world engine must be able to vary these sounds depending on the distance and the displacement of the emitter/receiver.
The format of these files should be free to use and commonly supported by softwares.
For that *.wav* is a fine choice

#### ref directory
A directory where to put files that can be used as a references to build virtual objects can contains :
- image files showing the real object (photos,blueprints)
- historic documents and reports describing the object
- original soundtrack records and videos

#### source directory
In this we can put files from which are developed what is needed by the virtual objects.
For example *.blend* files for 3D mesh construction.
or Gimp,Inskape files that allows to create and rework the different textures.
or some bumpmaps for surface embossing,(grayscale image file on 1byte(256 shades) are sufficient)
(from bumpmaps we can make normals images that are more convenient for CPU but less practical to edit for the humans)
Also some Audacity files from which we can work on the sounds for the virtual objects.
