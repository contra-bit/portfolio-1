"""
Main entry point for the vmtranslator package when executed from the command
line; compiles Hack Virtual Machine program files to a hack assembly program.
"""

import os
import sys

from vmtranslator import translator

def translate_path(path):
	"""
	Translates either a single VM file, or a directory of such files.

	Args:
		path (string): The path of either a file, or directory. In the case of
			the former, the file will get translated to an assembly file with
			an identical basename; in the latter, the directory's files will
			all be translated to an assembly file with the directory's name as
			its basename. In either case, the output assembly file will have a
			`.asm` extension.
	"""

	def translate_vm_file(vm_path):
		"""Read and translate a VM file to an assembly string."""

		with open(vm_path) as vm_file:
			return translator.translate(vm_file.read())

	def write_asm_file(asm_path, asm):
		"""Write a string to a file."""

		with open(asm_path, "w") as asm_file:
			asm_file.write(asm)

	if os.path.isfile(path):
		raw_asm = translate_vm_file(path)
		asm_path = os.path.splitext(os.path.basename(path))[0] + ".asm"
		write_asm_file(asm_path, raw_asm)

	elif os.path.isdir(path):
		vm_paths = []
		for fpath in os.listdir(path):
			full_fpath = os.path.join(path, fpath)
			if os.path.isfile(full_fpath):
				vm_paths.append(full_fpath)
		raw_asm_blobs = [translate_vm_file(vm_path) for vm_path in vm_paths]
		asm_path = os.path.basename(path.rstrip(os.sep)) + ".asm"
		write_asm_file(asm_path, "\n".join(raw_asm_blobs))

if __name__ == "__main__":
	translate_path(sys.argv[1])
