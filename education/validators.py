from rest_framework import serializers


class URLValidator:

    def __init__(self, field_name):
        self.field_name = field_name

    def __call__(self, value):
        url = dict(value).get(self.field_name)

        if url is not None and 'youtube.com' not in url:
            raise serializers.ValidationError('Видео должно быть только с YouTube')
        