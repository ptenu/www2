from django import forms

SITUATIONS = {
    "eviction": "Eviction",
    "damage": "Damage or disrepair",
    "rent": "Problems with rent",
    "overcrowding": "Overcrowding",
    "deposit": "Deposit dispute",
    "other": "Something else",
}


class ContactForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(max_length=500, required=True)


class SupportForm(forms.Form):
    given_name = forms.CharField(required=True)
    family_name = forms.CharField(required=True)
    membership_number = forms.CharField(required=False, max_length=10)
    email = forms.EmailField(required=True)
    telephone = forms.CharField(required=False, max_length=13)
    situation = forms.MultipleChoiceField(
        required=True, widget=forms.CheckboxSelectMultiple(), choices=SITUATIONS
    )
    postcode_1 = forms.CharField(max_length=4, required=True)
    postcode_2 = forms.CharField(max_length=3, required=True)

    def __str__(self):
        string = ""
        data = self.cleaned_data
        full_name = data["given_name"] + " " + data["family_name"]

        string += f"# NAME\n  {full_name.title()}\n\n"

        if "membership_number" in data:
            mn = data["membership_number"].upper()
            string += f"# MEMBERSHIP NUMBER\n  {mn}\n\n"

        email = data["email"].lower()
        string += f"# EMAIL ADDRESS\n  {email}\n\n"

        if "tel" in data:
            tel = data["telephone"]
            string += f"# TELEPHONE\n  {tel}\n\n"

        string += f"# TAGS\n  "
        for tag in data["situation"]:
            string += f"{tag}  "

        postcode = data["postcode_1"] + " " + data["postcode_2"]
        string += f"\n\n# POSTCODE\n  {postcode.upper()}"

        return string
