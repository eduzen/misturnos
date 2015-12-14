# misturnos
misturnos

Para hacer que funcione el manage.py:
- Corregir los import:

--- Calendars.py

 from django.contrib.contenttypes import generic
por
 from django.contrib.contenttypes.fields import GenericForeingKey


content_object = generic.GenericForeignKey('content_type', 'object_id')
por
content_object = GenericForeignKey('content_type', 'object_id')

--- Events.py

 from django.contrib.contenttypes import generic
por
 from django.contrib.contenttypes.fields import GenericForeingKey


content_object = generic.GenericForeignKey('content_type', 'object_id')
por
content_object = GenericForeignKey('content_type', 'object_id')
