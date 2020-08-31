from django.db import models

class Test(models.Model):
    short = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CourseSite(models.Model):
    short = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=1024)
    token = models.CharField(max_length=1024)
    active_tests = models.ManyToManyField(Test)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    student_id = models.CharField(max_length=32)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Question(models.Model):
    EVALUATE = 'Evaluate'
    FINAL_VALUE = 'Final value'
    EQUIVALENT_CODE = 'Equivalent code'
    PRINTED_OUTPUT = 'Printed output'
    QUESTION_TYPE_CHOICES = [
        (EVALUATE, 'Evaluate'),
        (FINAL_VALUE, 'Final value'),
        (EQUIVALENT_CODE, 'Equivalent code'),
        (PRINTED_OUTPUT, 'Printed output'),
    ]

    question_type = models.CharField(
        max_length=16,
        choices=QUESTION_TYPE_CHOICES,
        default=FINAL_VALUE,
    )
    repeat = models.PositiveSmallIntegerField()
    template = models.TextField()
    question_override = models.CharField(max_length=1024, null=True, blank=True, default=None)
    final_value_variable = models.CharField(max_length=64, null=True, blank=True, default=None)
    test = models.ForeignKey(Test, on_delete=models.RESTRICT)
    active = models.BooleanField(default=True)
    order = models.SmallIntegerField(default=0)

    def __str__(self):
        return str(self.test) + ': order ' + str(self.order)

class Attempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    test = models.ForeignKey(Test, on_delete=models.RESTRICT)
    course_site = models.ForeignKey(CourseSite, on_delete=models.RESTRICT)
    token = models.CharField(max_length=1024)
    questions = models.PositiveSmallIntegerField(default=0)
    correct_answers = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.student) + ' ' + str(self.test)
