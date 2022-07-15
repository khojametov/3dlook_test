import os

import pytest
from config.settings.base import BASE_DIR
from django.core.files.uploadedfile import SimpleUploadedFile
from products.models import Product


@pytest.fixture
def logo(db):
    with open(os.path.join(BASE_DIR, "tests/fixtures", "download.jpeg"), "rb") as image:
        logo = SimpleUploadedFile(
            "download.jpeg",
            image.read(),
        )
    return logo


@pytest.fixture
def dummy_product(db):
    data = {
        "name": "test_product",
        "description": "This is a test product",
    }
    with open(os.path.join(BASE_DIR, "tests/fixtures", "download.jpeg"), "rb") as logo:
        logo = SimpleUploadedFile(
            "download.jpeg",
            logo.read(),
        )
        product = Product.objects.create(**data)
        product.logo = logo
        product.save()
    return product


@pytest.fixture
def products_list(db):
    data = {
        "name": "test",
        "description": "test",
    }
    for i in range(5):
        product = Product.objects.create(**data)
        if i % 2 == 0:
            product.modified = True
        product.save()
