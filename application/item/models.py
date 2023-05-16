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
    ('ballad', 'Ballad'),
    ('blues', 'Blues, Rhythm\'n\'Blues'),
    ('country', 'Country'),
    ('dance', 'Dance'),
    ('disco', 'Disco polo, Party, Karaoke'),
    ('children', 'For children'),
    ('ethno', 'Ethno, Folk, World music'),
    ('jazz', 'Jazz, Swing'),
    ('carols', 'Christmas carols'),
    ('metal', 'Metal'),
    ('alternative', 'Alternative music'),
    ('electronic', 'Electronic music'),
    ('film', 'Film music'),
    ('classical', 'Classical music'),
    ('religious', 'Religious music, retreat'),
    ('new', 'New sounds'),
    ('opera', 'Opera, Operetta'),
    ('pop', 'Pop'),
    ('rap', 'Rap, Hip-Hop'),
    ('reggae', 'Reggae, Ska'),
    ('rock', 'Rock'),
    ('rock_and_roll', 'Rock\'n\'roll'),
    ('single', 'Singles'),
    ('compilations', 'Compilations'),
    ('soul', 'Soul, Funk'),
    ('synth_pop', 'Synth-pop'),
    ('other', 'Other'),
    ('sets', 'Sets, packages'),
    
)

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Categories"
        
    def __str__(self) -> str:
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name="items", on_delete=models.CASCADE, default="Vinyl")
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
    
class Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    url = models.ImageField(upload_to='item_images', null=False, blank=False)