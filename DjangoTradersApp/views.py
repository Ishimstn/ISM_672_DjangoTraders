from django.views.generic import ListView, DetailView
from django.shortcuts import render

from .models import Customers, Products, Categories, Suppliers, Orders, OrderDetails


# Create your views here.
def home(request):
    return render(
        request=request,
        template_name="DjangoTradersApp/welcome.html",
    )


# region Function-based customer views
def CustomersList(request):
    """View function to display all customers."""
    customers = Customers.objects.all()

    return render(
        request=request,
        template_name="DjangoTradersApp/Customers/List.html",
        context={"customers": customers},
    )


def CustomerDetail(request, customer_id):
    """View function to display the details of a specific customer."""
    customer = Customers.objects.get(customer_id=customer_id)
    return render(
        request=request,
        template_name="DjangoTradersApp/Customers/Detail.html",
        context={"customer": customer},
    )
# endregion


# region Class-based Customer views
class CustomerListView(ListView):
    """
    View to list all customers with search functionality.
    """
    model = Customers
    template_name = "DjangoTradersApp/Customers/Index.html"
    context_object_name = "customers"

    def get_queryset(self):
        """Get the filtered queryset based on search criteria."""
        queryset = super().get_queryset()

        customer_search = self.request.GET.get("customer")
        if customer_search:
            queryset = queryset.filter(company_name__startswith=customer_search)

        contact_search = self.request.GET.get("contact")
        if contact_search:
            queryset = queryset.filter(contact_name__icontains=contact_search)

        city_search = self.request.GET.get("city")
        if city_search:
            queryset = queryset.filter(city__startswith=city_search)

        country_search = self.request.GET.get("country")
        if country_search:
            queryset = queryset.filter(country__exact=country_search)

        contact_title_search = self.request.GET.get("contact_title")
        if contact_title_search:
            queryset = queryset.filter(contact_title__icontains=contact_title_search)
        
        region_search = self.request.GET.get("region")
        if region_search:
            queryset = queryset.filter(region__exact=region_search)

        # Sorting Functionality
        sort_by = self.request.GET.get("sort", "company_name")
        sort_order = self.request.GET.get("order", "asc")

        valid_sort_fields = ['company_name', 'contact_name', 'contact_title', 'city', 'region', 'country']

        if sort_by in valid_sort_fields:
            if sort_order == "desc":
                sort_by = f"-{sort_by}"  
            queryset = queryset.order_by(sort_by)  

        return queryset

    def get_context_data(self, **kwargs):
        """Add search criteria to the context."""
        context = super().get_context_data(**kwargs)
        context["search_country"] = self.request.GET.get("country", "")
        context["search_city"] = self.request.GET.get("city", "")
        context["search_contact"] = self.request.GET.get("contact", "")
        context["search_customer"] = self.request.GET.get("customer", "")
        context["search_contact_title"] = self.request.GET.get("contact_title", "")
        context["search_region"] = self.request.GET.get("region", "")
        context["current_sort"] = self.request.GET.get("sort", "company_name")
        context["current_order"] = self.request.GET.get("order", "asc")

        # Get distinct countries for dropdown
        context["available_countries"] = Customers.get_countries()

        # Query string for sorting links
        get_params = self.request.GET.copy()
        if 'page' in get_params:
            del get_params['page']
        context["query_string"] = get_params.urlencode()

        return context


class CustomerDetailView(DetailView):
    """
    Detail view for a customer - includes their orders (Requirement 3)
    """
    model = Customers
    template_name = "DjangoTradersApp/Customers/Detail.html"
    context_object_name = "customer"
    pk_url_kwarg = "customer_id"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all orders for this customer with related data, ordered by date
        context['orders'] = self.object.orders.all().order_by('-order_date')
        context['order_count'] = self.object.get_order_count()
        return context
# endregion


# region Class-based Product views
class ProductListView(ListView):
    """Product list view for Requirement 2."""
    model = Products
    template_name = "DjangoTradersApp/Products/index.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()

        # Product Name Search
        product_name_search = self.request.GET.get("product_name")
        if product_name_search:
            queryset = queryset.filter(product_name__icontains=product_name_search)

        # Category Search (REQUIRED)
        category_search = self.request.GET.get("category")
        if category_search:
            queryset = queryset.filter(category__category_name__icontains=category_search)

        # Supplier Search
        supplier_search = self.request.GET.get("supplier")
        if supplier_search:
            queryset = queryset.filter(supplier__company_name__icontains=supplier_search)

        # Status Filter (discontinued)
        status_filter = self.request.GET.get("status")
        if status_filter == "active":
            queryset = queryset.filter(discontinued=0)
        elif status_filter == "discontinued":
            queryset = queryset.filter(discontinued=1)

        # Price Range
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        if min_price:
            try:
                queryset = queryset.filter(unit_price__gte=float(min_price))
            except ValueError:
                pass
        if max_price:
            try:
                queryset = queryset.filter(unit_price__lte=float(max_price))
            except ValueError:
                pass

        # Sorting
        sort_by = self.request.GET.get("sort", "product_name")
        sort_order = self.request.GET.get("order", "asc")

        valid_sort_fields = [
            'product_name', 
            'unit_price', 
            'category__category_name', 
            'supplier__company_name', 
            'discontinued', 
            'units_in_stock'
        ]

        if sort_by in valid_sort_fields:
            if sort_order == "desc":
                sort_by = f"-{sort_by}"
            queryset = queryset.order_by(sort_by)

        queryset = queryset.select_related('category', 'supplier')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Search values
        context["search_product_name"] = self.request.GET.get("product_name", "")
        context["search_category"] = self.request.GET.get("category", "")
        context["search_supplier"] = self.request.GET.get("supplier", "")
        context["search_status"] = self.request.GET.get("status", "")
        context["search_min_price"] = self.request.GET.get("min_price", "")
        context["search_max_price"] = self.request.GET.get("max_price", "")

        # Sort info
        context["current_sort"] = self.request.GET.get("sort", "product_name")
        context["current_order"] = self.request.GET.get("order", "asc")

        # Dropdown options
        context["available_categories"] = Categories.objects.all().order_by('category_name')
        context["available_suppliers"] = Suppliers.objects.all().order_by('company_name')

        # Query string
        get_params = self.request.GET.copy()
        if 'page' in get_params:
            del get_params['page']
        context["query_string"] = get_params.urlencode()

        return context


class ProductDetailView(DetailView):
    """Detail view for a product"""
    model = Products
    template_name = "DjangoTradersApp/Products/detail.html"
    context_object_name = "product"
    pk_url_kwarg = "product_id"
# endregion

# Order List View for index.html
 
class ProductDetailView(DetailView):
    """Detail view for a product"""
    model = Products
    template_name = "DjangoTradersApp/Products/detail.html"
    context_object_name = "product"
    pk_url_kwarg = "product_id"
# endregion


# region Order views (Requirement 3)
class OrderListView(ListView):
    """List view for all orders."""
    model = Orders
    template_name = "DjangoTradersApp/Orders/index.html"
    context_object_name = "orders"

    def get_queryset(self):
        queryset = super().get_queryset()

        # Customer search
        customer_search = self.request.GET.get("customer")
        if customer_search:
            queryset = queryset.filter(customer__company_name__icontains=customer_search)

        # Status filter
        status_filter = self.request.GET.get("status")
        if status_filter == "shipped":
            queryset = queryset.filter(shipped_date__isnull=False)
        elif status_filter == "processing":
            queryset = queryset.filter(shipped_date__isnull=True)

        # Year filter
        year_filter = self.request.GET.get("year")
        if year_filter:
            queryset = queryset.filter(order_date__year=year_filter)

        # Sorting
        sort_by = self.request.GET.get("sort", "order_date")
        sort_order = self.request.GET.get("order", "desc")

        valid_sort_fields = [
            'order_id', 
            'customer__company_name', 
            'order_date', 
            'shipped_date', 
            'freight'
        ]

        if sort_by in valid_sort_fields:
            if sort_order == "desc":
                sort_by = f"-{sort_by}"
            queryset = queryset.order_by(sort_by)

        queryset = queryset.select_related('customer')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Search values
        context["search_customer"] = self.request.GET.get("customer", "")
        context["search_status"] = self.request.GET.get("status", "")
        context["search_year"] = self.request.GET.get("year", "")

        # Sort info
        context["current_sort"] = self.request.GET.get("sort", "order_date")
        context["current_order"] = self.request.GET.get("order", "desc")

        # Available years for dropdown
        from django.db.models import functions
        years = Orders.objects.annotate(
            year=functions.ExtractYear('order_date')
        ).values_list('year', flat=True).distinct().order_by('-year')
        context["available_years"] = [year for year in years if year]

        # Query string
        get_params = self.request.GET.copy()
        if 'page' in get_params:
            del get_params['page']
        context["query_string"] = get_params.urlencode()

        return context


class OrderDetailView(DetailView):
    """Detail view for an order"""
    model = Orders
    template_name = "DjangoTradersApp/Orders/Detail.html"
    context_object_name = "order"
    pk_url_kwarg = "order_id"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Query order details manually using the order_id
        order_details = OrderDetails.objects.filter(
            order_id=self.object.order_id
        ).all()
        
        context['order_details'] = order_details
        context['order_total'] = sum(detail.line_total for detail in order_details)
        return context
# endregion