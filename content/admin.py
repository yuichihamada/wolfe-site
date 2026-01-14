from django.contrib import admin
from .models import (
  Calendar, TrainingCategory, TrainingVideo,
  SideHustleItem, Roadmap, RoadmapPage, AITool, HeroImage, News, Question, FaqEntry
)
from markdownx.widgets import MarkdownxWidget
from django import forms

@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
  list_display = ("hero_title", "calendar_embed_src")
  fields = (
      "hero_title",
      "hero_sub",
      "calendar_embed_src",
      "roadmap_cover_image",
  )

@admin.register(TrainingCategory)
class TrainingCategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug": ("name",)}

@admin.register(TrainingVideo)
class TrainingVideoAdmin(admin.ModelAdmin):
  list_display = ("title", "category", "is_public")
  list_filter = ("category", "is_public")
  search_fields = ("title", "description")

@admin.register(SideHustleItem)
class SideHustleItemAdmin(admin.ModelAdmin):
  list_display = ("name", "link_url")

class RoadmapPageInline(admin.TabularInline):
    model = RoadmapPage
    extra = 1
    fields = (
        "order",
        "title",
        "slug",
        "is_published",
    )
    ordering = ("order",)
    
    prepopulated_fields = {
        "slug": ("title",),
    }

@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ("order", "kind", "name")
    ordering = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "summary")

    fieldsets = (
        ("基本情報（STEP）", {
            "fields": ("kind", "order", "name", "slug"),
        }),
        ("説明", {
            "fields": ("summary",),
        }),
    )

    inlines = [
        RoadmapPageInline,  # ← PDF相当（主役）
    ]

class RoadmapPageAdminForm(forms.ModelForm):
    class Meta:
        model = RoadmapPage
        fields = "__all__"
        widgets = {
            "body": MarkdownxWidget(attrs={
                "rows": 40,
                "style": (
                    "font-family: ui-monospace, Menlo, Consolas, monospace;"
                    "line-height:1.65;"
                    "font-size:14px;"
                ),
            }),
        }

@admin.register(RoadmapPage)
class RoadmapPageAdmin(admin.ModelAdmin):
    form = RoadmapPageAdminForm

    list_display = ("title", "roadmap", "order", "is_published")
    list_filter = ("roadmap", "is_published")
    search_fields = ("title", "body")
    ordering = ("roadmap", "order")

    prepopulated_fields = {"slug": ("title",)}

    fields = (
        "roadmap",
        "order",
        "title",
        "slug",
        "cover_image",
        "body",
        "is_published",
    )
    
    class Media:
        css = {
            "all": ("admin/roadmap_markdownx.css",)
        }

@admin.register(AITool)
class AIToolAdmin(admin.ModelAdmin):
  list_display = ("name", "category", "link_url")
  list_filter = ("category",)
  search_fields = ("name", "intro", "howto")

@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = ("slot", "order", "alt", "is_active", "start_at", "end_at")
    list_filter = ("slot", "is_active")
    search_fields = ("alt",)
    ordering = ("slot", "order", "id")

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at", "is_pinned")
    list_filter = ("category", "is_pinned", "created_at")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("display_name", "category", "short_body", "status", "faq_entry", "created_at")
    list_filter = ("category", "status", "created_at", "faq_entry")
    search_fields = ("name", "body")
    readonly_fields = ("created_at",)

    fieldsets = (
        ("投稿内容", {
            "fields": ("name", "category", "body"),
        }),
        ("対応状況", {
            "fields": ("status", "faq_entry"),
        }),
        ("メタ情報", {
            "fields": ("created_at",),
        }),
    )

    def short_body(self, obj):
        return (obj.body[:40] + "…") if len(obj.body) > 40 else obj.body
    short_body.short_description = "内容（抜粋）"


@admin.register(FaqEntry)
class FaqEntryAdmin(admin.ModelAdmin):
    list_display = ("question_text", "category", "is_published", "created_at")
    list_filter = ("category", "is_published", "created_at")
    search_fields = ("question_text", "answer")
