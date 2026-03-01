#!/usr/bin/env python3
"""
ローカルのMarkdownファイルをAPIで一括アップロードするスクリプト

使用方法:
    python upload_articles.py

事前準備:
    1. Django admin でトークンを発行し、TOKEN に設定
    2. API_URL をデプロイ先のドメインに変更
"""

import pathlib
import re
import unicodedata
import requests

# ===== 設定（後から変更する箇所) =====
API_URL = "https://www.rebirth-connect.com/api/pages/"
TOKEN = "2bd2386e36864c49a3e315ce215ccd2f9fd06ea1"
# ======================================

ARTICLES_DIR = pathlib.Path(
    "/Users/hamadayuichi/Desktop/WOLFE/マネジメント用"
    "/REBIRTH Connect ロードマップ/ロードマップ 記事/existing-articles"
)

headers = {"Authorization": f"Token {TOKEN}"}


def upload():
    if not ARTICLES_DIR.exists():
        print(f"エラー: 記事フォルダが見つかりません: {ARTICLES_DIR}")
        return

    total_created = 0
    total_updated = 0
    total_errors = 0

    for step_dir in sorted(ARTICLES_DIR.iterdir()):
        if not step_dir.is_dir():
            continue

        # フォルダ名から "STEP1 ", "STEP3.5 ", "extra " などのプレフィックスを除去
        # 例: "STEP1 スタートアップ" → "スタートアップ"
        #     "STEP3.5 事業に確信を持つ" → "事業に確信を持つ"
        #     "extra 番外編" → "番外編"
        roadmap_name = re.sub(r'^(STEP\d+(?:\.\d+)?\s+|extra\s+)', '', step_dir.name)
        # macOS はフォルダ名を NFD で保存するため NFC に正規化して DB と一致させる
        roadmap_name = unicodedata.normalize('NFC', roadmap_name)
        print(f"\n--- {roadmap_name} ---")

        for md_file in sorted(step_dir.glob("*.md")):
            filename = md_file.stem  # 例: "01_最初に"
            parts = filename.split("_", 1)

            try:
                order = int(parts[0])
            except ValueError:
                print(f"  スキップ（番号なし）: {md_file.name}")
                continue

            title = parts[1] if len(parts) > 1 else filename
            body = md_file.read_text(encoding="utf-8")

            payload = {
                "roadmap_name": roadmap_name,
                "title": title,
                "order": order,
                "body": body,
            }

            try:
                resp = requests.post(API_URL, json=payload, headers=headers, timeout=10)
            except requests.RequestException as e:
                print(f"  [通信エラー] {title}: {e}")
                total_errors += 1
                continue

            if resp.status_code == 201:
                print(f"  [作成] order={order} {title}")
                total_created += 1
            elif resp.status_code == 200:
                print(f"  [更新] order={order} {title}")
                total_updated += 1
            else:
                print(f"  [エラー {resp.status_code}] {title}: {resp.text}")
                total_errors += 1

    print(f"\n完了: 作成={total_created} 更新={total_updated} エラー={total_errors}")


if __name__ == "__main__":
    upload()
