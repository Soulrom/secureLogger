import os
import json
import click
from cryptography.fernet import Fernet
from datetime import datetime

class Vault:
    def __init__(self, key_file='key.key', db_file='vault.enc'):
        self.key_file = key_file
        self.db_file = db_file
        self.fernet = Fernet(self.load_key())

    def generate_key(self):
        """Генерує новий ключ шифрування"""
        key = Fernet.generate_key()
        with open(self.key_file, 'wb') as f:
            f.write(key)
        click.echo("🔑 Згенеровано новий ключ шифрування")

    def load_key(self):
        """Завантажує ключ шифрування або створює новий"""
        if not os.path.exists(self.key_file):
            self.generate_key()
        with open(self.key_file, 'rb') as f:
            return f.read()

    def load_db(self):
        """Завантажує та розшифровує базу даних"""
        if not os.path.exists(self.db_file):
            return {}
        try:
            with open(self.db_file, 'rb') as f:
                data = self.fernet.decrypt(f.read())
                return json.loads(data)
        except Exception as e:
            click.echo(f"❌ Помилка при завантаженні бази: {e}")
            return {}

    def save_db(self, data):
        """Шифрує та зберігає базу даних"""
        try:
            encrypted = self.fernet.encrypt(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))
            with open(self.db_file, 'wb') as f:
                f.write(encrypted)
        except Exception as e:
            click.echo(f"❌ Помилка при збереженні: {e}")

    def backup(self, backup_file):
        """Створити резервну копію (незашифровану)"""
        db = self.load_db()
        if not db:
            click.echo("📭 Немає даних для резервного копіювання")
            return
        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(db, f, ensure_ascii=False, indent=2)
            click.echo(f"💾 Резервну копію збережено в: {backup_file}")
            click.echo("⚠️  УВАГА: Файл не зашифрований! Видаліть після використання.")
        except Exception as e:
            click.echo(f"❌ Помилка створення резервної копії: {e}")
