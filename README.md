Django Prefix Range
===================

This library adds Postgresql [prefix range](https://github.com/dimitri/prefix)
extension to Django.


Usage
-----

### Prepare your database

First thing to do is ensuring that the extension is correctly set on your database.
Create an empty migration and set the PrefixRangeExtension.

```python
from __future__ import unicode_literals
from prefixrange import PrefixRangeExtension

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0271_auto_20171019_1145'),
    ]

    operations = [
      PrefixRangeExtension(),
    ]

```

If your database does not have root access, simply create it by hand:

```postgres
$ psql -U postgres my_db -c -c "create extension prefix;"
```


### Make some prefix fields

A prefix model field is declared using a PrefixRangeField.
This field is a subclass of CharField.
If you want to index your field, you should use a GIST index provided with this
package.

```python
from django.db import models
from prefixrange import PrefixRangeField, GistIndex

class MyModel(models.Model):
    prefix = PrefixRangeModel(max_length=5)

    class Meta:
      indexes = (
          (GistIndex(fields=['prefix']), ),
      )
```


### Query the field

A *prefixes* lookup is provided to filter instances of models that prefixes
a given value.


```python
cats = MyModel.objects.create('cats')
MyModel.objects.create('dogs')

MyModel.objects.filter(prefix__prefixes='ca') == cats
```
