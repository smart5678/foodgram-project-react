from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response


def set_action(
        self, request, recipe_pk,
        model_serializer=None,
        simple_serializer=None,
        action_model=None,
        recipe_model=None,
        follow=None,
        followed=None
):
    if request.method == 'GET':
        data = {follow: request.user.id, followed: recipe_pk}
        serializer = model_serializer(data=data, partial=False)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            recipe_serializer = simple_serializer(recipe_model.objects.get(id=recipe_pk), context={'request': request})
            return Response(recipe_serializer.data)
        else:
            raise serializers.ValidationError(
                {'error': serializer.errors}
            )
    else:
        try:
            action_model.objects.get(**{follow: request.user, followed+'_id': recipe_pk}).delete()
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': f'В {action_model.__name__} рецепта нет'},
            )
        return Response(status=status.HTTP_204_NO_CONTENT)