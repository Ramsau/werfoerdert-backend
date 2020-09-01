from django.db import models


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    text_de = models.CharField(max_length=255)
    text_en = models.CharField(max_length=255)
    type = models.ForeignKey('QuestionType', on_delete=models.CASCADE, related_name='questions')
    grants = models.ManyToManyField(through='Requirement', to='Grant')


class QuestionType(models.Model):
    id = models.AutoField(primary_key=True)
    name_de = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_short = models.CharField(max_length=255)

    class Meta:
        unique_together = (('name_short', ), )


class Grant(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('Grant', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    is_grant = models.BooleanField()
    name_de = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    questions = models.ManyToManyField(through='Requirement', to='Question')
    expires = models.DateField(blank=True, null=True)


class Requirement(models.Model):
    id = models.AutoField(primary_key=True)
    grant = models.ForeignKey('Grant', on_delete=models.CASCADE, related_name='requirements')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='requirements')
    bool = models.BooleanField(null=True, blank=True)
    int_exact = models.IntegerField(null=True, blank=True)
    int_lt = models.IntegerField(null=True, blank=True)
    int_gt = models.IntegerField(null=True, blank=True)
    date_exact = models.DateField(null=True, blank=True)
    date_lt = models.DateField(null=True, blank=True)
    date_gt = models.DateField(null=True, blank=True)


