import os
from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='datasets/') # guarda el archivo en MEDIA_ROOT/datasets/ y registra nombre y fecha de carga.
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # eliminar el archivo físico al borrar
    def delete(self, *args, **kwargs):
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name