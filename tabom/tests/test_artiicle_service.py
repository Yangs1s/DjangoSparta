from django.test import TestCase

from tabom.models import User
from tabom.models.article import Article
from tabom.services.article_service import get_an_article, get_article_list
from tabom.services.like_service import do_like


class TestArticleService(TestCase):
    def test_you_can_get_an_article_by_id(self) -> None:
        # Given
        title = "test_title"
        article = Article.objects.create(title=title)

        # When
        result_article = get_an_article(article.id)

        # Then 처음 만들었던 아티클 아이디 마지막 아티클 아이디 둘이 같은지 비교를 한다.
        self.assertEqual(article.id, result_article.id)
        self.assertEqual(title, result_article.title)

    def test_it_should_raise_exception_when_article_does_not_exist(self) -> None:
        # Given 없는 아티클 번호로 어떤 에러가 날까 검증을 한다.
        invalid_article_id = 9988

        # Expect
        with self.assertRaises(Article.DoesNotExist):
            get_an_article(invalid_article_id)

    def test_article_list_should_prefetch_like(self) -> None:
        # Given
        user = User.objects.create(name="test_user")
        articles = [Article.objects.create(title=f"{i}") for i in range(1, 21)]
        do_like(user.id, articles[-1].id)

        # when
        with self.assertNumQueries(3):
            result_articles = get_article_list(0, 0, 10)
            result_counts = [a.like_set.count() for a in result_articles]
        # Then

        self.assertEqual(len(result_articles), 10)
        self.assertEqual(1, result_counts[0])
        self.assertEqual(
            [a.id for a in reversed(articles[10:21])],
            [a.id for a in result_articles],
        )

    # def test_article_page_should_prefetch_like(self) -> None:
    #     #Given
    #     user = User.objects.create(name="test_user")
    #     articles = [Article.objects.create(title = f"{i}") for i in range(1,21)]
    #     do_like(user.id, articles[-1].id)
    #
    #     #when
    #     result_articles = get_article_page(1, 10)
    #
    #     #Then
    #
    #     self.assertEqual(len(result_articles),10)
    #     self.assertEqual(1, result_articles[0].like_set.count())
    #     self.assertEqual(
    #         [a.id for a in reversed(articles[10:21])],
    #         [a.id for a in result_articles],
    #
    #     )
    def test_get_article_list_should_contain_my_like_when_like_exists(self) -> None:
        # Given
        user = User.objects.create(name="test_user")
        article1 = Article.objects.create(title="article1")
        like = do_like(user.id, article1.id)
        Article.objects.create(title="article2")

        # When
        articles = get_article_list(user.id, 0, 10)

        # Then
        self.assertEqual(like.id, articles[1].my_likes[0].id)
        self.assertEqual(0, len(articles[0].my_likes))
