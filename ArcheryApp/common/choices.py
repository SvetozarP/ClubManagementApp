from django.db import models


class FieldDistanceChoices(models.TextChoices):
    yd20 = "20 Yards", "20 Yards"
    yd30 = "30 Yards", '30 Yards'
    yd40 = "40 Yards", "40 Yards"
    yd50 = "50 Yards", "50 Yards"
    yd60 = "60 Yards", "60 Yards"
    yd80 = "80 Yards", "80 Yards"
    yd100 = "100 Yards", "100 Yards"
    m18 = "18 metres", "18 metres"
    m25 = "25 metres", "25 metres"
    m30 = "30 metres", "30 metres"
    m50 = "50 metres", "50 metres"
    m60 = "60 metres", "60 metres"
    m70 = "70 metres", "70 metres"
    m90 = "90 metres", "90 metres"