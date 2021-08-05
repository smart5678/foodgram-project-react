from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from rest_framework.response import Response


def set_action(
        self, request, recipe_pk,
        acted_serializer=None, response_serializer=None,
        acted_model=None, response_model=None,
        follow=None, followed=None
):
    if request.method == 'GET':
        data = {follow: request.user.id, followed: recipe_pk}
        serializer = acted_serializer(data=data, partial=False)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            recipe_serializer = response_serializer(
                response_model.objects.get(id=recipe_pk),
                context={'request': request}
            )
            return Response(recipe_serializer.data)
        else:
            raise serializers.ValidationError(detail=serializer.errors)
    else:
        try:
            filter = {follow: request.user, followed+'_id': recipe_pk}
            acted_model.objects.get(**filter).delete()
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': f'В {acted_model.__name__} связи нет'},
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
