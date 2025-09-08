from django.views.generic import ListView, DetailView
from django.shortcuts import render


from .models import Customers


# Create your views here.
def home(request):

    return render(
        request=request,
        template_name="DjangoTradersApp/welcome.html",
    )

# region Function-based customer views
def CustomersList(request):
    """
    View function to display all customers.
    The context includes a list of all customer objects called customers.
    The data will be displayed in the all_customers.html template.
    """
    customers = Customers.objects.all()

    return render(
        request=request,
        template_name="DjangoTradersApp/Customers/List.html",
        context={"customers": customers},
    )


def CustomerDetail(request, customer_id):
    """
    View function to display the details of a specific customer.
    The context includes the customer object identified by customer_id.
    The data will be displayed in the customer_detail.html template.
    """
    customer = Customers.objects.get(customer_id=customer_id)
    return render(
        request=request,
        template_name="DjangoTradersApp/Customers/Detail.html",
        context={"customer": customer},
    )


# endregion Function-based customer views

# region Class-based Customer views


class CustomerListView(ListView):
    """
    View to list all customers with search functionality.
    The view uses the Customers model to retrieve and display customer data.
    The model is the set of all Customers.
    The template file returned by this ListView is "DjangoTradersApp/Customers/Index.html".
    The context variable containing the list of customers is named "customers".

    The get_queryset method is overridden to provide custom filtering based on search criteria.
    It "gets" the value of the search fields from the request.

    If the search field is not empty, then the queryset is filtered to include only those values that match the search criteria.
    Filtering uses is the Django ORM's `filter()` method
        and can lookup its values using:
        `icontains` - match any characters in the field value
         `exact` - match the exact value
         `startswith` - match values that start with the given input.

    """

    model = Customers
    template_name = "DjangoTradersApp/Customers/Index.html"
    context_object_name = "customers"

    def get_queryset(self):
        """
        Start with the default queryset and
        Get the filtered queryset based on search criteria.
        """
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

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add search criteria to the context.
        Allows template to display the current search filters.
        kwargs: The keyword arguments passed to the context.
        """
        context = super().get_context_data(**kwargs)
        context["search_country"] = self.request.GET.get("country", "")
        context["search_city"] = self.request.GET.get("city", "")
        context["search_contact"] = self.request.GET.get("contact", "")
        context["search_customer"] = self.request.GET.get("customer", "")

        # Get distinct countries for dropdown
        context["available_countries"] = Customers.get_countries()

        return context


class CustomerDetailView(DetailView):
    model = Customers
    template_name = "DjangoTradersApp/Customers/Detail.html"
    context_object_name = "customer"
    pk_url_kwarg = "customer_id"


# endregion Class-based Customer views
