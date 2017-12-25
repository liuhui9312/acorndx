from django.contrib import admin

# Register your models here.
from .models import PersonInfo
from .models import ItemsInfo
from .models import SaleInfo
from .models import FinancialRecord

admin.site.register(PersonInfo)
admin.site.register(ItemsInfo)
admin.site.register(SaleInfo)
admin.site.register(FinancialRecord)
