from tarfile import TruncatedHeaderError

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class Address(models.Model):
    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)

    def full_address(self):
        return f"{self.street}, {self.postal_code}, {self.city}"

    def __str__(self):
        return self.full_address()

    class Meta:
        verbose_name_plural = "Address Entries"


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


class Book(models.Model):
    title = models.CharField(max_length=50)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    # author = models.CharField(null=True, max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name="books")
    is_bestselling = models.BooleanField(default=False)
    slug = models.SlugField(default="", null=False, db_index=True)  # Harry Potter 1 => harry-potter-1
    published_countries = models.ManyToManyField(Country, null=False)

    # def get_absolute_url(self):
    #     return reverse("book_detail", args=[self.id])  # version1 without slug, but with id
    def get_absolute_url(self):
        return reverse("book_detail", args=[self.slug])

    # Harry Potter 1 => harry-potter-1 This function can be deleted when in the admin.py file you prepopulated the
    # field in the admin interface for adding a book, but I'll not delete for now to maintain also the python manage.py shell method.
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.rating})"

# # MODELS CHINOOK AND NORTHWIND WITH ADJUSTMENTS
# class ChinookAlbum(models.Model):
#     albumid = models.IntegerField(primary_key=True)
#     title = models.CharField(max_length=160)
#     artistid = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'Album'
#         # app_label = 'chinook_app'  # Needed for the db router
#
# class NorthwindProducts(models.Model):
#     productid = models.IntegerField(db_column='ProductID', primary_key=True)
#     productname = models.TextField(db_column='ProductName')
#     supplierid = models.ForeignKey('Suppliers', models.DO_NOTHING, db_column='SupplierID', blank=True, null=True)
#     categoryid = models.ForeignKey('Categories', models.DO_NOTHING, db_column='CategoryID', blank=True, null=True)
#     quantityperunit = models.TextField(db_column='QuantityPerUnit', blank=True, null=True)
#     unitprice = models.DecimalField(db_column='UnitPrice', max_digits=10, decimal_places=2)
#     unitsinstock = models.IntegerField(db_column='UnitsInStock', blank=True, null=True)
#     unitsonorder = models.IntegerField(db_column='UnitsOnOrder', blank=True, null=True)
#     reorderlevel = models.IntegerField(db_column='ReorderLevel', blank=True, null=True)
#     discontinued = models.TextField(db_column='Discontinued')
#
#     class Meta:
#         managed = False
#         db_table = 'Products'
#         # app_label = 'northwind_app'  # Needed for the db router
#
# class Suppliers(models.Model):
#     supplierid = models.IntegerField(db_column='SupplierID', primary_key=True)
#     companyname = models.TextField(db_column='CompanyName')
#     contactname = models.TextField(db_column='ContactName')
#     contacttitle = models.TextField(db_column='ContactTitle')
#     address = models.TextField(db_column='Address')
#     city = models.TextField(db_column='City')
#     region = models.TextField(db_column='Region')
#     postalcode = models.TextField(db_column='PostalCode')
#     country = models.TextField(db_column='Country')
#     phone = models.TextField(db_column='Phone')
#     fax = models.TextField(db_column='Fax')
#     homepage = models.TextField(db_column='HomePage')
#
#     class Meta:
#         managed = False
#         db_table = 'Suppliers'
#
# class Categories(models.Model):
#     categoryid = models.IntegerField(db_column='CategoryID', primary_key=True)
#     categoryname = models.TextField(db_column='CategoryName')
#     description = models.TextField(db_column='Description')
#     picture = models.BinaryField(db_column='Picture')
#
#     class Meta:
#         managed = False
#         db_table = 'Categories'


# MODELS CHINOOK AND NORTHWIND WITH COPY-PASTE

class ChinookAlbum(models.Model):
    albumid = models.AutoField(db_column='AlbumId', primary_key=True)  # Field name made lowercase.
    title = models.TextField(db_column='Title')  # Field name made lowercase. This field type is a guess.
    artistid = models.ForeignKey('Artist', models.DO_NOTHING, db_column='ArtistId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Album'


class Artist(models.Model):
    artistid = models.AutoField(db_column='ArtistId', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True,
                            null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Artist'

class NorthwindProducts(models.Model):
    productid = models.AutoField(db_column='ProductID', primary_key=True)  # Field name made lowercase.
    productname = models.TextField(db_column='ProductName')  # Field name made lowercase.
    supplierid = models.ForeignKey('NorthwindSuppliers', models.DO_NOTHING, db_column='SupplierID', blank=True, null=True)  # Field name made lowercase.
    categoryid = models.ForeignKey('NorthwindCategories', models.DO_NOTHING, db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    quantityperunit = models.TextField(db_column='QuantityPerUnit', blank=True, null=True)  # Field name made lowercase.
    unitprice = models.TextField(db_column='UnitPrice', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    unitsinstock = models.IntegerField(db_column='UnitsInStock', blank=True, null=True)  # Field name made lowercase.
    unitsonorder = models.IntegerField(db_column='UnitsOnOrder', blank=True, null=True)  # Field name made lowercase.
    reorderlevel = models.IntegerField(db_column='ReorderLevel', blank=True, null=True)  # Field name made lowercase.
    discontinued = models.TextField(db_column='Discontinued')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Products'

class NorthwindCategories(models.Model):
    categoryid = models.AutoField(db_column='CategoryID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    categoryname = models.TextField(db_column='CategoryName', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    picture = models.BinaryField(db_column='Picture', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Categories'

class NorthwindSuppliers(models.Model):
    supplierid = models.AutoField(db_column='SupplierID', primary_key=True)  # Field name made lowercase.
    companyname = models.TextField(db_column='CompanyName')  # Field name made lowercase.
    contactname = models.TextField(db_column='ContactName', blank=True, null=True)  # Field name made lowercase.
    contacttitle = models.TextField(db_column='ContactTitle', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    city = models.TextField(db_column='City', blank=True, null=True)  # Field name made lowercase.
    region = models.TextField(db_column='Region', blank=True, null=True)  # Field name made lowercase.
    postalcode = models.TextField(db_column='PostalCode', blank=True, null=True)  # Field name made lowercase.
    country = models.TextField(db_column='Country', blank=True, null=True)  # Field name made lowercase.
    phone = models.TextField(db_column='Phone', blank=True, null=True)  # Field name made lowercase.
    fax = models.TextField(db_column='Fax', blank=True, null=True)  # Field name made lowercase.
    homepage = models.TextField(db_column='HomePage', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Suppliers'

