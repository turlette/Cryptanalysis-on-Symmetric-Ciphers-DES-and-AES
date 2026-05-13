import pytest
from mini_des.mini_des import MiniDES


def test_instantiation() -> None:
    """Test basic MiniDES instantiation with valid key."""
    cipher = MiniDES(0x123456)
    assert cipher.key == 0x123456


def test_encrypt_decrypt() -> None:
    """Test basic encrypt/decrypt roundtrip."""
    cipher = MiniDES(0x123456)
    plaintext = 0xABCD
    ciphertext = cipher.encrypt(plaintext)
    recovered = cipher.decrypt(ciphertext)
    assert recovered == plaintext


def test_invalid_key() -> None:
    """Test that invalid key (outside 24-bit range) raises ValueError."""
    # Test key too large
    with pytest.raises(ValueError, match="24-bit key required"):
        MiniDES(2**24)
    
    # Test negative key
    with pytest.raises(ValueError, match="24-bit key required"):
        MiniDES(-1)


def test_invalid_plaintext() -> None:
    """Test that invalid plaintext (outside 16-bit range) raises ValueError."""
    cipher = MiniDES(0x123456)
    
    # Test plaintext too large
    with pytest.raises(ValueError, match="16-bit plaintext required"):
        cipher.encrypt(2**16)
    
    # Test negative plaintext
    with pytest.raises(ValueError, match="16-bit plaintext required"):
        cipher.encrypt(-1)


def test_invalid_ciphertext() -> None:
    """Test that invalid ciphertext (outside 16-bit range) raises ValueError."""
    cipher = MiniDES(0x123456)
    
    # Test ciphertext too large
    with pytest.raises(ValueError, match="16-bit ciphertext required"):
        cipher.decrypt(2**16)
    
    # Test negative ciphertext
    with pytest.raises(ValueError, match="16-bit ciphertext required"):
        cipher.decrypt(-1)


def test_multiple_values() -> None:
    """Test encrypt/decrypt roundtrip with multiple plaintext values."""
    cipher = MiniDES(0x123456)
    
    test_values = [0x0000, 0x1234, 0xFFFF, 0xABCD, 0x5555, 0xAAAA]
    
    for plaintext in test_values:
        ciphertext = cipher.encrypt(plaintext)
        recovered = cipher.decrypt(ciphertext)
        assert recovered == plaintext, f"Failed for plaintext {hex(plaintext)}"


def test_different_keys_produce_different_ciphertexts() -> None:
    """Test that different keys produce different ciphertexts."""
    plaintext = 0xABCD
    
    cipher1 = MiniDES(0x123456)
    cipher2 = MiniDES(0x654321)
    
    ciphertext1 = cipher1.encrypt(plaintext)
    ciphertext2 = cipher2.encrypt(plaintext)
    
    assert ciphertext1 != ciphertext2


def test_boundary_values() -> None:
    """Test boundary values for plaintext and key."""
    # Test with minimum and maximum keys
    cipher_min = MiniDES(0x000000)
    cipher_max = MiniDES(2**24 - 1)
    
    plaintext = 0xAAAA
    
    ct_min = cipher_min.encrypt(plaintext)
    recovered_min = cipher_min.decrypt(ct_min)
    assert recovered_min == plaintext
    
    ct_max = cipher_max.encrypt(plaintext)
    recovered_max = cipher_max.decrypt(ct_max)
    assert recovered_max == plaintext


if __name__ == "__main__":
    pytest.main(["-v", "mini_des/tests/test_mini_des.py"])