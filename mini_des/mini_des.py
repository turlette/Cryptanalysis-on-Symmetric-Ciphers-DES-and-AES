class MiniDES:
	def __init__(self, key: int):
		if not (0 <= key < 2**24):
			raise ValueError("24-bit key required")
		self.key = key
		self.subkeys = self._key_schedule(key)

	def _key_schedule(self, key):
		subkeys = []
		for i in range(8):
			subkey = (key >> (i * 3)) & 0xFF
			subkeys.append(subkey)
		return subkeys

	def encrypt(self, plaintext):
		"""Simple encryption - this is your core cipher"""
		if not (0 <= plaintext < 2**16):
			raise ValueError("16-bit plaintext required")

		# Placeholder: can show structure without full impl
		L = (plaintext >> 8) & 0xFF
		R = plaintext & 0xFF

		# Feistel rounds (simplified for demo)
		for round_num in range(8):
			L, R = R, L ^ self._f_function(R, self.subkeys[round_num])

		return (R << 8) | L

	def decrypt(self, ciphertext):
		"""For now, just reverse subkey order"""
		if not (0 <= ciphertext < 2**16):
			raise ValueError("16-bit ciphertext required")

		L = (ciphertext >> 8) & 0xFF
		R = ciphertext & 0xFF

		for round_num in range(7, -1, -1):
			L, R = R, L ^ self._f_function(R, self.subkeys[round_num])

		return (R << 8) | L
	def _f_function(self, R, subkey):
		"""Round function - simplified"""
		return ((R ^ subkey) + 0x42) & 0xFF