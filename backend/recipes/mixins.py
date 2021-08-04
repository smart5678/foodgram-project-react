from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response


class ActionViewSetMixin(viewsets.ModelViewSet):

    def set_action(self, request, pk=None, model_serializer=None, simple_serializer=None, model=None, recipe_model=None):
        if request.method == 'GET':
            data = {'user': request.user.id, 'favorite_recipe': pk}
            serializer = model_serializer(data=data, partial=False)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                recipe_serializer = simple_serializer(recipe_model.objects.get(id=pk), context={'request': request})
                return Response(recipe_serializer.data)
            else:
                raise serializers.ValidationError(
                    {'error': serializer.errors}
                )
        else:
            try:
                model.objects.get(user=request.user, favorite_recipe_id=pk).delete()
            except ObjectDoesNotExist:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'error': 'В избранном рецепта нет'},
                )
            return Response(status=status.HTTP_204_NO_CONTENT)