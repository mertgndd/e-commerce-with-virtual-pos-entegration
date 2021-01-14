from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.utils.text import slugify


class Item(models.Model):
    CATEGORY_CHOICES = (
        ('T-Shirt', 'T-Shirt'),
        ('Sweatshirt', 'Sweatshirt'),
        ('Kapisonlu', 'Kapisonlu'),
        ('Aksesuar', 'Aksesuar'),
        ('Esofman', 'Esofman')
    )

    title = models.CharField(max_length=80, verbose_name='Başlık')  # Başlık
    description = models.CharField(max_length=120, verbose_name='İçerik')  # Açıklama Yazısı
    publishing_date = models.DateTimeField(verbose_name='YayınlanmaTarihi', auto_now_add=True)  # Yayınlanma Tarihi
    urun_adedi = models.IntegerField(default=100)  # ürün adedi
    pre_fiyat = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Önceki Fiyat')
    fiyat = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    image = models.ImageField(null=False, blank=False, verbose_name='Ana Resim')
    image2 = models.ImageField(null=True, blank=True, verbose_name='İkinci Resim')
    image3 = models.ImageField(null=True, blank=True, verbose_name='Üçüncü Resim')
    image4 = models.ImageField(null=True, blank=True, verbose_name='Dördüncü Resim')
    category = models.CharField(max_length=15, null=False, blank=False, choices=CATEGORY_CHOICES)

    slug = models.SlugField(unique=True, editable=False, max_length=140)

    class Meta:
        ordering = ["-publishing_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item:detail', kwargs={'slug': self.slug})

    def get_create_url(self):
        return reverse('item:create')

    def get_update_url(self):
        return reverse('item:update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('item:delete', kwargs={'slug': self.slug})

    def get_unique_slug(self):
        slug = slugify(self.title.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while Item.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Item, self).save(*args, **kwargs)

