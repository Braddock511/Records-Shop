from django import forms
from .models import Item

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, required=False, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        else:
            return single_file_clean(data, initial)


class FileFieldForm(forms.Form):
    images = MultipleFileField()

class NewItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['label'].required = False
        self.fields['country'].required = False
        self.fields['year'].required = False
        
    class Meta:
        model = Item
        fields = ('name', 'format', 'label', 'country', 'year', 'genre', 'condition', 'price', 'carton')
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'format': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'label': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                "placeholder": "-"
            }),
            'country': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                "placeholder": "-",
            }),
            'year': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                "placeholder": "-"
            }),
            'genre': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'condition': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'carton': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
        }
        
class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'format', 'label', 'country', 'year', 'genre', 'condition', 'price', 'carton')
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'format': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'label': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                "required": False
            }),
            'country': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                "required": False
            }),
            'year': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                "required": False
            }),
            'genre': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'condition': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'carton': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
        }

class EditItemsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].required = False
        self.fields['carton'].required = False
        
    class Meta:
        model = Item
        fields = ('price', 'carton')
        
        widgets = {
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'carton': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
        }
  