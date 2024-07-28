from django.db import models
from django.conf import settings




class CommonModelInfo(models.Model):
    # slug = models.SlugField(unique=True)
    time_added = models.DateTimeField(auto_now_add=True)
    time_last_edited = models.DateTimeField(auto_now=True)
    last_edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True
        
        
# class Brands(CommonModelInfo):
#     title = models.CharField(max_length=25)

#     class Meta:
#         ordering = ['title']


#     def __str__(self):
#         return self.title



class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_title = models.CharField(max_length=20)
    category_path = models.CharField(max_length=100 ,default='')

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['category_title']

    def save(self, *args, **kwargs):
        if self.category_title:
            self.category_title = self.category_title.lower()
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_title
    
class Price(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.FloatField()
    currencycode = models.CharField(max_length=10)
    
    
    def __str__(self):
        return self.amount

class ItemImage(models.Model):
    image = models.ImageField(upload_to='images/dynamic/products/items/')
    alt_text = models.TextField()
    
    def __str__(self):
        return self.alt_text
class Item(CommonModelInfo):
    title = models.CharField(max_length=100)
    price = models.ForeignKey(Price , on_delete=models.CASCADE )
    availableForSale = models.BooleanField(default=True)
    # discount_price = models.FloatField(blank=True, null=True)
    # brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ForeignKey(ItemImage , on_delete=models.CASCADE)
    color = models.CharField(max_length=25 )
    size = models.CharField(max_length=25, blank=True , null=True)
    

    
    # class Meta:
    #     ordering = ['id']

    def __str__(self):
        return self.title
    
    
