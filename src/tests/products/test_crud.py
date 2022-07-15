import os

import pytest
from django.test import override_settings
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.urls import reverse
from products.models import Product


class TestCRUD:
    @pytest.mark.django_db
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_product_create(self, client, logo, celery_config):
        data = {"name": "test", "description": "test", "logo": logo}
        url = reverse("product-create")
        response = client.post(url, data=data)
        assert response.status_code == 201

        uuid = response.data["uuid"]
        product = Product.objects.get(uuid=uuid)
        assert product.rotate_duration > 0
        assert product.logo.url.startswith("/media/images/")

    @pytest.mark.django_db
    def test_product_list(self, client, products_list, token, dummy_user):
        url = reverse("product-list")
        response = client.get(url)
        assert response.status_code == 200
        assert response.data["count"] == 5

        url = reverse("product-list")
        response = client.get(url, data={"modified": True})
        assert response.status_code == 200
        assert response.data["count"] == 3

    def test_product_detail(self, client, dummy_product):
        url = reverse("product-detail", kwargs={"uuid": dummy_product.uuid})
        response = client.get(url)
        assert response.status_code == 200
        assert response.data["uuid"] == str(dummy_product.uuid)

    @pytest.mark.django_db
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_product_update(self, client, dummy_product, logo):
        data = {"name": "test", "description": "test", "logo": logo}
        url = reverse("product-update", kwargs={"uuid": dummy_product.uuid})
        encoded_data = encode_multipart(BOUNDARY, data)
        response = client.put(url, content_type=MULTIPART_CONTENT, data=encoded_data)
        assert response.status_code == 200

        data = {"name": "test1", "description": "test", "logo": logo}
        encoded_data = encode_multipart(BOUNDARY, data)
        response = client.put(url, content_type=MULTIPART_CONTENT, data=encoded_data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_product_delete(self, client, dummy_product):
        url = reverse("product-delete", kwargs={"uuid": dummy_product.uuid})
        response = client.delete(url)
        assert response.status_code == 204

        image_path = dummy_product.logo.path
        assert not os.path.exists(image_path)
