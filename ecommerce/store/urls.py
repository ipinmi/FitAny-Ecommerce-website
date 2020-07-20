from django.urls import path

 #creating url paths for calling the views
from . import views



urlpatterns = [
    #empty string for base url
    path('', views.homepage, name='home'),
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('search/', views.search, name='search'),
    path('category/<int:id>/<slug:slug>', views.category_products, name='category_detail'),
    path('product/<int:id>/<slug:slug>/', views.productpage, name='product_details'),
    path('selectcurrency', views.selectcurrency, name='selectcurrency'),
    # path('savelangcur', views.savelangcur, name='savelangcur'),
    

    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
]

