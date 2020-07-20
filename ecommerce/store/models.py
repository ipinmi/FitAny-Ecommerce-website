import uuid
from django.db import models
from django.urls import reverse
# import default django user model 
from django.contrib.auth.models import User
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
from currencies.models import Currency 

# mptt model for the categories
class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, unique=True)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # field names defining the ordering when new tree bodes are inserted 
    class MPTTMeta:
        order_insertion_by = ['title']
    
    # to create automatic slugs
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})
    
    # for showing the main category w subcategory in the admin
    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.title]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])



#customer model
class Customer(models.Model):
    #one to one relationship
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True,blank=True)


    def __str__(self):
        return self.name

#product model
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True) #many to one relation with Category
    name = models.CharField(max_length=200)
    description = models.TextField(default='')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    amount=models.IntegerField(default=0)
    #if the product doesnt require shipping (not a physical product)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    detail=RichTextUploadingField(null=True)
    slug = models.SlugField(null=False, unique=True, default=uuid.uuid4)
    create_at=models.DateTimeField(auto_now_add=True, null=True)
    update_at=models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name 

     # to create automatic slugs
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug}) 
    
    #incase the url of the image doesnt exist aand to avoid an error
    @property #makes it as an attribute not a method
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url 

#image model for the product oage 
class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	prodimage = models.ImageField()

	def __str__(self):
		return self.name

	# @property
	# def imageURL(self):
	# 	try:
	# 		url = self.prodimage.url
	# 	except:
	# 		url = ''
	# 	print('URL:', url)
	# 	return url


#order model
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

     # adding a shipping model looping through all the items to give a true or false value if the item is digita;
    @property 
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True

        return shipping   
    
    #to get total cart value and number of items
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    

#order items model (items within the carts)
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    #to get the total price 
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

#shipping model 
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address