"""
Classes representing the Hack Virtual Machine's memory manipulation operations.
"""

import re
from vmtranslator.operations import operation

class MemoryOp(operation.Operation):
	"""
	A memory operation.

	Attributes:
		_segment (string): The segment name, as parsed from a VM operation.
		_index (number): The segment index, as parsed from a VM operation.
		_module (string): The name of the module (file) that the operation was
			found in, for use in creating unique labels for `push` and `pop`
			operations on the `static` memory segment.
		STATIC_SEGMENTS (dictionary): Maps "static" segment names (see
			`_segment`) to their exact addresses in memory, which allows
			precomputing addresses via `_get_static_address()`.
		DYNAMIC_SEGMENTS (dictionary): Maps "dynamic" segment names to the
			pre-defined assembly symbols, which are translated to the memory
			locations that contain the base address of the desired segment.

		OP_STRING (string): Defined by subclasses; the string representation of
			this operation (eg, "push", "pop").
	"""

	OP_STRING = ""

	DYNAMIC_SEGMENTS = {
		"argument": "ARG",
		"local": "LCL",
		"this": "THIS",
		"that": "THAT"
	}

	STATIC_SEGMENTS = {
		"constant": 0,
		"pointer": 3,
		"temp": 5,
		"static": 16
	}

	def __init__(self, segment, index, module):
		self._segment = segment
		self._index = index
		self._module = module

	def _get_static_address(self):
		"""
		Should only be called if `self._segment` is in `self.STATIC_SEGMENTS`.

		Returns:
			(int) The target address of this memory operation.
		"""

		return self.STATIC_SEGMENTS[self._segment] + self._index

	def _get_static_label(self):
		"""
		Should only be called if `self._segment` is '"static"'.

		Returns:
			(string) The unique label for this operation on an index of the
				`static` memory segment; uses the current module as a label
				prefix.
		"""

		return "{0}.{1}".format(self._module, self._index)

	@classmethod
	def from_string(cls, string, state):
		parts = string.split(" ")
		if len(parts) == 3:
			oper, segment, index = parts
			if oper == cls.OP_STRING and \
				(segment in cls.STATIC_SEGMENTS or \
				segment in cls.DYNAMIC_SEGMENTS):
				return cls(segment, int(index), state["module"])

class PushOp(MemoryOp):
	"""
	Push a value from memory onto the stack.
	"""

	OP_STRING = "push"

	def to_assembly(self):
		asm = """@SP
			A = M
			M = D
			@SP
			M = M + 1
			"""

		if self._segment in self.DYNAMIC_SEGMENTS:
			base_address_asm = """@{0}
				D = M
				@{1}
				A = A + D
				D = M
				""".format(self.DYNAMIC_SEGMENTS[self._segment], self._index)

			return base_address_asm + asm

		elif self._segment in self.STATIC_SEGMENTS:
			if self._segment == "constant":
				return """@{0}
					D = A
					{1}""".format(self._index, asm)

			elif self._segment == "static":
				return """@{0}
					D = M
					{1}
					""".format(self._get_static_label(), asm)

class PopOp(MemoryOp):
	"""
	Pop a value from the stack and into a part of memory.
	"""

	OP_STRING = "pop"

	def to_assembly(self):
		asm = """
			@SP
			A = M - 1
			D = M
			@SP
			M = M - 1
			@{0}
			M = D
			"""

		if self._segment in self.DYNAMIC_SEGMENTS:
			base_address_asm = """@{0}
				D = M
				@pop_address
				M = D
				@{1}
				D = A
				@pop_address
				M = M + D
				""".format(
					self.DYNAMIC_SEGMENTS[self._segment], self._index
				)

			return base_address_asm + asm.format("pop_address\nA = M")

		elif self._segment in self.STATIC_SEGMENTS:
			if self._segment == "constant":
				return

			elif self._segment == "static":
				return asm.format(self._get_static_label())

			base_address = self._get_static_address()
			return asm.format(base_address)

OPS = [PushOp, PopOp]
