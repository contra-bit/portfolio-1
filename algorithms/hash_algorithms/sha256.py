"""
`sha256` contains an implementation of the SHA-256 hash algorithm.

It adheres as much as possible to the pseudocode in
`http://en.wikipedia.org/wiki/SHA-2` for purposes of readability. Some of the
code is thus a little inelegant, unoptimized, and PEP8-incompliant.
"""

import hashlib

def sha256(string):
	"""
	Generate the SHA-256 digest of a string.

	Args:
		string (str): The string to process.

	Returns:
		(int) The hash of `str`.
	"""

	def rightRotate(x, c):
		"""
		Perform a circular right-rotation.

		Args:
			x (int): The value to rotate.
			c (int): The number of bits to rotate `x` by.

		Returns:
			(int) `x` shifted right `c` bits, with those that overflowed
			reappearing on the left.
		"""

		return (x >> c) | (x << (32 - c))

	# Initialize hash constants.
	h0 = 0x6a09e667
	h1 = 0xbb67ae85
	h2 = 0x3c6ef372
	h3 = 0xa54ff53a
	h4 = 0x510e527f
	h5 = 0x9b05688c
	h6 = 0x1f83d9ab
	h7 = 0x5be0cd19

	# Initialize array of round constants.
	k = [
		0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
		0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
		0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
		0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
		0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
		0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
		0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
		0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
		0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
		0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
		0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
	]

	bin_msg = "".join([bin(ord(byte))[2:].zfill(8) for byte in string])
	bin_msg += "1" + (448 - 1 - len(bin_msg) % 512) * "0"
	bin_msg += bin(len(string) * 8)[2:].zfill(64)

	# Partition bin_msg into 512-bit chunks.
	for chunk in range(len(bin_msg) / 512):

		# Partition chunk into an array `w` containing 16 32-bit words.
		w = []
		for word in range(16):
			start = chunk * 512 + word * 32
			w.append(bin_msg[start:(start + 32)])

		# Extend original 16-word array to 64 words.
		for i in range(16, 64):
			s0 = rightRotate(int(w[i - 15], 2), 7) ^ \
				rightRotate(int(w[i - 15], 2), 18) ^ (int(w[i - 15], 2) >> 3)
			s1 = rightRotate(int(w[i - 2], 2), 17) ^ \
				rightRotate(int(w[i - 2], 2), 19) ^ (int(w[i - 2], 2) >> 10)
			total = (int(w[i - 16], 2) + s0 + int(w[i - 7], 2) + s1) % 2**32
			w.append(bin(total)[2:])

		# Initialize word buffers.
		a = h0
		b = h1
		c = h2
		d = h3
		e = h4
		f = h5
		g = h6
		h = h7

		# Primary for-loop that hashes message.
		for i in range(64):

			s1 = rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25)
			ch = (e & f) ^ (~e & g)
			temp1 = h + s1 + ch + k[i] + int(w[i], 2)
			s0 = rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22)
			maj = (a & b) ^ (a & c) ^ (b & c)
			temp2 = s0 + maj

			# Update word buffers.
			h = g
			g = f
			f = e
			e = (d + temp1) % 2 ** 32
			d = c
			c = b
			b = a
			a = (temp1 + temp2) % 2 ** 32

		# Update hash constants
		h0 = (h0 + a) % 2 ** 32
		h1 = (h1 + b) % 2 ** 32
		h2 = (h2 + c) % 2 ** 32
		h3 = (h3 + d) % 2 ** 32
		h4 = (h4 + e) % 2 ** 32
		h5 = (h5 + f) % 2 ** 32
		h6 = (h6 + g) % 2 ** 32
		h7 = (h7 + h) % 2 ** 32

	constants = [h0, h1, h2, h3, h4, h5, h6, h7]
	digest = 0
	for ind in xrange(len(constants)):
		digest += constants[ind] << (32 * (len(constants) - ind - 1))
	return digest

if __name__ == "__main__":
	msg = "The quick brown fox jumps over the lazy dog"
	expected = int(hashlib.sha256(msg).hexdigest(), 16)
	hash_digest = sha256(msg)
	print "Hash of '%s': %x\nMatches expected: %s." % (
		msg, hash_digest, hash_digest == expected
	)