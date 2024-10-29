from django.core.exceptions import ValidationError

from services.ValidationErrorsCollector import ValidationErrorsCollector


class SelfCleaningMixin:
    """Модель которая запускает метод save перед сохранением"""

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class SelfValidationMixin(SelfCleaningMixin):
    """Модель которая запускает заданные функции валидации перед сохранением"""

    error_collector: ValidationErrorsCollector = ValidationErrorsCollector
    validators: list = []

    def clean(self):
        error_collector = self.error_collector()
        error_collector.validators = self.validators
        errors = error_collector.collect_errors(self)
        if errors:
            raise ValidationError(errors)

        return super().clean()


class WithOriginalMixin:  # class ModelWithOriginal(models.Model)
    """Сохраняет пердедущие значения полей экземпляра модели"""

    @classmethod
    def get_model_fields(cls) -> list:
        """Get fields of model"""
        return list(cls._meta.fields)

    def __init__(self, *args, **kwargs):
        super(WithOriginalMixin, self).__init__(*args, **kwargs)
        # Store initial field values into self._original
        self._original = {}
        for field in self.get_model_fields():
            try:
                # for foreign keys save in _original field_id instead of field name
                # this is for reducing database hits
                if hasattr(self, field.name + '_id'):
                    fname = field.name + '_id'
                else:
                    fname = field.name
                self._original[fname] = getattr(self, fname)
            except:  # DoesNotExist
                self._original[field.name] = None

    def _get_changed_fields(self):
        changed = []
        for field in self.get_model_fields():
            if hasattr(self, field.name + '_id'):
                fname = field.name + '_id'
            else:
                fname = field.name
            if self._original[fname] != getattr(self, fname):
                changed.append(fname)
        return changed

    def _get_original(self):
        return self._original

    changed_fields = property(_get_changed_fields)
    original = property(_get_original)

    class Meta:
        abstract = True


class FieldTrackerMixin(WithOriginalMixin):
    def has_changed(self, field):
        if field in self.changed_fields and self.pk is not None:
            return True

        return False

    def previous(self, field):
        return self.original[field]


class GetFieldRelatedNameMixin:

    def get_related_field_name(self, field):
        fields_meta = self._meta.fields
        for field_meta in fields_meta:
            field_name = field_meta.name
            if field_name == field:
                return field_meta._related_name

        raise Exception(f'Field with name {field} is not found(')
