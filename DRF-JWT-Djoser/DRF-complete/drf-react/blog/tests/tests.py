from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from blog.models import Category, Post


class CategoryModelTests(TestCase):
    def test_str_returns_name(self):
        category = Category.objects.create(name="Tech")
        self.assertEqual(str(category), "Tech")

    def test_name_max_length_constraint(self):
        # max_length is 100; construct a name of length 101
        long_name = "x" * 101
        category = Category(name=long_name)
        # full_clean should raise ValidationError for max_length
        with self.assertRaises(ValidationError):
            category.full_clean()


class PostModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="General")

    def test_defaults_and_basic_fields(self):
        now_before = timezone.now()
        post = Post.objects.create(
            category=self.category,
            title="Hello",
            excerpt="Summary",
            content="Body",
            slug="hello",
        )
        self.assertEqual(post.category, self.category)
        self.assertEqual(post.title, "Hello")
        self.assertEqual(post.excerpt, "Summary")
        self.assertEqual(post.content, "Body")
        # published default should be set to a time >= creation start
        self.assertGreaterEqual(post.published, now_before)

    def test_excerpt_can_be_null(self):
        post = Post.objects.create(
            category=self.category,
            title="No Excerpt",
            excerpt=None,
            content="Content",
            slug="no-excerpt",
        )
        self.assertIsNone(post.excerpt)

    def test_slug_unique_for_date_enforced(self):
        # Create first post with a specific published date
        published = timezone.now()
        Post.objects.create(
            category=self.category,
            title="First",
            excerpt="e1",
            content="c1",
            slug="same",
            published=published,
        )
        # Second post with same slug and same date should violate unique_for_date
        p2 = Post(
            category=self.category,
            title="Second",
            excerpt="e2",
            content="c2",
            slug="same",
            published=published,
        )
        with self.assertRaises(ValidationError):
            p2.full_clean()

    def test_slug_can_repeat_on_different_dates(self):
        day1 = timezone.now()
        day2 = day1 + timezone.timedelta(days=1)
        Post.objects.create(
            category=self.category,
            title="D1",
            excerpt="e1",
            content="c1",
            slug="dup",
            published=day1,
        )
        # Same slug but different day should be valid
        p2 = Post(
            category=self.category,
            title="D2",
            excerpt="e2",
            content="c2",
            slug="dup",
            published=day2,
        )
        # Should not raise
        p2.full_clean()
        p2.save()

    def test_title_and_slug_max_lengths(self):
        # title and slug both have max_length=100 and 250 respectively
        too_long_title = "t" * 101
        post = Post(
            category=self.category,
            title=too_long_title,
            excerpt="e",
            content="c",
            slug="ok-slug",
        )
        with self.assertRaises(ValidationError):
            post.full_clean()

        too_long_slug = "s" * 251
        post = Post(
            category=self.category,
            title="ok",
            excerpt="e",
            content="c",
            slug=too_long_slug,
        )
        with self.assertRaises(ValidationError):
            post.full_clean()
