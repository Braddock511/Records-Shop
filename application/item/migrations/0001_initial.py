# Generated by Django 4.2 on 2023-05-15 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name_plural": "Categories",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("label", models.CharField(default="-", max_length=255, null=True)),
                ("country", models.CharField(default="-", max_length=255, null=True)),
                ("year", models.CharField(default="-", max_length=255, null=True)),
                (
                    "genre",
                    models.CharField(
                        choices=[
                            ("ballad", "Ballad"),
                            ("blues", "Blues, Rhythm'n'Blues"),
                            ("country", "Country"),
                            ("dance", "Dance"),
                            ("disco", "Disco polo, Party, Karaoke"),
                            ("children", "For children"),
                            ("ethno", "Ethno, Folk, World music"),
                            ("jazz", "Jazz, Swing"),
                            ("carols", "Christmas carols"),
                            ("metal", "Metal"),
                            ("alternative", "Alternative music"),
                            ("electronic", "Electronic music"),
                            ("film", "Film music"),
                            ("classical", "Classical music"),
                            ("religious", "Religious music, retreat"),
                            ("new", "New sounds"),
                            ("opera", "Opera, Operetta"),
                            ("pop", "Pop"),
                            ("rap", "Rap, Hip-Hop"),
                            ("reggae", "Reggae, Ska"),
                            ("rock", "Rock"),
                            ("rock_and_roll", "Rock'n'roll"),
                            ("single", "Singles"),
                            ("compilations", "Compilations"),
                            ("soul", "Soul, Funk"),
                            ("synth_pop", "Synth-pop"),
                            ("other", "Other"),
                            ("sets", "Sets, packages"),
                        ],
                        default="ballad",
                        max_length=50,
                    ),
                ),
                (
                    "condition",
                    models.CharField(
                        choices=[
                            ("M", "Mint (M)"),
                            ("M-", "Near Mint (NM or M-)"),
                            ("EX", "Excellent (EX)"),
                            ("VG+", "Very Good Plus (VG+)"),
                            ("VG", "Very Good (VG)"),
                            ("G", "Good (G)"),
                            ("F", "Fair (F)"),
                        ],
                        default="M-",
                        max_length=50,
                    ),
                ),
                ("price", models.FloatField()),
                ("carton", models.CharField(default="-", max_length=5)),
                ("is_sold", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "category",
                    models.ForeignKey(
                        default="Vinyl",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="item.category",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="")),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="item.item"
                    ),
                ),
            ],
        ),
    ]
