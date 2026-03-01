from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Roadmap, RoadmapPage
from .serializers import RoadmapPageUpsertSerializer


class PageUpsertView(APIView):
    """
    ロードマップ記事の作成・更新 API

    POST /api/pages/
    {
        "roadmap_name": "STEP1 スタートアップ",
        "title": "最初に",
        "order": 1,
        "body": "Markdown本文..."
    }

    - 同じ roadmap × order の記事が存在する場合は上書き更新
    - 存在しない場合は新規作成
    - 認証: Authorization: Token <token>
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RoadmapPageUpsertSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        try:
            roadmap = Roadmap.objects.get(name=data["roadmap_name"])
        except Roadmap.DoesNotExist:
            return Response(
                {"error": f"Roadmap '{data['roadmap_name']}' が見つかりません。Django admin でまず Roadmap を作成してください。"},
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
