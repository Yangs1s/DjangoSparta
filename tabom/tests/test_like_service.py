from django.db import IntegrityError
from django.test import TestCase

from tabom.models import Like
from tabom.models.article import Article
from tabom.models.user import User
from tabom.services.like_service import do_like, undo_like


class TestLikeService(TestCase):
    def test_a_user_can_like_an_article(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")

        # When
        like = do_like(user.id, article.id)

        # Then
        self.assertIsNotNone(like.id)
        self.assertEqual(user.id, like.user_id)
        self.assertEqual(article.id, like.article_id)

    def test_a_user_can_like_an_article_only_once(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")

        # Expect
        # like1에서는 에러가 안일어났고
        # like 2에서 일어났다.
        like1 = do_like(user.id, article.id)
        with self.assertRaises(Exception):
            like2 = do_like(user.id, article.id)

    def test_it_should_raise_exception_when_like_an_user_does_not_exist(self) -> None:

        # Given
        invalid_user_id = 9988
        article = Article.objects.create(title="test_title")

        # Expect

        with self.assertRaises(IntegrityError):
            do_like(invalid_user_id, article.id)

    def test_like_count_should_increase(self) -> None:
        # Given: User,Article을 주고
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")

        # When
        do_like(user.id, article.id)

        # Then
        article = Article.objects.get(id=article.id)
        self.assertEqual(1, article.like_set.count())

    def test_a_use_can_undo_like(self) -> None:
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")
        like = do_like(user.id, article.id)

        undo_like(user.id, article.id)

        with self.assertRaises(Like.DoesNotExist):
            Like.objects.filter(id=like.id).get()
