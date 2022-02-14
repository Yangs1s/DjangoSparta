from typing import List, Optional

from ninja import Schema

from tabom.APIs.v1.schema.like_response import LikeResponse


class ArticleResponse(Schema):
    id: int
    title: str
    my_likes: Optional[List[LikeResponse]]
