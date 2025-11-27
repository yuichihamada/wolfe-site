from django.db import models
from django.utils.text import slugify
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Calendar(models.Model):
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
    CATEGORY_CHOICES = [
        ('pocket', 'お小遣い案件'),
        ('career', 'キャリア支援'),
        ('life', '固定費削減'),
        ('other', 'その他'),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='pocket'
    )
    name = models.CharField(max_length=80)
    summary = models.TextField(blank=True)
    reward = models.CharField(max_length=120, blank=True)
    pros = models.TextField(blank=True)
    cons = models.TextField(blank=True)
    link_url = models.URLField(blank=True)

    image = models.ImageField(
        upload_to='side_hustle/',
        blank=True,
        null=True,
        verbose_name='イメージ画像'
    )

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
  image = models.ImageField(upload_to='ai_tools/', blank=True, null=True)

  def __str__(self):
    return self.name

class HeroImage(models.Model):
    SLOT_HOME = "home"
    SLOT_CHOICES = [
        (SLOT_HOME, "ホーム"),
    ]

    slot = models.CharField(max_length=20, choices=SLOT_CHOICES, default=SLOT_HOME, db_index=True)
    image = models.ImageField(upload_to="hero/")
    alt = models.CharField("代替テキスト", max_length=200, blank=True)
    order = models.PositiveIntegerField("表示順", default=0, db_index=True)
    is_active = models.BooleanField("有効", default=True)
    start_at = models.DateTimeField("掲載開始", null=True, blank=True)
    end_at = models.DateTimeField("掲載終了", null=True, blank=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        base = self.alt or self.image.name
        return f"{self.get_slot_display()} | {base} ({'ON' if self.is_active else 'OFF'})"

class News(models.Model):
    CATEGORY_CHOICES = [
        ("info", "会社情報"),
        ("training", "研修"),
        ("event", "イベント"),
        ("site", "サイト"),
        ("others", "その他"),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False, help_text="固定表示")
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ["-is_pinned", "-created_at"]
    
    def is_new(self):
        """作成から7日以内なら新着扱い"""
        if not self.created_at:
            return False
        return self.created_at >= timezone.now() - timedelta(days=7)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class FaqEntry(models.Model):
    CATEGORY_CHOICES = [
        ("apoint", "アポイント"),
        ("knowledge", "WOLFE事業知識"),
        ("sidejob", "副業コミュニティ"),
        ("request", "意見・要望"),
        ("other", "その他"),
    ]

    category = models.CharField(
        "カテゴリ",
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="other",
    )
    
    question_text = models.TextField(
        "Q&Aの質問内容（1つ or 複数の質問をまとめた要約）",
        help_text="複数の質問をまとめる場合は要約文でOKです。",
    )
    
    answer = models.TextField("回答内容")

    is_published = models.BooleanField(
        "サイトに公開する",
        default=True,
    )

    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.question_text[:30] + "…" if len(self.question_text) > 30 else self.question_text


class Question(models.Model):
    CATEGORY_CHOICES = FaqEntry.CATEGORY_CHOICES

    STATUS_CHOICES = [
        ("new", "未回答"),
        ("answered_private", "個別対応済み"),
        ("answered_public", "Q&Aで回答済み"),
        ("no_action", "対応不要"),
    ]

    name = models.CharField(
        "お名前",
        max_length=50,
        blank=True,
        help_text="匿名で投稿したい場合は空欄でOKです。",
    )

    category = models.CharField(
        "カテゴリ",
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="apoint",
    )

    body = models.TextField("内容（質問・相談・ご意見など）")

    status = models.CharField(
        "対応ステータス",
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
    )

    # この質問が、どのQ&Aでカバーされているか（されていない場合は空欄）
    faq_entry = models.ForeignKey(
        FaqEntry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="紐づくQ&A",
        related_name="questions",
    )

    created_at = models.DateTimeField("投稿日時", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def display_name(self):
        return self.name or "匿名"

    def __str__(self):
        return f"{self.get_category_display()}（{self.display_name()}）"
