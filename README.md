# Passkey Vault

🔐 **Passkey Vault** is a secure CLI password manager with encryption, password generation, and strength checking. It supports backup, clipboard copy, detailed listing, and statistics.

## Features

- Store passwords in encrypted form (AES, Fernet)
- Generate strong passwords with various options
- Password strength checking and recommendations
- Copy password to clipboard (optional)
- Detailed listing and search
- Storage statistics (count, weak/strong passwords)
- Backup to plain JSON (backup)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Soulrom/secureLogger.git
   cd passkey-vault
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Minimum dependencies: `click`, `cryptography`, `pyperclip` (optional for clipboard)

## Usage

### Add a new entry

```bash
python vault.py add
```

### Generate a password automatically

```bash
python vault.py add --generate
```

### Retrieve a password

```bash
python vault.py get --site "gmail"
```

### Copy password to clipboard

```bash
python vault.py get --site "gmail" --copy
```

### Show detailed list

```bash
python vault.py list --details
```

### Generate 5 passwords of 20 characters each

```bash
python vault.py generate --length 20 --count 5
```

### Show statistics

```bash
python vault.py stats
```

### Create a backup

```bash
python vault.py backup
```

## Project Structure

- `vault.py` — CLI interface
- `vault_core.py` — class for database and encryption
- `password_utils.py` — password generation and strength checking

## Security

- Passwords are stored encrypted (Fernet/AES)
- Backup is created in plain text — do not store it unprotected!

## License

MIT License

---

**Author:** [Soulrom](https://github.com/Soulrom)
