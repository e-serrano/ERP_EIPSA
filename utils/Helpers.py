from config.config_functions import get_path

def decrypt_password(password):
	from cryptography.fernet import Fernet
	with open(str(get_path("Resources", "clave.key")),"rb") as key_file:
		secret_key = key_file.read()

	f = Fernet(secret_key)
	password_decrypted=f.decrypt(password)
	return password_decrypted.decode()
