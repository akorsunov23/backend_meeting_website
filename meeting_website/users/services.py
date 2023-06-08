from io import BytesIO

from PIL import Image

from meeting_website.settings import BASE_DIR


def watermark_overlay(photo_user):
    """Наложение водяного знака на фото пользователя."""
    # Открываем изображение с помощью PIL
    image = Image.open(photo_user)
    # Путь к изображению водяного знака
    watermark = Image.open(f'{BASE_DIR}/watermark.png')
    # Изменение прозрачности
    alpha_value = 100
    alpha = watermark.getchannel('A').point(lambda i: i * alpha_value / 255)
    watermark.putalpha(alpha)
    # изменяем размер
    watermark = watermark.resize((watermark.width // 2, watermark.height // 2))
    # вычисляем нижний угол изображения для вставки водяного знака
    width, height = image.size
    bottom_corner = (width - round(watermark.width * 0.8), height - round(watermark.height * 0.8))
    # накладываем водяной знак по заданным координатам
    image.paste(watermark, bottom_corner, watermark)

    # Сохраняем обработанное изображение в памяти
    output = BytesIO()
    image.save(output, format='JPEG')
    output.seek(0)

    return output
