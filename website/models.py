from django import forms
from django.db import models

status_choices = (
    ('זומן', 'זומן'),
    ('התקבל', 'התקבל'),
    ('לא התקבל', 'לא התקבל'),
    ('הסיר מועמדות', 'הסיר מועמדות'),
    ('פסל', 'פסל'),
    ('מבדק אמינות', 'מבדק אמינות'),
    ('קבט', 'קבט'),
)

# Define choices for the 'source' field
SOURCE_CHOICES = (
    ('מעוף', 'מעוף'),
    ('פייסבוק', 'פייסבוק'),
    ('JobMaster', 'JobMaster'),
    ('חמח הראל', 'חמח הראל'),
    ('עבודה עכשיו', 'עבודה עכשיו'),
    ('JobKarov', 'JobKarov'),
    ('אתר בזק אונליין', 'אתר בזק אונליין'),
    ('פייסבוק ממומן', 'פייסבוק ממומן'),
    ('חמח', 'חמח'),
    ('רון כהן', 'רון כהן'),
    # Add more options as needed
)

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.IntegerField()
    date_of_interview = models.DateField()
    hour_of_interview = models.TimeField()
    source = models.CharField(max_length=500, choices=SOURCE_CHOICES)
    status = models.CharField(max_length=100, choices=status_choices)
    notes = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.id} {self.first_name} {self.last_name} {self.phone} {self.source} {self.status} {self.date_of_interview} {self.hour_of_interview} {self.notes}"
