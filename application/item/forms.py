from django import forms
from .models import Item, Image

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class ImageForm(forms.ModelForm):
    MAX_IMAGES = 6
    
    image = forms.ImageField(
        label="Images (Max 6)",
        widget=forms.ClearableFileInput(attrs={"class": INPUT_CLASSES, "multiple": True}),
    )

    class Meta:
        model = Image
        fields = ("image",)
        
    def clean_image(self):
        images = self.cleaned_data.get('image')
        if images:
            if len(images) > self.MAX_IMAGES:
                raise forms.ValidationError(f"Please select a maximum of {self.MAX_IMAGES} images.")
        return images

class NewItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['label'].required = False
        self.fields['country'].required = False
        self.fields['year'].required = False
        
    class Meta:
        model = Item
        fields = ('name', 'category', 'label', 'country', 'year', 'genre', 'condition', 'price', 'carton')
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'category': forms.Select(attrs={
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
        fields = ('name', 'category', 'label', 'country', 'year', 'genre', 'condition', 'price', 'carton')
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'category': forms.Select(attrs={
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
            'genre': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'condition': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'carton': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
        }
        