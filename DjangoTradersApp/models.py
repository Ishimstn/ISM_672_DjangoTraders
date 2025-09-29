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

    class Meta:
        managed = False
        db_table = "customers"

    # endregion

    # Added Model Methods
    def __str__(self):
        """String representation of the Customer object."""
        return f"Company: {self.company_name} [Contact: {self.contact_name}]"

    def get_full_address(self):
        """Returns the full address of the customer."""
        return f"{self.address}, {self.city}, {self.region}, {self.postal_code}, {self.country}"

    @classmethod
    def get_countries(cls):
        """Returns a list of all unique countries from the customer records."""
        countries = (
            cls.objects.values_list("country", flat=True).distinct().order_by("country")
        )
        return countries
    
    def get_order_count(self):
        """Get number of orders for this customer"""
        return self.orders.count()
    
    def get_total_spent(self):
        """Calculate total amount spent by this customer"""
        total = 0
        for order in self.orders.all():
            total += order.get_order_total()
        return total


# Added in Product Models & Model Methods
class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=15)
    description = models.TextField(blank=True, null=True)
    picture = models.BinaryField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = "categories"
    
    def __str__(self):
        return self.category_name


class Suppliers(models.Model):
    supplier_id = models.AutoField(primary_key=True)
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
    homepage = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = "suppliers"
    
    def __str__(self):
        return self.company_name


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=40)
    supplier = models.ForeignKey(
        Suppliers, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        db_column='supplier_id'
    )
    category = models.ForeignKey(
        Categories, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        db_column='category_id'
    )
    quantity_per_unit = models.CharField(max_length=20, blank=True, null=True)
    unit_price = models.DecimalField(
        max_digits=10, 
        decimal_places=4, 
        blank=True, 
        null=True
    )
    units_in_stock = models.SmallIntegerField(blank=True, null=True)
    units_on_order = models.SmallIntegerField(blank=True, null=True)
    reorder_level = models.SmallIntegerField(blank=True, null=True)
    discontinued = models.IntegerField(default=0)
    
    class Meta:
        managed = False
        db_table = "products"
    
    def __str__(self):
        return f"{self.product_name} - ${self.unit_price}"
    
    @property
    def status_display(self):
        """Returns user-friendly status text"""
        return "Discontinued" if self.discontinued == 1 else "Active"
    
    @property
    def status_class(self):
        """Returns CSS class for styling"""
        return "discontinued" if self.discontinued else "active"
    
    @classmethod
    def get_categories(cls):
        """Get all unique categories for dropdown"""
        return Categories.objects.all().order_by('category_name')


# Orders Model - Requirement 3
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        Customers, 
        on_delete=models.CASCADE, 
        related_name='orders',
        db_column='customer_id'
    )
    employee_id = models.IntegerField(blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    required_date = models.DateTimeField(blank=True, null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    ship_via = models.IntegerField(blank=True, null=True)
    freight = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    ship_name = models.CharField(max_length=40, blank=True, null=True)
    ship_address = models.CharField(max_length=60, blank=True, null=True)
    ship_city = models.CharField(max_length=15, blank=True, null=True)
    ship_region = models.CharField(max_length=15, blank=True, null=True)
    ship_postal_code = models.CharField(max_length=10, blank=True, null=True)
    ship_country = models.CharField(max_length=15, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = "orders"
    
    def __str__(self):
        return f"Order #{self.order_id}"
    
    def get_order_total(self):
        """Calculate total for this order"""
        total = sum(detail.line_total for detail in self.order_details.all())
        return total


# OrderDetails Model - Requirement 3
class OrderDetails(models.Model):
    order_id = models.IntegerField(primary_key=True)
    product_id = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=4)
    quantity = models.SmallIntegerField()
    discount = models.FloatField()
    
    class Meta:
        managed = False
        db_table = "order_details"
    
    @property
    def order(self):
        """Get the related order"""
        return Orders.objects.get(order_id=self.order_id)
    
    @property
    def product(self):
        """Get the related product"""
        return Products.objects.get(product_id=self.product_id)
    
    def __str__(self):
        return f"Order {self.order_id} - Product {self.product_id}"
    
    @property
    def line_total(self):
        """Calculate line item total with discount applied"""
        base_total = float(self.unit_price) * self.quantity
        discount_amount = base_total * self.discount
        return base_total - discount_amount