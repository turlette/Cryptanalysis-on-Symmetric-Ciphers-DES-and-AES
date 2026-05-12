import pytest
from mini_des import MiniDES
def test_instantiation():
	cipher = MiniDES(0x123456)
	assert cipher.key == 0x123456
def test_encrypt_decrypt():
	cipher = MiniDES(0x123456)
	plaintext = 0xABCD
	ciphertext = cipher.encrypt(plaintext)
	recovered = cipher.decrypt(ciphertext)
	assert recovered == plaintext # If not working, adjust _f_function

# Run tests
pytest.main(['-v', 'mini_des/tests/test_mini_des.py'])