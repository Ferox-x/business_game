from django.db.models import QuerySet


def attributes_to_json(attributes: QuerySet):
    """Метод для формования JSON объекта из атрибутов координатора."""
    return [[attribute.id, attribute.attribute] for attribute in attributes]
