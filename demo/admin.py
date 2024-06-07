from django.contrib import admin

# Register your models here.
from demo.models import User,Book,User,Reservation,Review,BorrowingRecord,UserViolation
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Reservation)
admin.site.register(Review)
admin.site.register(BorrowingRecord)
admin.site.register(UserViolation)
# admin.site.register(NEWTEST)
