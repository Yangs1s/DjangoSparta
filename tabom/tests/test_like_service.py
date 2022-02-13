from django.test import TestCase

from tabom.models.article import Article
from tabom.models.user import User
from tabom.services.like_service import do_like


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
        #like 2에서 일어났다.
        like1 = do_like(user.id, article.id)
        with self.assertRaises(Exception):
            like2 = do_like(user.id, article.id)