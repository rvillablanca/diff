#!/usr/bin/python3
from sys import argv
import os
import filecmp
import shutil

if (len(argv) != 4):
	print("Número de parametros incorrectos")
	print("Uso:")
	print(argv[0], "<old_src> <new_src> <dest_dir>")
	exit(-1)

script, old, new, dest = argv

new_files = []
old_files = []

to_delete = []
to_replace = []
to_add = []

print("Procesando...")

for dirname, dirnames, filenames in os.walk(old):
	path = os.path.relpath(dirname, old)
	for old_filename in filenames:
		old_files.append(os.path.join(path, old_filename))
		
for dirname, dirnames, filenames in os.walk(new):
	path = os.path.relpath(dirname, new)
	for new_filename in filenames:
		new_files.append(os.path.join(path, new_filename))
		
for old_file in old_files:
	if old_file not in new_files:
		to_delete.append(old_file)
		
for new_file in new_files:
	if new_file not in old_files:
		to_add.append(new_file)
		

for to_delete_file in to_delete:
	old_files.remove(to_delete_file)
	
for found_file in old_files:
	file_old = os.path.join(old, found_file)
	file_new = os.path.join(new, found_file)
	equals = filecmp.cmp(file_old, file_new, False)
	if not equals:
		to_replace.append(found_file)

for to_copy_file in to_replace:
	dir_name = os.path.join(dest, os.path.dirname(to_copy_file))
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)
	shutil.copy(os.path.join(new, to_copy_file), os.path.join(dest, to_copy_file))
	
for to_copy_file in to_add:
	dir_name = os.path.join(dest, os.path.dirname(to_copy_file))
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)
	shutil.copy(os.path.join(new, to_copy_file), os.path.join(dest, to_copy_file))

if len(to_delete) > 0:
	to_delete_file = os.path.join(dest, "to_delete.txt")
	f_delete = open(to_delete_file, "w")
	for dfile in to_delete:
		f_delete.write(dfile + "\n")
	f_delete.close()
	print("Se deben eliminar los archivos descritos en", to_delete_file)
	
print("Listo")
