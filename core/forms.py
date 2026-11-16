
from django import forms
from django.core.exceptions import ValidationError

from .models import PesanMasuk


class PesanMasukForm(forms.ModelForm):
    class Meta:
        model = PesanMasuk
        fields = [
            field.name
            for field in PesanMasuk._meta.fields
            if (
                field.editable
                and not field.primary_key
                and field.get_internal_type()
                in ("CharField", "TextField", "EmailField", "URLField")
                and not field.choices
            )
        ]

    def clean_pesan(self):
        pesan = self.cleaned_data.get("pesan", "").strip()

        if len(pesan) < 10:
            raise ValidationError(
                "Pesan minimal harus terdiri dari 10 karakter."
            )

        return pesan
