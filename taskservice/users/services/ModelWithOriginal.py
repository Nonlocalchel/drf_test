from django.db import models


class ModelWithOriginal(models.Model):
    def __init__(self, *args, **kwargs):
        super(ModelWithOriginal, self).__init__(*args, **kwargs)
        # Store initial field values into self._original
        self._original = {}
        for field in self._meta.fields:
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
        for field in self._meta.fields:
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