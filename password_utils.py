import secrets
import string

class PasswordUtils:
    @staticmethod
    def generate_password(length=16, use_symbols=True):
        """Генерує безпечний пароль"""
        characters = string.ascii_letters + string.digits
        if use_symbols:
            characters += "!@#$%^&*"
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password

    @staticmethod
    def check_password_strength(password):
        """Перевіряє силу пароля"""
        score = 0
        feedback = []
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Довжина менше 8 символів")
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Немає малих літер")
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Немає великих літер")
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Немає цифр")
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
        else:
            feedback.append("Немає спеціальних символів")
        strength_levels = {
            0: "❌ Дуже слабкий",
            1: "🔸 Слабкий", 
            2: "🔶 Середній",
            3: "🔷 Хороший",
            4: "✅ Сильний",
            5: "🔒 Дуже сильний"
        }
        return strength_levels.get(score, "❓ Невідомо"), feedback
