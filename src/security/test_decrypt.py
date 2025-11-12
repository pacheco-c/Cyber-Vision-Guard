from cryptography.fernet import Fernet

# Carica la chiave
with open("security/secret.key", "rb") as f:
    key = f.read()

fernet = Fernet(key)

# Decifra un file .enc a tua scelta
file_path = "logs/event_1762935913.enc"  # metti il nome corretto

with open(file_path, "rb") as f:
    data_cifrata = f.read()

data_decifrata = fernet.decrypt(data_cifrata)
print("🔓 Contenuto decifrato:")
print(data_decifrata.decode())