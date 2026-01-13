# content/forms.py
from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["name", "category", "body"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full border rounded px-2.5 py-2 text-sm",
                    "placeholder": "空欄で匿名",
                }
            ),
            "category": forms.Select(
                attrs={"class": "w-full border rounded px-2.5 py-2 text-sm"},
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "w-full border rounded px-2.5 py-2 text-sm",
                    "rows": 6,
                    "placeholder": "相談・意見・要望など、なんでも自由に書いてください。",
                }
            ),
        }
        labels = {
            "name": "お名前",
            "category": "カテゴリ",
            "body": "内容",
        }
