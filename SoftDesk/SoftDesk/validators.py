from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CharValidator:
    def validate(self, password, user=None):
        for elemt in "[]()\/+:=,\"\'.":
            if elemt in password:
                raise ValidationError(
                    _("Votre password contient un caractère non autorisé"
                      " ( []()+:=,\"\'./ )."),
                    code='password_with_bad_char'
                )

    def get_help_text(self):
        return _(
            "Your password contain an unauthorized character "
            "( []()\/+:=,\"\'. )"
        )