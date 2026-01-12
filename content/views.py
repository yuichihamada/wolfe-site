from django.shortcuts import render, get_object_or_404
from .models import (
  Calendar, MissionBlock, TrainingCategory, TrainingVideo,
  SideHustleItem, Roadmap, RoadmapPage, AITool, HeroImage, News
)
import secrets
import unicodedata
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q,  Prefetch
from django.utils import timezone
from datetime import timedelta
from .forms import QuestionForm
from .models import Question, FaqEntry
import markdown as md_lib

def render_markdown_with_toc(text: str) -> tuple[str, str]:
    md = md_lib.Markdown(
        extensions=["fenced_code", "tables", "toc"],
        extension_configs={
            "toc": {"toc_depth": "2-2", "permalink": False}
        },
        output_format="html5",
    )
    html = md.convert(text or "")
    toc = md.toc or ""
    return html, toc

def get_setting():
  return Calendar.objects.first()

def home(request):
  s = get_setting()
  now = timezone.now()
  hero_images = (
      HeroImage.objects
      .filter(slot=HeroImage.SLOT_HOME, is_active=True)
      .filter(Q(start_at__isnull=True) | Q(start_at__lte=now))
      .filter(Q(end_at__isnull=True) | Q(end_at__gte=now))
      .order_by("order", "id")
  )
  ctx = {'s': s, 'hero_images': hero_images}
  return render(request, 'content/home.html', ctx)

def mission(request):
  blocks = MissionBlock.objects.all()
  return render(request, 'content/mission.html', {'blocks': blocks})

def training_list(request):
  qs = TrainingVideo.objects.filter(is_public=True)
  categories = TrainingCategory.objects.all()
  c = request.GET.get('category')
  if c:
    qs = qs.filter(category__slug=c)
  return render(request, 'content/training_list.html', {
    'videos': qs,
    'categories': categories,
    'current': c or '',
  })

def side_hustle(request):
    qs = SideHustleItem.objects.all().order_by('id')

    context = {
        'pocket_items': qs.filter(category='pocket'),
        'career_items': qs.filter(category='career'),
        'life_items': qs.filter(category='life'),
        'other_items': qs.filter(category='other'),
    }
    return render(request, 'content/side_hustle.html', context)

def roadmap_home(request):
    s = get_setting()
    page_qs = (
        RoadmapPage.objects
        .filter(is_published=True)
        .only("id", "roadmap_id", "title", "slug", "order", "cover_image")
        .order_by("order", "id")
    )
    roads = (
        Roadmap.objects
        .all()
        .order_by("order", "id")
        .prefetch_related(
            Prefetch("pages", queryset=page_qs)
        )
    )
    return render(request, "roadmap/home.html", {"roads": roads, "s": s})

def roadmap_page_detail(request, roadmap_slug, page_slug):
    roadmap = get_object_or_404(Roadmap, slug=roadmap_slug)

    page = get_object_or_404(
        RoadmapPage,
        roadmap=roadmap,
        slug=page_slug,
        is_published=True,
    )

    # 同じSTEP内のページ一覧（サイドバーやナビ用）
    pages = roadmap.pages.filter(is_published=True)

    # 前後ページ（次へ・前へ）
    prev_page = (
        pages
        .filter(order__lt=page.order)
        .order_by("-order")
        .first()
    )
    next_page = (
        pages
        .filter(order__gt=page.order)
        .order_by("order")
        .first()
    )
    
    body_html, body_toc = render_markdown_with_toc(page.body)
    
    context = {
        "roadmap": roadmap,
        "page": page,
        "pages": pages,
        "prev_page": prev_page,
        "next_page": next_page,
        "body_html": body_html,
        "body_toc": body_toc,
    }

    return render(
        request,
        "roadmap/page_detail.html",
        context
    )

def ai_tools(request):
  tools = AITool.objects.all()
  return render(request, 'content/ai_tools.html', {'tools': tools})

def calendar(request):
  s = get_setting()
  return render(request, 'content/calendar.html', {'s': s})

def news_list(request):
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")

    news = News.objects.all()

    # キーワード検索（タイトル＋本文）
    if q:
        news = news.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        )

    # カテゴリ絞り込み（あれば）
    if category:
        news = news.filter(category=category)

    context = {
        "news": news,
        "q": q,
        "category": category,
    }
    return render(request, "news/list.html", context)

def news_detail(request, slug):
    item = News.objects.get(slug=slug)
    return render(request, "news/detail.html", {"item": item})

def question_box(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "送信ありがとうございます！")
            return redirect("question_box")
    else:
        form = QuestionForm()

    public_faqs = FaqEntry.objects.filter(is_published=True)

    context = {
        "form": form,
        "public_faqs": public_faqs,
    }
    return render(request, "content/question_box.html", context)

def _norm_bytes(s: str) -> bytes:
    # NFC 正規化してから UTF-8 で bytes 化
    return unicodedata.normalize("NFC", (s or "")).encode("utf-8")

def gate(request):
    """共通パスワード入力ページ"""
    if request.method == "POST":
        pw = (request.POST.get("password") or "").strip()
        ok = secrets.compare_digest(_norm_bytes(pw), _norm_bytes(settings.WOLFE_GATE_PASSWORD))
        if ok:
            request.session['gate_ok'] = True
            request.session['gate_ver'] = settings.GATE_VERSION 
            # 24時間保持（remember付き）/ ブラウザ閉じたら破棄（rememberなし）
            if request.POST.get("remember"):
                request.session.set_expiry(60 * 60 * 24)  # 24h
            else:
                request.session.set_expiry(0)
            return redirect(request.GET.get("next") or "/")
        else:
            messages.error(request, "パスワードが違います。")
    return render(request, "content/gate.html")

def gate_logout(request):
    """ゲート通過状態を解除"""
    request.session.pop('gate_ok', None)
    return redirect(settings.ACCESS_GATE_URL)
  