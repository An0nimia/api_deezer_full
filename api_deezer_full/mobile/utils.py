from Cryptodome.Cipher import AES


def aes_enc(key: str, word: bytes):
	c = AES.new(key.encode(), AES.MODE_ECB) # pyright: ignore

	p = c.encrypt(word).hex()

	return p


def aes_dec(key: str, word:str):
	c = AES.new(key.encode(), AES.MODE_ECB) # pyright: ignore

	p = c.decrypt(
		bytes.fromhex(word)
	).decode()

	return p