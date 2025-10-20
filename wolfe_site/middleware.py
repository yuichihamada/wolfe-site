import re
from django.conf import settings
from django.shortcuts import redirect

class AccessGateMiddleware:
  """
  共通パスワードのゲート。セッションに 'gate_ok' がない限り、
  /gate/ 以外のページを /gate/?next=... にリダイレクトする。
  """
  def __init__(self, get_response):
    self.get_response = get_response
    self.exempt_patterns = [re.compile(p) for p in getattr(settings, 'ACCESS_GATE_EXEMPT_URLS', [])]

  def __call__(self, request):
    path = request.path

    # 管理画面ユーザー（staff）は素通しにしたい場合
    if getattr(request, "user", None) and request.user.is_authenticated and request.user.is_staff:
      return self.get_response(request)

    # 除外パスは素通し
    for pattern in self.exempt_patterns:
      if pattern.match(path):
        return self.get_response(request)
    
    # 通過フラグがあればOK → を、バージョン一致に強化
    if request.session.get('gate_ok') and request.session.get('gate_ver') == settings.GATE_VERSION:
      return self.get_response(request)

    # それ以外はゲートへ
    next_qs = f"?next={path}" if path != settings.ACCESS_GATE_URL else ""
    return redirect(settings.ACCESS_GATE_URL + next_qs)
