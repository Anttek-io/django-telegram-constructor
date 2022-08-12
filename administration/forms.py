from django import forms

from administration.models import Department, Position


class DepartmentCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DepartmentCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Department
        fields = ('name', )


class DepartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Department
        fields = ('name', 'parent_department', 'is_active', 'is_deleted', )


class PositionCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PositionCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Position
        fields = ('name', )


class PositionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Position
        fields = ('name', 'parent_position', 'is_active', 'is_deleted', 'is_head')
