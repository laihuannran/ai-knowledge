"""Shared, deterministic content inventory for the site and validation scripts."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORY_ORDER = [
    'AI 基础', '模型能力', '训练与对齐', 'AI 应用', '智能体',
    '接入平台', '推理设施', '评测运行', '多模态', '行业技术栈', '应用技术栈',
]

def load_articles():
    articles = []
    for name in ('articles.json', 'expansion.json', 'supplement.json', 'stack_chapters.json', 'deep_chapters.json', 'protocol_series.json', 'retrieval_series.json', 'agent_series.json', 'protocol_landscape.json', 'a2a_series.json', 'rsi_series.json', 'foundation_series.json', 'reasoning_series.json', 'data_training_series.json', 'interactive_multimodal_series.json', 'context_series.json', 'memory_series.json', 'openai_api_series.json', 'claude_gemini_api_series.json', 'cloud_client_api_series.json', 'api_adapter_series.json', 'wiki_curation.json', 'wiki_retrieval_series.json', 'wiki_training_series.json', 'wiki_serving_series.json'):
        path = ROOT / 'content' / name
        if path.exists():
            articles.extend(json.loads(path.read_text()))
    for article in articles:
        if article['category'] == 'AI应用':
            article['category'] = 'AI 应用'
    order = {name: index for index, name in enumerate(CATEGORY_ORDER)}
    book_path = ROOT / 'content' / 'book.json'
    if book_path.exists():
        book = json.loads(book_path.read_text())
        slugs = [slug for part in book['parts'] for chapter in part['chapters'] for slug in chapter['slugs']]
        positions = {slug: index for index, slug in enumerate(slugs)}
        return sorted(articles, key=lambda article: positions.get(article['slug'], len(positions)))
    return sorted(articles, key=lambda article: order.get(article['category'], len(order)))
