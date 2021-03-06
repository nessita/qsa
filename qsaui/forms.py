from __future__ import unicode_literals

from django import forms

from tvdbpy import TvDB


UPDATE_CHOICES = [
    (TvDB.DAY, 'Last day'),
    (TvDB.WEEK, 'Last week'),
    (TvDB.MONTH, 'Last month'),
    (TvDB.ALL, 'All series'),
]


class UpdateCatalogueForm(forms.Form):

    period = forms.ChoiceField(
        required=True, choices=UPDATE_CHOICES, initial=TvDB.WEEK)
