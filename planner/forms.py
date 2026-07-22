from django import forms
from django.contrib.auth import get_user_model

from .models import MovieNight
from movies.models import Theater

User = get_user_model()


class MovieNightForm(forms.ModelForm):

    # Invite Friends field
    invited_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        label="Invite Friends",
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = MovieNight
        fields = [
            "movie",
            "venue_type",
            "theater",
            "date",
            "time",
            "description",
            "invited_users",
        ]

        widgets = {
            "movie": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "venue_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "theater": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Invite your friends with a short message..."
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        # Get logged-in user from view
        user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        # Show theaters alphabetically
        self.fields["theater"].queryset = Theater.objects.all().order_by("name")

        # Theater optional initially
        self.fields["theater"].required = False

        # Show all users except the logged-in host
        if user:
            self.fields["invited_users"].queryset = (
                User.objects.exclude(id=user.id).order_by("username")
            )
        else:
            self.fields["invited_users"].queryset = (
                User.objects.all().order_by("username")
            )

        # Bootstrap styling
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })

    def clean(self):
        cleaned_data = super().clean()

        venue = cleaned_data.get("venue_type")
        theater = cleaned_data.get("theater")

        if venue == "Cinema" and theater is None:
            self.add_error(
                "theater",
                "Please select a theater for a cinema movie night."
            )

        if venue == "Home":
            cleaned_data["theater"] = None

        return cleaned_data