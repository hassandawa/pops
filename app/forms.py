########################################
# app\forms.py
########################################
from django import forms
from .models import District, Market, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'district', 'market', 'price']
        widgets = {
            'district': forms.Select(attrs={'class': 'form-control'}),
            'market': forms.Select(attrs={'class': 'form-control'}),
        }

class FilterForm(forms.Form):
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        empty_label="All Districts",
        required=False
    )
    market = forms.ModelChoiceField(
        queryset=Market.objects.all(),
        empty_label="All Markets",
        required=False
    )
    date = forms.DateField(required=False)
    month = forms.CharField(max_length=2, required=False)
    year = forms.CharField(max_length=4, required=False)
    product = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add "All" options dynamically for districts and markets
        self.fields['district'].choices = [("", "All Districts")] + [
            (district.name, district.name) for district in District.objects.all()
        ]
        self.fields['market'].choices = [("", "All Markets")] + [
            (market.name, market.name) for market in Market.objects.all()
        ]

