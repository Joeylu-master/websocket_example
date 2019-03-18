from foo.models import Foo
from rest_framework import serializers




class FooSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foo
        fields = ('bar',)
