from django import forms
from django.utils.translation import gettext_lazy as _

from .models import RegistrationFormField


class EventFieldsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.form_fields = kwargs.pop("form_fields")
        super().__init__(*args, **kwargs)

        for key, field in self.form_fields:

            match field["type"]:
                case RegistrationFormField.BOOLEAN_FIELD:
                    self.fields[key] = forms.BooleanField(required=False)
                case RegistrationFormField.INTERGER_FIELD:
                    self.fields[key] = forms.IntegerField(required=field["required"])
                case RegistrationFormField.DATETIME_FIELD:
                    self.fields[key] = forms.DateTimeField(required=field["required"])
                case _:  # RegistrationFormField.TEXT_FIELD
                    self.fields[key] = forms.CharField(
                        required=field["required"],
                        max_length=4096
                    )

            self.fields[key].label = field["subject"]
            self.fields[key].help_text = field["description"]
            self.fields[key].initial = field["default"]

    def is_valid(self):
        return True #TODO recouple to registration
        return super().is_valid()

    def field_values(self):
        for key in self.form_fields.items():
            yield key, self.cleaned_data.get(key)
