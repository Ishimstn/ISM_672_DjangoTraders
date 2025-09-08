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
	)

	#endregion Class Based View URLs
]