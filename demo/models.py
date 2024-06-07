from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=100)
    # age = models.IntegerField(

# class NEWTEST(models.Model):
#     name = models.CharField(max_length=100)
#     age = models.CharField(max_length=100)
class Book(models.Model):
    abstract = models.CharField(max_length=200)
    author = models.CharField(max_length=30)
    bookname = models.CharField(max_length=30)
    # price = models.FloatField()
    book_type = models.CharField(max_length=30)
    ISBN = models.CharField(max_length=30)
    num = models.IntegerField()
    image_url = models.CharField(max_length=200,default='https://media.istockphoto.com/id/1500059583/photo/telluride-colorado-in-fall-color.jpg?s=2048x2048&w=is&k=20&c=8hx5S-0JHIsaslHSOmYkFaJ66axxBFvJD0XTsoCPuC4=')

class User(models.Model):
    user_id = models.CharField(max_length=30,unique=True)
    load_name = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    # load_id = models.CharField(max_length=30)
    password= models.CharField(max_length=256)
    relation_phone = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    # staut
    STATUS_CHOICES = [
        (0, 'pending'),
        (1, '逾期'),
        (2, 'cancelled'),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    class Meta:
        unique_together = ('user','book')

class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.CharField(max_length=200, default='')
    class Meta:
        unique_together = ('user','book')
# 归还记录

class BorrowingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField()
    class Meta:
        unique_together = ('user', 'book', 'borrow_date')

    def clean(self) -> None:
        # return super().clean()
        super().clean()
        if self.return_date and self.return_date < self.borrow_date:
            raise ValidationError("Return date cannot be earlier than borrow date")

class UserViolation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    violation_description = models.TextField()
    borrow_date = models.DateTimeField()
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'book', 'borrow_date')




