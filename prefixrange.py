from django.contrib.postgres import lookups
from django.contrib.postgres.operations import CreateExtension
from django.db.models import CharField, Index


class PrefixRangeExtension(CreateExtension):
    def __init__(self):
        self.name = 'prefix'


class PrefixRangeField(CharField):
    def db_type(self, connection):
        return 'prefix_range'


class GistIndex(Index):
    suffix = 'gist'
    max_name_length = 31

    def create_sql(self, model, schema_editor):
        return super(GistIndex, self).create_sql(
            model,
            schema_editor,
            using=' USING gist')


@PrefixRangeField.register_lookup
class PrefixLookup(lookups.PostgresSimpleLookup):
    lookup_name = 'prefixes'
    operator = '@>'
