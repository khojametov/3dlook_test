import io
import os
import time

from config.celery import app
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from products.models import Product


def calculate_rotation_duration(image):
    start_time = time.time()
    image = image.rotate(180)
    return image, time.time() - start_time


@app.task
def upload_image(product_uuid, image_path, image_name, image_format):
    with open(image_path, "rb") as image_file:
        image = Image.open(image_file)
        temp = io.BytesIO()
        rotated_image, rotate_duration = calculate_rotation_duration(image)
        rotated_image.save(temp, image_format)
        memory_file = InMemoryUploadedFile(
            file=temp,
            field_name=None,
            name=image_name,
            content_type=image_format,
            size=rotated_image.size,
            charset=None,
        )
        product = Product.objects.get(uuid=product_uuid)
        product.logo = memory_file
        product.rotate_duration = rotate_duration
        product.save()

    os.remove(image_path)
