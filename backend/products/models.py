from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=1, related_name='products')
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=15, default=99.99)

    @property
    def sale_price(self):
        return "%.2f" %(float(self.price) * 0.8)

    def get_discount(self):
        return "122"