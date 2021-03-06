from datetime import datetime

from pymongo import IndexModel

from app import mongodb as db, ma


class Base(db.Model):
    """
     Define a base model for other database tables to inherit
    """

    __abstract__ = True

    date_created = db.fields.DateTimeField(required=True,
                                           default=datetime.now())
    date_modified = db.fields.DateTimeField(required=True, 
                                            default=datetime.now())


class Item(Base):
    """
    Define an Item model
    """
    __tablename__ = "product_item"

    name = db.fields.CharField(required=True)
    price = db.fields.IntegerField(required=True)

    filter_list = ['name', 'price']

    class Meta:
        # example to have a field ensuring unique value 'name'
        indexes = [IndexModel([('name', 1)], unique=True)]
        collection_name = "product_item"

    def save(self, *args, **kwargs) -> None:
        """
        Override default save to add required fields
        :param args: Additional arguments passed
        :param kwargs: Additional arguments passed in key=value format
        :return: None
        """
        self.date_modified = datetime.now()
        super(Item, self).save(*args, **kwargs)

    def __repr__(self):
        return "<Item %r>" % self.name


class ItemSchema(ma.Schema):
    """
    Defined Item Schema
    """
    class Meta:
        model = Item
        fields = ('id', 'name', 'price', 'date_created', 'date_modified')


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
