# __Modification of Gen_black script__

Original version: https://linhasverticais.wordpress.com </br>
Frito version: https://static1.downloadgamemods.com/Live%20for%20Speed/Tools/lfsdk.7z

__Requires:__</br>
Python 2.5 or 2.7</br>
PIL (Python Imaging Library) for python 2.5 or 2.7

If you run this script with [pypy](https://www.pypy.org) it can increase compiling speed by 10-50% depends by project size/quality (personaly i can't install PIL on [pypy](https://www.pypy.org), so render_template not works :/)

It can be used with __[GenBlack Multicore 2020 DLC](https://github.com/PodFolio/GenBlack-Multicore-2020-DLC)__

<hr>

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#added-commands">Added commands</a>
      <ul>
        <li><a href="#glue-ressurected">GLUE</a></li>
        <li><a href="#set_texture_slot2">SET_TEXTURE_SLOT2</a></li>
        <li><a href="#submeshes_count">SUBMESHES_COUNT</a></li>
        <li><a href="#mirror_state">MIRROR_STATE</a></li>
        <li><a href="#mesh_type">MESH_TYPE</a></li>
        <li><a href="#mesh_fix">MESH_FIX</a></li>
        <li><a href="#delete_col-ressurected">DELETE_COL</a></li>
        <li><a href="#delete_shadow">DELETE_SHADOW</a></li>
        <li><a href="#delete_model-ressurected">DELETE_MODEL</a></li>
        <li><a href="#del">DEL</a></li>
        <li><a href="#check_bb">CHECK_BB</a></li>
        <li><a href="#set_bb">SET_BB</a></li>
        <li><a href="#scale_texture">SCALE_TEXTURE</a></li>
        <li><a href="#move_texture">MOVE_TEXTURE</a></li>
        <li><a href="#plate_fix">PLATE_FIX</a></li>
      </ul>
    </li>
    <li>
      <a href="#modified-commands">Modified commands</a>
      <ul>
        <li><a href="#mirror-glassfix2fix3bodyoffbodyonbodyfix">MIRROR GLASS/FIX2/FIX3/BODYOFF/BODYON/BODYFIX</a></li>
        <li><a href="#render_template">RENDER_TEMPLATE</a></li>
      </ul>
    </li>
    <li>
      <a href="#misc">Misc</a>
      <ul>
        <li><a href="#lfscarimp-locked-mod-object-dump">LFSCarImp locked mod object dump</a></li>
        <li><a href="#base-vobs">Base vobs</a></li>
        <li><a href="#gen_black-notepad-syntax">Gen_Black Notepad++ syntax</a></li>
      </ul>
    </li>
    <li><a href="#show-your-support">Show your support</a></li>
  </ol>
</details>

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
set sub-mesh count for main mesh (based on idea by [DemonRed](https://www.facebook.com/demonred8/)), intendent to use with __[GenBlack Multicore 2020 DLC](https://github.com/PodFolio/GenBlack-Multicore-2020-DLC)__</br>

```
SUBMESHES_COUNT <count> 
```
it works like `MESH 1` command but with extra step.</br>

example (if you want have total 69 meshes set it to 68. main mesh + 68 sub meshes (childs) = 69):</br>
```
SUBMESHES_COUNT 68
```

### MIRROR_STATE 
set mesh state (based on idea by [DemonRed](https://www.facebook.com/demonred8/))</br>

```
MIRROR_STATE <state>
```
states:</br>
MIRROR_ONLY</br>
MIRROR_FIX_POSSIBLE</br>

example:</br>
```
MESH 1
MIRROR_STATE MIRROR_ONLY
```

### MESH_TYPE
set mesh type (based on idea by [DemonRed](https://www.facebook.com/demonred8/))</br>

```
MESH_TYPE <type>
```
type:</br>
MAIN - main mesh</br>
CALIPER - brake caliper</br>
WHEEL - steering wheel</br>
DEFAULT - default mesh</br>
ALWAYS_VISIBLE - always visible, even in F mode</br>
MIRROR - central rearview mirror</br>

example:</br>
```
MESH 5
MESH_TYPE ALWAYS_VISIBLE
```

### MESH_FIX 
set mesh fix flag (based on idea by [DemonRed](https://www.facebook.com/demonred8/))</br>

```
MESH_FIX <state>
```
states:</br>
ON -  mirror fix works</br>
OFF - mirror fix not work</br>

example:</br>
```
MESH 2
MESH_FIX OFF
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
-1  - no model choosed</br>

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

### PLATE_FIX
simple number plate fix</br>

```
PLATE_FIX <part_name>
```

example:</br>
```
CHECK_BB plate_Front
#result of check > 0.268096923828 0.50129699707 0.160095214844 0.24609375

SET_BB plate_Front 0.50129699707 0.268096923828 0.160095214844 0.24609375
PLATE_FIX plate_Front
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


## Misc

### LFSCarImp locked mod object dump
use __vob_obj_cimp.py__ to dump LFSCarImp locked vob files ;)</br>

### Base vobs
in __BASE__ folder:</br>
- __P__ folder cointains defauld vob bases from pre virtual mirrors ("big wing") update</br>
- __R__ folder cointains defauld vob bases from post virtual mirrors ("big wing") update, compatible with 0.6V</br>
- __Custom__ folder cointains custom vob bases</br>

### Gen_Black Notepad++ syntax
Syntax for Notepad++</br>
_Language > User Defined Language > Define your language... > Import > chose genblack.xml_</br>
It works with [Visual Studio 2019 Dark Theme for Notepad++](https://github.com/hellon8/VS2019-Dark-Npp)</br>

example:</br>
![Gen_Black Notepad++ syntax](https://i.imgur.com/eDhyuZN.png)


## Show your support
Please ⭐️ this repository if this project helped you!</br>
<a href="https://paypal.me/podfolio">
  <img src="https://i.imgur.com/9tOq2a6.png" width="200">
</a>

