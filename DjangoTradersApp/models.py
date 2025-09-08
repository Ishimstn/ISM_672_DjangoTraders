from django.db import models


class Customers(models.Model):

    # region Customer Fields from Database.
    customer_id = models.CharField(primary_key=True, max_length=5)
    company_name = models.CharField(max_length=40)
    contact_name = models.CharField(max_length=30, blank=True, null=True)
    contact_title = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    region = models.CharField(max_length=15, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    phone = models.CharField(max_length=24, blank=True, null=True)
    fax = models.CharField(max_length=24, blank=True, null=True)
    password = models.CharField(
        db_column="Password", max_length=64, blank=True, null=True
    )
    # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "customers"

    # endregion

    # Added Model Methods
    def __str__(self):
        """
        String representation of the Customer object.
        An f-string is a string formatting method .
        It allows embedding expressions directly inside strings
        using the f prefix and placing variables or expressions
        inside curly braces {}.

        This __str__ function
        returns the company and contact names using the f-string:
        """
        return f"Company: {self.company_name} [Contact: {self.contact_name}]"

    def get_full_address(self):
        """
        Returns the full address of the customer by concatenating
        the address, city, region, postal code, and country.
        """
        return f"{self.address}, {self.city}, {self.region}, {self.postal_code}, {self.country}"

    @classmethod
    def get_countries(cls):
        """
        Returns a list of all unique countries from the customer records.
        All the countries in this list will be from the current records.

        classmethod: A Member method - a method that is bound to the class and not the instance.
        cls: The class itself. The data type is <class 'DjangoTradersApp.models.Customers'>

        """
        countries = (
            cls.objects.values_list("country", flat=True).distinct().order_by("country")
        )
        return countries
