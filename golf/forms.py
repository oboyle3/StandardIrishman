from django import forms
from .models import Golfer

class FavoritesForm(forms.Form):
    golfers = forms.ModelMultipleChoiceField(
        queryset=Golfer.objects.order_by('name'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Choose up to 5 favorite golfers"
    )

    def clean_golfers(self):
        golfers = self.cleaned_data.get('golfers')
        if golfers and len(golfers) > 5:
            raise forms.ValidationError("You can select at most 5 favorite golfers.")
        return golfers
