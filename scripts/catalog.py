"""Shared, deterministic content inventory for the site and validation scripts."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORY_ORDER = [
    'AI 基础', '模型能力', '训练与对齐', 'AI 应用', '智能体',
    '接入平台', '推理设施', '评测运行', '多模态', '行业技术栈',
]

def load_articles():
    articles = []
    for name in ('articles.json', 'expansion.json', 'supplement.json'):
        path = ROOT / 'content' / name
        if path.exists():
            articles.extend(json.loads(path.read_text()))
    order = {name: index for index, name in enumerate(CATEGORY_ORDER)}
    return sorted(articles, key=lambda article: order.get(article['category'], len(order)))
