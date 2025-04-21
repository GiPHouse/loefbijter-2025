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
                case RegistrationFormField.INTEGER_FIELD:
                    self.fields[key] = forms.IntegerField(required=field["required"])
                case RegistrationFormField.DATETIME_FIELD:
                    self.fields[key] = forms.DateTimeField(required=field["required"])
                case _:  # RegistrationFormField.TEXT_FIELD
                    self.fields[key] = forms.CharField(
                        required=field["required"],
                        max_length=4096,
                        widget=forms.Textarea(attrs={"class": "w-full text-base p4 border border-gray-400 rounded-md",
                                                     "rows": 5,
                                                     "placeholder": "Lorem Ipsum"}),
                    )

            self.fields[key].label = field["subject"]
            self.fields[key].help_text = field["description"]
            self.fields[key].initial = field["default"]

    def field_values(self):
        print("cleaned_data", self.cleaned_data)
        for pk, _ in self.form_fields:
            yield pk, self.data[str(pk)] #TODO Might need to be cleaned data?
