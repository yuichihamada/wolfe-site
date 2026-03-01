from rest_framework import serializers


class RoadmapPageUpsertSerializer(serializers.Serializer):
    roadmap_name = serializers.CharField(help_text="Roadmapのname（例: STEP1 スタートアップ）")
    title = serializers.CharField(max_length=120, help_text="記事タイトル")
    order = serializers.IntegerField(min_value=1, help_text="記事の表示順（ファイル名の番号）")
    body = serializers.CharField(allow_blank=True, help_text="Markdown本文")
