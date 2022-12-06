from peewee import *

class LibraryModel(Model):
    id = PrimaryKeyField(null=False)
    title = CharField(max_length=100)
    year = IntegerField()
    author = CharField(max_length=100)

    class Meta:
        db_table = "library"
        order_by = ("id",)
