import os

from config.settings.base import MEDIA_ROOT
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django_filters.rest_framework import DjangoFilterBackend
from products.models import Product
from products.tasks import upload_image
from rest_framework import serializers
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny


class ProductSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    rotate_duration = serializers.FloatField(read_only=True)
    modified = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ("uuid", "name", "description", "logo", "rotate_duration", "modified")


class ProductCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.validated_data.pop("logo")
        product = serializer.save()
        image = self.request.FILES["logo"]
        path = default_storage.save(image.name, ContentFile(image.read()))
        tmp_file = os.path.join(MEDIA_ROOT, path)
        upload_image.delay(product.uuid, tmp_file, image.name, image.image.format)


class ProductDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "uuid"


class ProductListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("modified",)


class ProductUpdateView(UpdateAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "uuid"

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.modified:
            raise serializers.ValidationError("Product cannot be updated second time")
        serializer.validated_data.pop("logo")
        serializer.validated_data["modified"] = True
        serializer.save()

        image = self.request.FILES["logo"]
        path = default_storage.save(image.name, ContentFile(image.read()))
        tmp_file = os.path.join(MEDIA_ROOT, path)
        upload_image.delay(instance.uuid, tmp_file, image.name, image.image.format)


class ProductDeleteView(DestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "uuid"

    def perform_destroy(self, instance):
        if instance.logo:
            instance.logo.delete()
        instance.delete()
