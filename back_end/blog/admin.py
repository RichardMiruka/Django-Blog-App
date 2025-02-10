from django.contrib import admin
from blog.models import Profile, Tag, Post


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Profile model.
    """
    model = Profile
    list_display = ("user", "website", "bio")
    search_fields = ("user__username", "bio")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Tag model.
    """
    model = Tag
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Post model.
    """
    model = Post

    list_display = (
        "id",
        "title",
        "subtitle",
        "slug",
        "publish_date",
        "published",
    )
    list_filter = ("published", "publish_date")

    list_editable = ("subtitle", "slug", "publish_date", "published")

    search_fields = ("title", "subtitle", "slug", "body")

    prepopulated_fields = {
        "slug": ("title",)
    }

    date_hierarchy = "publish_date"
    save_on_top = True
