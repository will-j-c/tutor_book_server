from django.contrib import admin
import sys, inspect
from .models import *
# Register your models here.
class_list = inspect.getmembers(sys.modules[__name__], inspect.isclass)

for class_tuple in class_list:
    try: 
        admin.site.register(class_tuple[1]) 
    except:
        pass
