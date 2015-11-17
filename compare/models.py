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

class ProductPhoto(models.Model):
    product_img=models.ImageField(upload_to='compare/product')

class Tag(models.Model): #temporary location as it is not a part of feed
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name


class Website(models.Model):
    name=models.CharField(max_length=255)
    product_url=models.URLField()
    price=models.FloatField(default=0.0)
    sentiment_rating=models.IntegerField(default=0)

class Product(models.Model):
    name=models.CharField(max_length=255)
    product_category=models.ForeignKey(ProductCategory)
    product_subcategory=models.ForeignKey(ProductSubcategory)
    available= models.ManyToManyField(Website, related_name="products")
    description=models.TextField()
    featured_image = models.ForeignKey(ProductPhoto,null=True,blank=True,related_name='featured')
    isbn_number=models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    created=models.DateTimeField(auto_now_add=True)
    visit_count=models.IntegerField(default=0)

class Reviews(models.Model):
    inside_text=models.TextField()
    product=models.ForeignKey(Product, related_name="p_reviews")
