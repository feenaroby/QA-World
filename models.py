from datetime import timezone


from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField

# Create your models here.
class user(models.Model):
    #id=models.AutoField(primary_key=True,)

    f_name = models.CharField(max_length=30)
    l_name = models.CharField(max_length=30)
    mobile = models.IntegerField()
    email = models.EmailField(max_length=30,unique=True)
    password = models.CharField(max_length=30)
    gender = models.CharField(max_length=10,default='Female')
    status= models.IntegerField(default=1)
    credit_balance=models.IntegerField(default=0)
    type = models.CharField(max_length=10,default="user")


    def __str__(self):
       return (self.f_name)
class expert_tbl(models.Model):
     # id=models.AutoField(primary_key=True,)


    f_name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=30)
    cat = models.CharField(max_length=30)
    interest = models.CharField(max_length=20)
    email = models.EmailField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    status = models.IntegerField(default=0)
    rating=models.IntegerField(default=50)
    fileToUpload = models.FileField(upload_to='e_proof/%m',null=False)
    type = models.CharField(max_length=10, default="expert")
    count=models.IntegerField(default=0)
    payment_received=models.IntegerField(default=0)
    payment_pending = models.IntegerField(default=0)
    payment_status = models.IntegerField(default=0)
    def __str__(self):
      return (self.f_name)





def validate_date(date):
        if date < date.today():
            raise ValidationError("Date cannot be in the past")


class question(models.Model):

    person = models.ForeignKey("user", on_delete=models.CASCADE)
    categry = models.ForeignKey("categry", on_delete=models.CASCADE)
    question = RichTextField()
    rating=models.IntegerField(default=1)
    e_date= models.DateField(blank=True, null=True, verbose_name="expected date",validators=[validate_date])
    question_status=models.IntegerField(default=0)
    review = models.CharField(max_length=400, default="empty")
    expert=models.CharField(max_length=50,null=True)

    def __str__(self):
        return (self.question)



class Pending(models.Model):
    expert = models.ForeignKey("expert_tbl",on_delete=models.CASCADE )
    question=models.ForeignKey("question", on_delete=models.CASCADE)
    status=models.IntegerField(default=1)

    def __str__(self):
        return (self.question.question)


class categry(models.Model):
    cat=models.CharField(max_length=30, unique=True,validators=[RegexValidator('^[A-Z ]*$',
                               'Only uppercase letters  allowed.')])

    def __str__(self):
        return (self.cat)


class subcategory(models.Model):
    categry=models.ForeignKey("categry",on_delete=models.CASCADE)
    subcat=models.CharField(max_length=30, unique=True)

    def __str__(self):
        return (self.subcat)

class tbl_answer(models.Model):
    pending=models.ForeignKey("Pending",on_delete=models.CASCADE)
    # answer=RichTextField(blank=True,null=True)
    answer=models.CharField(max_length=1500, null=True)
    review = models.CharField(max_length=400, null=True)
    status=models.IntegerField(default=0)

class tbl_chat(models.Model):
    public=models.ForeignKey("user",on_delete=models.CASCADE)
    expert=models.ForeignKey("expert_tbl",on_delete=models.CASCADE)
    question=models.ForeignKey("Pending",on_delete=models.CASCADE)
    msg=models.CharField(max_length=1500, null=True)
    person=models.CharField(max_length=50, null=False)
    status=models.IntegerField(default=1)







