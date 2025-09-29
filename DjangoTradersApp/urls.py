from django.urls import path
from . import views

urlpatterns = [

	#region Function View URLs
	#URLs for Function based views - including Home.	
	path(
		route="",
		view=views.home,
		name="home"
	),

    path(
        'DjTraders/Customers', 
         views.CustomerListView.as_view(), 
         name='DjTraders.Customers'),

    path(
        'DjTraders/CustomerDetail/<str:customer_id>/', 
         views.CustomerDetailView.as_view(), 
         name='DjTraders.CustomerDetail'),

	#endregion Function View URLs

	#region Class Based View URLs
	path(
		route="customers/",
		view=views.CustomersList,
		name="CustomersList"
	),

	path(
		route="customers/<str:customer_id>/",
		view=views.CustomerDetail,
		name="CustomerDetail"
	),
    
	# Added in ListView for Product URL

	path(
        "DjTraders/Products/", 
        views.ProductListView.as_view(), 
        name="DjTraders.Products"
	),
    
	# Added in DetailView for Product URL

	path(
        "DjTraders/ProductDetail/<int:product_id>/", 
      	views.ProductDetailView.as_view(), 
        name="DjTraders.ProductDetail"
    ),
    
	# Added in Order URL
    path(
        "DjTraders/OrderDetail/<int:order_id>/", 
        views.OrderDetailView.as_view(), 
        name="DjTraders.OrderDetail"
	),
    
	# Added in Order URL Index
	path(
        "DjTraders/Orders/", 
    	views.OrderListView.as_view(), 
    	name="DjTraders.Orders"
	),

	#endregion Class Based View URLs
]