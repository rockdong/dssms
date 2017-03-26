import xadmin

# Register your models here.

from company.models import *


xadmin.site.register(Department)
xadmin.site.register(Duty)