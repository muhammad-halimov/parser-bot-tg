from bs4 import BeautifulSoup

html_content = ('<div id="cover7037" data-id="7037" class="covers" style="background:url('
                '/upl/modules/shop/360/5xi4fubg69.jpg);">')

# Создаем объект BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Находим элемент с нужным id
div_element = soup.find('div', id='cover7037')

# Получаем значение атрибута style
style_value = div_element.get('style')

# Извлекаем ссылку из значения атрибута style
# Можно использовать регулярные выражения или методы строк для этого
# В данном случае, если структура всегда будет одинаковой, можно использовать split()
if style_value:
    url = style_value.split('(')[1].split(')')[0]
    print("Извлеченная ссылка:", url)
else:
    print("Атрибут style не найден")
