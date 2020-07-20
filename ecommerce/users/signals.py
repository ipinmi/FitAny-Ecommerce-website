# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.contrib.auth.models import Group
# from store.models import Customer


# def customer_profile(sender, instance, created, **kwargs):
#     if created: 
#         group = Group.objects.get(name='customer')
#         instance.groups.add(group)
# 		#Added username after video because of error returning customer name if not added
#         Customer.objects.create(
# 		    user=instance,
# 		    name=instance.username,
# 		)

#         print('Profile created')

# post_save.connect(customer_profile, sender=User)