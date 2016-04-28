from django import forms


class ExampleForm(forms.Form):
    non_blank_field = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': "Must not be blank!",
        }),
    )
