from django.db import models

# Create your models here.
class ProductCategory(models.Model):
    product_category=models.CharField(max_length=200)
    featured_image=models.ImageField(upload_to='commerce/product_category')
    description=models.TextField(null=True, blank=True)

class ProductSubcategory(models.Model):
    product_subcategory=models.CharField(max_length=200)
    featured_image=models.ImageField(upload_to='commerce/product_subcategory')
    description=models.TextField(null=True, blank=True)

class Tag(models.Model): #temporary location as it is not a part of feed
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name


class Website(models.Model):
    name=models.CharField(max_length=255)
    product_url=models.URLField()
    price=models.FloatField(default=0.0)
    sentiment_rating=models.IntegerField(default=0)
    def __unicode__(self):
        return self.name

from django.core.files import File
import os
import urllib
class Product(models.Model):
    name=models.CharField(max_length=255)
    product_category=models.ForeignKey(ProductCategory,  null=True, blank=True)
    product_subcategory=models.ForeignKey(ProductSubcategory,  null=True, blank=True)
    available= models.ManyToManyField(Website, related_name="products")
    description=models.TextField()
    featured_image = models.ImageField(upload_to='compare/', null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    isbn_number=models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    visit_count=models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        if self.image_url and not self.featured_image:
            result = urllib.urlretrieve(self.image_url)
            self.featured_image.save(
                    os.path.basename(self.image_url),
                    File(open(result[0]))
                    )
            self.save()
        super(Product, self).save(*args, **kwargs)
    def __unicode__(self):
        return self.name


class Reviews(models.Model):
    inside_text=models.TextField()
    product=models.ForeignKey(Product, related_name="p_reviews")
