import re

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Roadmap, RoadmapPage
from .serializers import RoadmapPageUpsertSerializer


def _get_roadmap(name: str) -> Roadmap | None:
    """
    nameでRoadmapを取得。存在しない場合は None を返す。
    フォルダ名の "STEP1 " 等のプレフィックスは upload_articles.py 側で除去済み。
    """
    try:
        return Roadmap.objects.get(name=name)
    except Roadmap.DoesNotExist:
        return None


class PageUpsertView(APIView):
    """
    ロードマップ記事の作成・更新 API

    POST /api/pages/
    {
        "roadmap_name": "スタートアップ",
        "title": "最初に",
        "order": 1,
        "body": "Markdown本文..."
    }

    - roadmap_name は DB 上の Roadmap.name と完全一致させること（自動作成しない）
    - 同じ roadmap × order の記事が存在する場合は上書き更新
    - 認証: Authorization: Token <token>
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RoadmapPageUpsertSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        roadmap = _get_roadmap(data["roadmap_name"])
        if roadmap is None:
            return Response(
                {"roadmap_name": f"Roadmap '{data['roadmap_name']}' が見つかりません。"},
                status=status.HTTP_404_NOT_FOUND,
            )

        page, created = RoadmapPage.objects.update_or_create(
            roadmap=roadmap,
            order=data["order"],
            defaults={
                "title": data["title"],
                "body": data["body"],
            },
        )

        return Response(
            {
                "id": page.id,
                "roadmap": roadmap.name,
                "title": page.title,
                "order": page.order,
                "created": created,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )
