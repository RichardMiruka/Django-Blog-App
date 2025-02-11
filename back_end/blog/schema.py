import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from blog import models


class UserType(DjangoObjectType):
    """
    GraphQL type for the Django User model.
    This type allows querying user-related data.
    """
    class Meta:
        model = get_user_model()


class AuthorType(DjangoObjectType):
    """
    GraphQL type for the Profile model.
    Represents an author profile,
    including user-related data.
    """
    class Meta:
        model = models.Profile


class PostType(DjangoObjectType):
    """
    GraphQL type for the Post model.
    Represents a blog post, including metadata
    such as title, body, publish date, and tags
    """
    class Meta:
        model = models.Post


class TagType(DjangoObjectType):
    """
    GraphQL type for the Tag model.
    Represents a tag that can be associated
    with a blog post.
    """
    class Meta:
        model = models.Tag


class Query(graphene.ObjectType):
    """
    Root Query class for GraphQL
    Defines the queries available for retrieving
    blog-related data.
    """
    all_posts = graphene.List(PostType)
    author_by_username = graphene.Field(AuthorType, username=graphene.String())
    post_by_slug = graphene.Field(PostType, slug=graphene.String())
    posts_by_author = graphene.List(PostType, username=graphene.String())
    posts_by_tag = graphene.List(PostType, tag=graphene.String())

    def resolve_all_posts(root, info):
        """
        Resolver function for the allPosts query.
        """
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .all()
        )

    def resolve_author_by_username(root, info, username):
        """
        Resolver function for the authorByUsername query.
        """
        return models.Profile.objects.select_related("user").get(
            user__username=username
        )

    def resolve_post_by_slug(root, info, slug):
        """
        Resolver function for the postBySlug query.
        """
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .get(slug=slug)
        )

    def resolve_posts_by_author(root, info, username):
        """
        Resolver function for the postsByAuthor query.
        """
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(author__user__username=username)
        )

    def resolve_posts_by_tag(root, info, tag):
        """
        Resolver function for the postsByTag query.
        """
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(tags__name__iexact=tag)
        )


schema = graphene.Schema(query=Query)
