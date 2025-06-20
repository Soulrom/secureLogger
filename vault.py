import click
from datetime import datetime
from vault_core import Vault
from password_utils import PasswordUtils

vault = Vault()

@click.group()
def cli():
    """🔐 Безпечне сховище паролів з шифруванням"""
    pass

@cli.command()
@click.option('--site', prompt='Сайт/Сервіс', help='Назва сайту або сервісу')
@click.option('--login', prompt='Логін/Email', help='Логін або email')
@click.option('--password', prompt='Пароль (Enter для генерації)', 
              default='', hide_input=True, help='Пароль або порожньо для генерації')
@click.option('--generate', '-g', is_flag=True, help='Згенерувати пароль автоматично')
@click.option('--length', '-l', default=16, help='Довжина згенерованого пароля')
def add(site, login, password, generate, length):
    """Додати новий запис до сховища"""
    db = vault.load_db()
    if site in db:
        if not click.confirm(f"Запис для '{site}' вже існує. Замінити?"):
            click.echo("❌ Скасовано")
            return
    if generate or not password:
        password = PasswordUtils.generate_password(length)
        click.echo(f"🎲 Згенерований пароль: {password}")
    strength, feedback = PasswordUtils.check_password_strength(password)
    click.echo(f"💪 Сила пароля: {strength}")
    if feedback:
        click.echo("💡 Рекомендації: " + ", ".join(feedback))
    db[site] = {
        "login": login, 
        "password": password,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat()
    }
    vault.save_db(db)
    click.echo(f"✅ Додано запис для: {site}")

@cli.command()
@click.option('--site', prompt='Сайт/Сервіс', help='Назва сайту для пошуку')
@click.option('--copy', '-c', is_flag=True, help='Скопіювати пароль в буфер')
def get(site, copy):
    """Отримати логін і пароль для сайту"""
    db = vault.load_db()
    if site in db:
        record = db[site]
        click.echo(f"🌐 Сайт: {site}")
        click.echo(f"👤 Логін: {record['login']}")
        click.echo(f"🔐 Пароль: {record['password']}")
        if 'created' in record:
            click.echo(f"📅 Створено: {record['created'][:19]}")
        if 'updated' in record:
            click.echo(f"🔄 Оновлено: {record['updated'][:19]}")
        if copy:
            try:
                import pyperclip
                pyperclip.copy(record['password'])
                click.echo("📋 Пароль скопійовано в буфер обміну")
            except ImportError:
                click.echo("📋 Для копіювання встановіть: pip install pyperclip")
    else:
        matches = [s for s in db.keys() if site.lower() in s.lower()]
        if matches:
            click.echo(f"❓ Точного співпадіння не знайдено. Можливо ви мали на увазі:")
            for match in matches:
                click.echo(f"  - {match}")
        else:
            click.echo("❌ Запис не знайдено")

@cli.command()
@click.option('--site', prompt='Сайт для видалення', help='Назва сайту для видалення')
@click.option('--force', '-f', is_flag=True, help='Видалити без підтвердження')
def delete(site, force):
    """Видалити запис з сховища"""
    db = vault.load_db()
    if site in db:
        if force or click.confirm(f"Видалити запис для '{site}'?"):
            del db[site]
            vault.save_db(db)
            click.echo(f"🗑️ Видалено: {site}")
        else:
            click.echo("❌ Скасовано")
    else:
        click.echo("❌ Запис не знайдено")

@cli.command()
@click.option('--search', '-s', help='Фільтр для пошуку')
@click.option('--details', '-d', is_flag=True, help='Показати детальну інформацію')
def list(search, details):
    """Показати всі збережені сайти"""
    db = vault.load_db()
    if not db:
        click.echo("📭 Сховище порожнє")
        return
    sites = list(db.keys())
    if search:
        sites = [s for s in sites if search.lower() in s.lower()]
        if not sites:
            click.echo(f"❌ Не знайдено записів з '{search}'")
            return
    click.echo(f"🌐 Записів у сховищі: {len(sites)}")
    click.echo("─" * 50)
    for site in sorted(sites):
        if details:
            record = db[site]
            click.echo(f"🔹 {site}")
            click.echo(f"   👤 Логін: {record['login']}")
            if 'created' in record:
                click.echo(f"   📅 Створено: {record['created'][:19]}")
            click.echo()
        else:
            click.echo(f"🔹 {site}")

@cli.command()
@click.option('--length', '-l', default=16, help='Довжина пароля')
@click.option('--count', '-c', default=1, help='Кількість паролів')
@click.option('--no-symbols', is_flag=True, help='Без спеціальних символів')
def generate(length, count, no_symbols):
    """Згенерувати безпечні паролі"""
    click.echo(f"🎲 Генерація {count} паролів довжиною {length} символів:")
    click.echo("─" * 50)
    for i in range(count):
        password = PasswordUtils.generate_password(length, not no_symbols)
        strength, _ = PasswordUtils.check_password_strength(password)
        click.echo(f"{i+1:2d}. {password} [{strength}]")

@cli.command()
@click.option('--backup-file', default='backup.json', help='Файл для резервної копії')
def backup(backup_file):
    """Створити резервну копію (незашифровану)"""
    vault.backup(backup_file)

@cli.command()
def stats():
    """Показати статистику сховища"""
    db = vault.load_db()
    if not db:
        click.echo("📭 Сховище порожнє")
        return
    click.echo("📊 Статистика сховища:")
    click.echo("─" * 30)
    click.echo(f"📈 Загальна кількість записів: {len(db)}")
    weak_passwords = 0
    strong_passwords = 0
    for site, record in db.items():
        strength, _ = PasswordUtils.check_password_strength(record['password'])
        if "Дуже слабкий" in strength or "Слабкий" in strength:
            weak_passwords += 1
        elif "Сильний" in strength or "Дуже сильний" in strength:
            strong_passwords += 1
    click.echo(f"🔒 Сильних паролів: {strong_passwords}")
    click.echo(f"⚠️  Слабких паролів: {weak_passwords}")
    if weak_passwords > 0:
        click.echo("💡 Рекомендується оновити слабкі паролі!")

if __name__ == "__main__":
    cli()