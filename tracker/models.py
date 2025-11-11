from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)
    roll_no = models.IntegerField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Performance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    score = models.FloatField()
    attendance = models.FloatField()
    term = models.CharField(max_length=50)
    date_recorded = models.DateField()

    def __str__(self):
        return f"{self.student.name} - {self.subject}"
