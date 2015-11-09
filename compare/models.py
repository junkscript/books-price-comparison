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

class Brand(models.Model):
    name=models.CharField(max_length=255)
    brand_logo=models.ImageField(upload_to='commerce/brand')

class Color(models.Model):
    color_name=models.CharField(max_length=255)

class Material(models.Model):
    material_name=models.CharField(max_length=255)

class ProductPhoto(models.Model):
    product_img=models.ImageField(upload_to='commerce/product')

class VendorType(models.Model):
    vendor_type=models.CharField(max_length=255)

class Vendor(models.Model):
    name=models.CharField(max_length=255)
    address=models.TextField()
    phone=models.CharField(max_length=12)
    vendor_type=models.ManyToManyField(VendorType)
    vendor_code=models.CharField(max_length=255)

class Tag(models.Model): #temporary location as it is not a part of feed
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name


class Website(models.Model):
    name=models.CharField(max_length=255)
    price=models.FloatField(default=0.0)

class Product(models.Model):
    name=models.CharField(max_length=255)
    price=models.IntegerField()
    brand=models.ForeignKey(Brand)
    product_category=models.ForeignKey(ProductCategory)
    product_subcategory=models.ForeignKey(ProductSubcategory)
    available= models.ManyToManyField(Website, related_name="products")
    description=models.TextField()
    material=models.ManyToManyField(Material)
    colors=models.ManyToManyField(Color)
    photos=models.ManyToManyField(ProductPhoto)
    featured_image = models.ForeignKey(ProductPhoto,null=True,blank=True,related_name='featured')
    sku_code=models.CharField(max_length=255)
    vendor=models.ManyToManyField(Vendor)
    width=models.FloatField()
    depth=models.FloatField()
    height=models.FloatField()
    return_policy=models.TextField(max_length=100)
    quantity=models.IntegerField()
    tags = models.ManyToManyField(Tag)
    created=models.DateTimeField(auto_now_add=True)

class Reviews(models.Model):
    inside_text=models.TextField()
    product=models.ForeignKey(Product, related_name="p_reviews")
