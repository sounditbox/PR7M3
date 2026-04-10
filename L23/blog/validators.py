from rest_framework import serializers


def validate_content(value):
    if "fuuu" in value.lower():
        raise serializers.ValidationError("Пост содержит плохие слова.")
    return value