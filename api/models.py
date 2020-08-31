from django.db import models


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    text_de = models.CharField(max_length=255)
    text_en = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    grants = models.ManyToManyField(through='Requirement', to='Grant')


class QuestionType(models.Model):
    id = models.AutoField(primary_key=True)
    name_de = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_short = models.CharField(max_length=255)


class QuestionBoundary(models.Model):
    id = models.AutoField(primary_key=True)
    bool = models.BooleanField(null=True, blank=True)
    int_exact = models.IntegerField(null=True, blank=True)
    int_lt = models.IntegerField(null=True, blank=True)
    int_gt = models.IntegerField(null=True, blank=True)
    date_exact = models.DateField(null=True, blank=True)
    date_lt = models.DateField(null=True, blank=True)
    date_gt = models.DateField(null=True, blank=True)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name_de = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='category_mains')
    parent_category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='child_categories', blank=True)


class Grant(models.Model):
    id = models.AutoField(primary_key=True)
    name_de = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    questions = models.ManyToManyField(through='Requirement', to='Question')


class Requirement(models.Model):
    id = models.AutoField(primary_key=True)
    grant = models.ForeignKey('Grant', on_delete=models.CASCADE, related_name='requirements')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='requirements')


