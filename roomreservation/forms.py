from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    

class EventForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    category = forms.CharField(max_length=50)
    capacity = forms.IntegerField()
    duration = forms.DurationField(help_text="Format: HH:MM:SS")
    weekly = forms.DateTimeField(required=False, input_formats=["%Y-%m-%d %H:%M"],
                                 widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    # Simplifying permissions to a CharField for example purposes
    permissions = forms.JSONField()

class RoomForm(forms.Form):
    name = forms.CharField(max_length=100)
    x = forms.IntegerField()
    y = forms.IntegerField()
    capacity = forms.IntegerField()
    workinghours_start = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    workinghours_end = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    permissions = forms.JSONField()
    def clean(self):
        cleaned_data = super().clean()
        workinghours_start = cleaned_data.get("workinghours_start")
        workinghours_end = cleaned_data.get("workinghours_end")
        if workinghours_start >= workinghours_end:
            raise forms.ValidationError("Start time must be before end time.")
        del cleaned_data["workinghours_start"]
        del cleaned_data["workinghours_end"]
        cleaned_data["workinghours"] = (workinghours_start, workinghours_end)
        return cleaned_data
    
class ReserveForm(forms.Form):
    room = forms.IntegerField()
    event = forms.IntegerField()
    start = forms.DateTimeField(required=False, input_formats=["%Y-%m-%d %H:%M"],
                                 widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    

class QueryForm(forms.Form):
    title = forms.CharField(max_length=100)
    category = forms.CharField(max_length=50)
    start = forms.DateTimeField(required=False, input_formats=["%Y-%m-%d %H:%M"],
                                    widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end = forms.DateTimeField(required=False, input_formats=["%Y-%m-%d %H:%M"],
                                    widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    rectangle_x1 = forms.IntegerField()
    rectangle_y1 = forms.IntegerField()
    rectangle_x2 = forms.IntegerField()
    rectangle_y2 = forms.IntegerField()
    def clean(self):
        cleaned_data = super().clean()
        rectangle_x1 = cleaned_data.get("rectangle_x1")
        rectangle_y1 = cleaned_data.get("rectangle_y1")
        rectangle_x2 = cleaned_data.get("rectangle_x2")
        rectangle_y2 = cleaned_data.get("rectangle_y2")
        if rectangle_x1 >= rectangle_x2 or rectangle_y1 >= rectangle_y2:
            raise forms.ValidationError("Invalid rectangle.")
        del cleaned_data["rectangle_x1"]
        del cleaned_data["rectangle_y1"]
        del cleaned_data["rectangle_x2"]
        del cleaned_data["rectangle_y2"]
        cleaned_data["rectangle"] = ((rectangle_x1, rectangle_y1), (rectangle_x2, rectangle_y2))
        return cleaned_data
    
class ViewForm(forms.Form):
    start = forms.DateTimeField(required=False, input_formats=["%Y-%m-%d %H:%M"],
                                    widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end = forms.DateTimeField(required=False, input_formats=["%Y-%m-%d %H:%M"],
                                    widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    
