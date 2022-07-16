# Map Files and Objdump
## Map Files
### Creating Map Files
A map file is created when linking. Basically give some flags to linker to create mapfile.
```shell
 -Xlinker -Map=output.map 
```
```Shell
 -Wl,-Map=final.map 
```
There are symbols and origin addresses.
### Examining Object Files
To Examine an Object file we can use objdump tool.
```shell
objdump -x an_object_file.o
```