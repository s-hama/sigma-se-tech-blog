from django.db.models import Count, Q

from .models import BigCategory, Tag


def common(request):
    context = {
        "big_categories": BigCategory.objects.order_by("-id"),
        "tags": Tag.objects.annotate(
            public_post_count=Count(
                "post",
                filter=Q(post__is_publick=True),
                distinct=True,
            )
        ).order_by("-public_post_count", "id"),
    }
    return context
