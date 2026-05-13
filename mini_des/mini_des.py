class MiniDES:
    """
    Simplified DES-like Feistel cipher.

    A simplified implementation of the DES (Data Encryption Standard) algorithm
    using a Feistel network structure for educational purposes.

    Attributes:
        Block size: 16 bits
        Key size: 24 bits
        Rounds: 8
        key: The 24-bit encryption key
        subkeys: List of 8-bit subkeys derived from the main key
    """

    def __init__(self, key: int) -> None:
        """
        Initialize MiniDES cipher with a 24-bit key.

        Args:
            key: A 24-bit integer key (0 <= key < 2^24)

        Raises:
            ValueError: If key is not in the valid 24-bit range
        """
        if not (0 <= key < 2**24):
            raise ValueError("24-bit key required")
        self.key: int = key
        self.subkeys: list[int] = self._key_schedule(key)

    def _key_schedule(self, key: int) -> list[int]:
        """
        Derive 8 subkeys from the 24-bit master key using rotation.

        Args:
            key: The 24-bit master key

        Returns:
            List of 8 subkeys (8-bit each)
        """
        subkeys: list[int] = []

        for i in range(8):
            # Rotate key left by i bits
            rotated: int = (
                ((key << i) | (key >> (24 - i)))
                & 0xFFFFFF
            )

            # Extract lowest 8 bits
            subkey: int = rotated & 0xFF
            subkeys.append(subkey)

        return subkeys

    def encrypt(self, plaintext: int) -> int:
        """
        Encrypt a 16-bit plaintext block using the Feistel network.

        Performs 8 rounds of Feistel operations, each using a subkey
        derived from the main key.

        Args:
            plaintext: A 16-bit integer to encrypt (0 <= plaintext < 2^16)

        Returns:
            The encrypted 16-bit ciphertext

        Raises:
            ValueError: If plaintext is not in the valid 16-bit range
        """
        if not (0 <= plaintext < 2**16):
            raise ValueError("16-bit plaintext required")

        # Split plaintext into left and right halves
        L: int = (plaintext >> 8) & 0xFF
        R: int = plaintext & 0xFF

        # Feistel rounds (8 rounds)
        for round_num in range(8):
            L, R = R, L ^ self._f_function(R, self.subkeys[round_num])

        # Final swap and combine
        return (R << 8) | L

    def decrypt(self, ciphertext: int) -> int:
        """
        Decrypt a 16-bit ciphertext block using the Feistel network.

        Reverses the Feistel operation by applying rounds in reverse order
        with subkeys also used in reverse.

        Args:
            ciphertext: A 16-bit encrypted integer (0 <= ciphertext < 2^16)

        Returns:
            The decrypted 16-bit plaintext

        Raises:
            ValueError: If ciphertext is not in the valid 16-bit range
        """
        if not (0 <= ciphertext < 2**16):
            raise ValueError("16-bit ciphertext required")

        # Split ciphertext into left and right halves
        L: int = (ciphertext >> 8) & 0xFF
        R: int = ciphertext & 0xFF

        # Reverse Feistel rounds (8 rounds in reverse order)
        for round_num in range(7, -1, -1):
            L, R = R, L ^ self._f_function(R, self.subkeys[round_num])

        # Final swap and combine
        return (R << 8) | L

    def _f_function(self, R: int, subkey: int) -> int:
        """
        The F-function (round function) of the Feistel network.

        A simplified round function that performs XOR and addition operations
        on the right half using the subkey. This is the core of each Feistel round.

        Args:
            R: The right half of the current block (8-bit)
            subkey: The subkey for this round (8-bit)

        Returns:
            The result of the F-function (8-bit)
        """
        return ((R ^ subkey) + 0x42) & 0xFF