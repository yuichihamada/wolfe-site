from django.contrib import admin
from .models import (
  SiteSetting, MissionBlock, TrainingCategory, TrainingVideo,
  SideHustleItem, Roadmap, Step, AITool
)

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
  list_display = ("hero_title", "calendar_embed_src")

@admin.register(MissionBlock)
class MissionBlockAdmin(admin.ModelAdmin):
  list_display = ("title", "order",)
  list_editable = ("order",)

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

class StepInline(admin.TabularInline):
  model = Step
  extra = 1

@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug": ("name",)}
  inlines = [StepInline]

@admin.register(AITool)
class AIToolAdmin(admin.ModelAdmin):
  list_display = ("name", "category", "link_url")
  list_filter = ("category",)
  search_fields = ("name", "intro", "howto")
