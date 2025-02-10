from django.db import models
from django.conf import settings


class Profile(models.Model):
    """
    Represents a user profile with additional information
    such as website and bio.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    website = models.URLField(blank=True)
    bio = models.CharField(max_length=240, blank=True)

    def __str__(self):
        """
        Returns the username associated with this profile.
        """
        return self.user.get_username()


class Tag(models.Model):
    """
    Represents a tag that can be associated with posts.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """
        Returns the name of the tag.
        """
        return self.name


class Post(models.Model):
    """
    Represents a blog post with metadata such as title, body,
    and publication status.
    """
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    body = models.TextField()
    meta_description = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ["-publish_date"]

    def __str__(self):
        """
        Returns the title of the post.
        """
        return self.title
