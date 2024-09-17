class SelfCleaningModel:
    """Модель которая запускает проерки перед сохранением"""

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

