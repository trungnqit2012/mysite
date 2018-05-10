# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
import django.utils.safestring as safestring
import datetime
import hashlib

class Product(models.Model):
    name = models.CharField("Tên sản phẩm", max_length=500)
    price = models.IntegerField("Giá", default=0)
    quantity = models.IntegerField("Số lượng tồn", default=0)
    unit = models.CharField("Đơn vị tính", max_length=50)
    color = models.CharField("Màu", max_length=50)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    description = models.TextField("Mô tả")

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.image:
            return safestring.mark_safe(
                '<img src="%s%s" width="150" height="150" />' % (settings.MEDIA_URL, self.image))
        else:
            return ""

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

class Item(Product):

    hash = models.CharField("hash", max_length=200, editable=False)
    previousHash = models.CharField("previoushash", max_length=200, editable=False)
    timeStamp = models.IntegerField("timestamp", default=0, editable=False)

