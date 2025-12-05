# src/utils.py

def calculate_discount(price, user_level):
    """
    Вычисляет скидку на основе уровня пользователя.
    Новая функция для системы лояльности.
    """
    discounts = {
        'standard': 0.05,
        'gold': 0.15,
        'platinum': 0.20
    }
    
    return price * (1 - discounts.get(user_level, 0))
