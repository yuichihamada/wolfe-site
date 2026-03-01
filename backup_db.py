import json, psycopg2

url = "postgresql://postgres:dvaOnaIzeNvKjIDERWrZeRDYGVJtrogP@maglev.proxy.rlwy.net:25452/railway"
conn = psycopg2.connect(url)
cur = conn.cursor()
cur.execute("""
    SELECT p.id, r.name as roadmap_name, p.title, p.slug, p.order, p.is_published, p.body
    FROM content_roadmappage p
    JOIN content_roadmap r ON p.roadmap_id = r.id
    ORDER BY r.order, p.order
""")
rows = cur.fetchall()
cols = [d[0] for d in cur.description]
data = [dict(zip(cols, row)) for row in rows]
with open("backup_roadmap_pages.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"バックアップ完了: {len(data)} 件")
conn.close()
