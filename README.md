# __Modification of Gen_black script__

Original version: https://linhasverticais.wordpress.com </br>
Frito version: https://static1.downloadgamemods.com/Live%20for%20Speed/Tools/lfsdk.7z

Requires:</br>
Python 2.5 or 2.7</br>
PIL (Python Imaging Library) for python 2.5 or 2.7

If you run this script with pypy it can increase compiling speed by 10-50% depends by project size/quality (personaly i can't install PIL on pypy, so render_template not works :/)

It can be used with __[GenBlack Multicore 2020 DLC](https://github.com/PodFolio/GenBlack-Multicore-2020-DLC)__

## Added commands

### GLUE ressurected
welding two objects, to have smooth edges

```
GLUE <obj_name> <obj_name2> <distance>
```

example:</br>
```
GLUE m4_C1_Frnt m4_M1_side 0.005
```

### SET_TEXTURE_SLOT2 
for fixing 0.6V ALPHA textures

```
SET_TEXTURE_SLOT2 <0-4 transparent type> <part_name> <texture_name_ALP> <texture_appiled_mode> <texture_side> <0-15 slots>
```
0-4 transparent type:</br>
0 - not transpaent</br>
1 - fully transparent</br>
2 - glass</br>
3 - light glass</br>
4 - tinted glass (look for tinted glass in orginal Car2.psh)</br>

example:</br>
```
SET_TEXTURE_SLOT2 2 orb2 X_GTW_ALP single top 0 15
```

### SUBMESHES_COUNT 
set sub-mesh count for main mesh

```
SUBMESHES_COUNT <count> 
```
it works like `MESH 1` command but with extra step.</br>

example (if you want have total 69 meshes set it to 68. main mesh + 68 sub meshes (childs) = 69):</br>
```
SUBMESHES_COUNT 68
```

### MIRROR_STATE 
set mesh state. to be compatible with [DLC](https://github.com/PodFolio/GenBlack-Multicore-2020-DLC) it must have number at end of command.</br>

```
MIRROR_STATE <state> <its dlc?>
```
states:</br>
MIRROR_ONLY</br>
MIRROR_FIX_POSSIBLE</br>

its dlc?:</br>
0 - no</br>
1 - yes</br>

example:</br>
```
MESH 1
MIRROR_STATE MIRROR_ONLY 0
```

### MESH_TYPE
set mesh type. to be compatible with [DLC](https://github.com/PodFolio/GenBlack-Multicore-2020-DLC) it must have number at end of command.</br>

```
MESH_TYPE <type> <its dlc?>
```
type:</br>
MAIN - main mesh</br>
CALIPER - brake caliper</br>
WHEEL - steering wheel</br>
DEFAULT - default mesh</br>
ALWAYS_VISIBLE - always visible, even in F mode</br>
MIRROR - central rearview mirror</br>

its dlc?:</br>
0 - no</br>
1 - yes</br>

example:</br>
```
MESH 5
MESH_TYPE ALWAYS_VISIBLE 0
```

### MESH_FIX 
set mesh fix flag. to be compatible with [DLC](https://github.com/PodFolio/GenBlack-Multicore-2020-DLC) it must have number at end of command.</br>

```
MESH_FIX <state> <its dlc?>
```
states:</br>
ON -  mirror fix works</br>
OFF - mirror fix not work</br>

its dlc?:</br>
0 - no</br>
1 - yes</br>

example:</br>
```
MESH 2
MESH_FIX OFF 0
```

### DELETE_COL ressurected
deletes colision</br>

```
DELETE_COL <part_name>
```

### DELETE_SHADOW
deletes shadow</br>

```
DELETE_SHADOW <part_name>
```

### DELETE_MODEL ressurected
deletes parts by specific model</br>

```
DELETE_MODEL <part_name>
```

example:</br>
````
MODEL 4
DELETE_MODEL M1_side
````

### DEL
combined DELETE SHADOW/COL/MODEL command</br>

```
DEL <part_name> <0-2 colision/shadow> <model>
```
colision/shadow: </br>
0 - no colision/shadow</br>
1 - shadow</br>
2 - colision</br>

model: </br>
0-9 - model number</br>
-1 - no model choosed</br>

example:</br>
```
DEL M1_side 2 4
```

### CHECK_BB
check texture boundaries</br>

```
CHECK_BB <part_name>
```

example:</br>
```
CHECK_BB M1_side
```

### SET_BB
set new boundaries of texture</br>

```
SET_BB <part_name> <x1> <x2> <y1> <y2>
```

example:</br>
```
SET_BB M1_side -2.5 2.0 0.5 1.2
```

### SCALE_TEXTURE
scale texture</br>

```
SCALE_TEXTURE <part_name> <scale>
```
float, 1 = 100%</br>

example:</br>
```
SCALE_TEXTURE M1_side 0.5
```

### MOVE_TEXTURE
move texture</br>

```
MOVE_TEXTURE <part_name> <left/right> <up/down>
```

example:</br>
```
MOVE_TEXTURE M1_side 1.5 1.2
```


## Modified commands

### MIRROR GLASS/FIX2/FIX3/BODYOFF/BODYON/BODYFIX
added more mirror variants</br>

`FIX2/FIX3` works like normal FIX </br>

`GLASS` adding "smooth" for glass (like in orginal vob, i don't know if it does anything at all)</br>

`BODYOFF/BODYON/BODYFIX` adding "smooth" for body parts (like in orginal vob, i don't know if it does anything at all)</br>

### RENDER_TEMPLATE
now it makes transparent PNG files, just change in command .jpg to .png

example:</br>
```
RENDER_TEMPLATE l_find 33_LIGHTS1.png 0
```
