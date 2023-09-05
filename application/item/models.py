from django.contrib.auth.models import User
from django.db import models

CONDITONS = (
    ("M", "Mint (M)"),
    ("M-", "Near Mint (NM or M-)"),
    ("EX", "Excellent (EX)"),
    ("VG+", "Very Good Plus (VG+)"),
    ("VG", "Very Good (VG)"),
    ("G", "Good (G)"),
    ("F", "Fair (F)"),
)

GENRES = (
    ('Ballada', 'Ballada'),
    ('Blues, Rhythm\'n\'Blues', 'Blues, Rhythm\'n\'Blues'),
    ('Country', 'Country'),
    ('Dance', 'Dance'),
    ('Disco polo, Party, Karaoke', 'Disco polo, Party, Karaoke'),
    ('Dla dzieci', 'Dla dzieci'),
    ('Ethno, Folk, World music', 'Ethno, Folk, World music'),
    ('Jazz, Swing', 'Jazz, Swing'),
    ('Kolędy', 'Kolędy'),
    ('Metal', 'Metal'),
    ('Muzyka alternatywna', 'Muzyka alternatywna'),
    ('Muzyka elektroniczna', 'Muzyka elektroniczna'),
    ('Muzyka filmowa', 'Muzyka filmowa'),
    ('Muzyka klasyczna', 'Muzyka klasyczna'),
    ('Muzyka religijna', 'Muzyka religijna'),
    ('Nowe brzmienia', 'Nowe brzmienia'),
    ('Opera, Operetka', 'Opera, Operetka'),
    ('Pop', 'Pop'),
    ('Rap, Hip-Hop', 'Rap, Hip-Hop'),
    ('Reggae, Ska', 'Reggae, Ska'),
    ('Rock', 'Rock'),
    ('Rock\'n\'roll', 'Rock\'n\'roll'),
    ('Single', 'Single'),
    ('Składanki', 'Składanki'),
    ('Soul, Funk', 'Soul, Funk'),
    ('Synth-pop', 'Synth-pop'),
    ('Pozostałe', 'Pozostałe'),
    ('Zestawy, pakiety', 'Zestawy, pakiety'),
    
)

class Format(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255)
    format = models.ForeignKey(Format, related_name="items", on_delete=models.CASCADE, default=1)
    label = models.CharField(max_length=255, null=True, default="-")
    country = models.CharField(max_length=255, null=True, default="-")
    year = models.CharField(max_length=255, null=True, default="-")
    genre = models.CharField(choices=GENRES, default="ballad", max_length=50)
    condition = models.CharField(choices=CONDITONS, default="M-", max_length=50)
    price = models.FloatField()
    carton = models.CharField(max_length=5, default="-")
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name="items", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.carton = self.carton.upper()
        super().save(*args, **kwargs)
    
class Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    url = models.ImageField(upload_to='item_images', null=False, blank=False)
    
class FavoriteItem(models.Model):
    item_id = models.ForeignKey(Item, null=False, blank=False, on_delete=models.CASCADE)