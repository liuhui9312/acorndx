from django.contrib import admin

# Register your models here.
from .models import PersonInfo
from .models import DetectInfo
from .models import ItemsInfo
from .models import SaleInfo
from .models import FinancialRecord

admin.site.register(PersonInfo)
admin.site.register(DetectInfo)
admin.site.register(ItemsInfo)
admin.site.register(SaleInfo)
admin.site.register(FinancialRecord)
