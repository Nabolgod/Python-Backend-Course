from time import sleep
from PIL import Image
from src.tasks.celery_app import celery_instance
from pathlib import Path


@celery_instance.task
def test_task():
    sleep(5)
    print("Я молодец")


@celery_instance.task
def resize_image(image_path: str):
    sizes = [1000, 500, 200]
    output_folder = Path('src/static/images')

    # Открываем изображение
    img = Image.open(image_path)

    # Получаем имя файла и его расширение

    image_path = Path(image_path)
    name = image_path.stem
    ext = image_path.suffix

    # Проходим по каждому размеру
    for size in sizes:
        # Сжимаем изображение
        img_resized = img.resize(
            (size, int(img.height * (size / img.width))),
            Image.Resampling.LANCZOS  # Современный антиалиасинг
        )

        # Формируем имя нового файла
        new_file_name = f"{name}_{size}px{ext}"

        # Полный путь для сохранения
        output_path = output_folder / new_file_name

        # Сохраняем изображение
        img_resized.save(output_path)

    print(f"Изображние сохранено в следующих размерах: {sizes} в папке {output_folder}")
