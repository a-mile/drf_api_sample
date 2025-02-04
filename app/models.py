from django.db import models

class Study(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
    

class Assay(models.Model):
    measurement_type = models.CharField(max_length=255)
    study = models.ForeignKey(Study, related_name='assays', on_delete=models.CASCADE)

    def __str__(self):
        return self.name