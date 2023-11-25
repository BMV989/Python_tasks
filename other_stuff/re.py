import re


def find_repeated_words(text: str) -> list[str]:
    word_count = {}
    words = re.findall(r'\b\w+\b', text.lower())

    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    repeated_words = [word for word, count in word_count.items() if count >= 3]
    return repeated_words


def find_repeated_letter(text: str) -> str | None:
    pattern = r'(.)\1{9}'
    words = re.finditer(pattern, text)
    for word in words:
        print(word)


def check_password_strength(password: str) -> str:
    if not re.search(r'[a-z]', password) or not re.search(r'[A-Z]', password):
        return "Пароль должен содержать буквы разного регистра."

    if not re.search(r'\d', password):
        return "Пароль должен содержать хотя бы одну цифру."

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Пароль должен содержать хотя бы один специальный символ."

    # Если все проверки пройдены, пароль считается надежным
    return "Пароль надежный."


def phone_number_parse(text: str) -> [str, str]:


    # Пример использования
text = "Эта строка содержит букву 'а' 10 раз подряд: аааааааааа"

repeated_letter = find_repeated_letter(text)
print(repeated_letter)


text = "Hello Hello Hello w w w"

repeated_words = find_repeated_words(text)
print(repeated_words)
# Пример использования
password = "Mysecurepassword123!"
result = check_password_strength(password)
print(result)
