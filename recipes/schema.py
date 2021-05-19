import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType
from recipes.models import Recipe, Comment
from django.db.models import Q

class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class Query(graphene.ObjectType):
    recipes = graphene.List(RecipeType, search=graphene.String())
    comments = graphene.List(CommentType)

    def resolve_recipes(self, info, search=None, **kwargs):
        if search:
            filter = (
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
            return Recipe.objects.filter(filter)

        return Recipe.objects.all()

    def resolve_comments(self, info, **kwargs):
        return Comment.objects.all()

class CreateRecipe(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    cuisine = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        cuisine = graphene.String()

    def mutate(self, info, title, description, cuisine):
        user = info.context.user or None
        recipe = Recipe(title=title, description=description, cuisine=cuisine, posted_by=user)
        recipe.save()

        return CreateRecipe(
            id=recipe.id,
            title=recipe.title,
            description=recipe.description,
            cuisine=recipe.cuisine,
            posted_by=recipe.posted_by,
        )

class CreateComment(graphene.Mutation):
    user = graphene.Field(UserType)
    recipe = graphene.Field(RecipeType)
    message = graphene.String()

    class Arguments:
        recipe_id = graphene.Int()
        message = graphene.String()

    def mutate(self, info, recipe_id, message):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('You must be logged to vote!')

        recipe = Recipe.objects.filter(id=recipe_id).first()
        if not recipe:
            raise Exception('Invalid Link!')

        Comment.objects.create(
            user=user,
            recipe=recipe,
            message=message
        )

        return CreateComment(user=user, recipe=recipe, message=message)

#4
class Mutation(graphene.ObjectType):
    create_recipe = CreateRecipe.Field()
    create_comment = CreateComment.Field()
