from django.db import models
from django.utils.text import slugify

class SiteSetting(models.Model):
  hero_title = models.CharField(max_length=120, blank=True)
  hero_sub = models.CharField(max_length=200, blank=True)
  hero_cta_text = models.CharField(max_length=50, blank=True)
  hero_cta_link = models.CharField(max_length=120, blank=True)
  calendar_embed_src = models.URLField(blank=True, help_text='Googleカレンダーの埋め込みURL')

  def __str__(self):
    return 'Site Setting'

class MissionBlock(models.Model):
  title = models.CharField(max_length=100)
  body = models.TextField()
  order = models.PositiveIntegerField(default=0)

  class Meta:
    ordering = ['order']
  
  def __str__(self):
    return f"{self.order:02d}. {self.title}"

class TrainingCategory(models.Model):
  name = models.CharField(max_length=50)
  slug = models.SlugField(unique=True, blank=True)

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.name)
    super().save(*args, **kwargs)

  def __str__(self):
    return self.name

class TrainingVideo(models.Model):
  title = models.CharField(max_length=120)
  category = models.ForeignKey(TrainingCategory, on_delete=models.PROTECT, null=True, blank=True)
  description = models.TextField(blank=True)
  video_url = models.URLField(help_text='YouTubeの視聴URL（watch?v=... でも可）')
  duration = models.CharField(max_length=20, blank=True)
  is_public = models.BooleanField(default=True)

  @property
  def embed_src(self) -> str:
    """YouTube視聴URL → 埋め込みURLへ変換。
    例: https://www.youtube.com/watch?v=ID → https://www.youtube-nocookie.com/embed/ID
    ショートURL(youtu.be/ID)にも対応。
    """
    url = self.video_url
    vid = None
    if 'watch?v=' in url:
      vid = url.split('watch?v=')[-1].split('&')[0]
    elif 'youtu.be/' in url:
      vid = url.split('youtu.be/')[-1].split('?')[0]
    elif '/embed/' in url:
      return url
    return f"https://www.youtube-nocookie.com/embed/{vid}" if vid else url

  def __str__(self):
    return self.title

class SideHustleItem(models.Model):
  name = models.CharField(max_length=80)
  summary = models.TextField(blank=True)
  pros = models.TextField(blank=True)
  cons = models.TextField(blank=True)
  link_url = models.URLField(blank=True)

  def __str__(self):
    return self.name

class Roadmap(models.Model):
  name = models.CharField(max_length=50)
  slug = models.SlugField(unique=True, blank=True)
  intro = models.TextField(blank=True)

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.name)
    super().save(*args, **kwargs)

  def __str__(self):
    return self.name

class Step(models.Model):
  roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name='steps')
  order = models.PositiveIntegerField(default=0)
  title = models.CharField(max_length=120)
  detail = models.TextField(blank=True)
  resource_url = models.URLField(blank=True)

  class Meta:
    ordering = ['order']

  def __str__(self):
    return f"{self.roadmap.name} - {self.order:02d} {self.title}"

class AITool(models.Model):
  name = models.CharField(max_length=80)
  category = models.CharField(max_length=50, blank=True)
  intro = models.TextField(blank=True)
  howto = models.TextField(blank=True)
  link_url = models.URLField()

  def __str__(self):
    return self.name
