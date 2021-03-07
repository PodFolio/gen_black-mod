# __Gen_black script made by Rangel, modified by Frito, and now modified by ME__

Original version: https://linhasverticais.wordpress.com </br>
Frito version: https://static1.downloadgamemods.com/Live%20for%20Speed/Tools/lfsdk.7z

Requires:</br>
Python 2.5 or 2.7</br>
PIL (Python Imaging Library) for python 2.5 or 2.7

If you run this script with pypy it can increase compiling speed by 10-50% depends by project size/quality (personaly i can't install PIL on pypy, so render_template not works :/)

## Added commands

### GLUE ressurected
welding two objects, to have smooth edges

`GLUE <obj_name> <obj_name2> <distance>`</br>
example:</br>
`glue m4_C1_Frnt m4_M1_side 0.005`

### SET_TEXTURE_SLOT2 
for fixing 0.6V ALPHA textures

`SET_TEXTURE_SLOT2 <0-4 transparent type> <part_name> <texture_name_ALP> <texture_appiled_mode> <texture_side> <0-15 slots>`</br>
0-4 transparent type:</br>
0 - not transpaent</br>
1 - fully transparent</br>
2 - glass</br>
3 - light glass</br>
4 - tinted glass (look for tinted glass in orginal Car2.psh)</br>

example:</br>
`set_texture_slot2 2 orb2 X_GTW_ALP single top 0 15`


### DELETE_COL ressurected
deletes colision</br>

`DELETE_COL <part_name>`

### DELETE_SHADOW
deletes shadow</br>

`DELETE_SHADOW <part_name>`


### DELETE_MODEL ressurected
deletes parts by specific model</br>

`DELETE_MODEL <part_name>`</br>

example:</br>
`model 4`</br>
`DELETE_MODEL M1_side`

### DEL
combined DELETE SHADOW/COL/MODEL command</br>

`DEL <part_name> <0-2 colision/shadow> <model>`</br>
colision/shadow: </br>
0 - no colision/shadow</br>
1 - shadow</br>
2 - colision</br>

example:</br>
`DEL M1_side 2 4`

## Modified commands

### MIRROR GLASS/FIX2/FIX3/BODYOFF/BODYON/BODYFIX
added more mirror variants</br>

`FIX2/FIX3` works like normal FIX </br>

`GLASS` adding "smooth" for glass (like in orginal vob)</br>

`BODYOFF/BODYON/BODYFIX` adding "smooth" for body parts (like in orginal vob)</br>

### RENDER_TEMPLATE
now it makes transparent PNG files, just change in command .jpg to .png
