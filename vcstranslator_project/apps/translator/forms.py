from django import forms

from translator.models import TranslationFeedback
from translator.utils import Translator


class TranslationForm(forms.Form):
    command = forms.CharField(initial="command (e.g svn commit)...")

    def clean_command(self):
        value = self.cleaned_data["command"]
        parts = value.split()
        if parts[0] not in Translator.vcs:
            raise forms.ValidationError("Command must start with a valid VCS (%s)." %
                ", ".join(Translator.vcs)
            )
        return value

    def get_data(self):
        assert self.is_valid()
        return {
            "source": self.cleaned_data["command"].split()[0],
            "command": self.cleaned_data["command"],
        }

    def translate(self):
        assert self.is_valid()
        data = self.cleaned_data
        command, rest = data["command"].split(" ", 1)
        base_command = command.split()[0]
        translations = {}
        for vcs in Translator.vcs.keys():
            translations[vcs] = Translator(base_command, vcs).translate(rest)
        return translations


class TranslationFeedbackForm(forms.ModelForm):
    command = forms.CharField()

    class Meta:
        model = TranslationFeedback
