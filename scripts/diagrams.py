"""Original accessible SVG teaching diagrams; no network or third-party assets."""
from html import escape as esc

INK = '#234d3d'
GREEN = '#245c48'
MUTED = '#6f8072'

def lines(text, width=11):
    return [text[i:i + width] for i in range(0, len(text), width)]

def label(x, y, text, size=16, color=INK, width=11, anchor='start'):
    return ''.join(
        f'<text x="{x}" y="{y + i * 23}" text-anchor="{anchor}" '
        f'fill="{color}" font-size="{size}">{esc(line)}</text>'
        for i, line in enumerate(lines(text, width))
    )

def box(x, y, width, height, text, number=None, dark=False):
    fill = GREEN if dark else '#fffefa'
    out = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="12" fill="{fill}" stroke="#c8d5c6"/>'
    if number is not None:
        out += label(x + 18, y + 25, f'{number:02d}', 11, '#b5d1bf' if dark else MUTED)
    out += label(x + 18, y + (56 if number is not None else 34), text, color='#fff' if dark else INK, width=max(8, (width - 36) // 17))
    return out

def arrow(path, dashed=False):
    dash = ' stroke-dasharray="5 5"' if dashed else ''
    return f'<path d="{path}" fill="none" stroke="#718772" stroke-width="1.8" marker-end="url(#arrow)"{dash}/>'

def render(article, index):
    nodes = article['nodes']
    kind = article.get('diagram_type', 'flow')
    if article['slug'] in {'rag-finetune', 'gpu-memory', 'model-choices', 'industry-stack', 'serving-stack'}:
        kind = 'comparison'
    height = 420 if kind in {'branch', 'cycle', 'comparison'} else 340
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 {height}" role="img" aria-labelledby="title desc">',
         f'<title id="title">{esc(article["title"])}</title>',
         f'<desc id="desc">{esc("；".join(nodes))}。概念示意，细节见正文。</desc>',
         '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10" fill="none" stroke="#718772" stroke-width="1.5"/></marker></defs>',
         f'<rect width="840" height="{height}" rx="16" fill="#edf1e8"/>',
         '<g font-family="PingFang SC,Microsoft YaHei,sans-serif">',
         label(28, 34, f'FIELD NOTE / {index:02d}', 11, MUTED, 40)]
    if article['slug'] == 'ai-map':
        for i, node in enumerate(nodes):
            x, y = 35 + i * 46, 55 + i * 52
            p.append(f'<rect x="{x}" y="{y}" width="{770-i*92}" height="{265-i*52}" rx="10" fill="{["#dae5d6","#c0d5bf","#9fbea5",GREEN][i]}"/>')
            p.append(label(x+17, y+29, node, color='#fff' if i==3 else INK, width=35))
    elif article['slug'] == 'pd-disaggregation':
        p += [box(28, 100, 200, 125, 'P 实例：处理输入', 1),
              box(321, 100, 200, 125, 'KV 状态传输', 2),
              box(614, 100, 200, 125, 'D 实例：生成输出', 3, True),
              arrow('M234 160 H309'), arrow('M527 160 H602'),
              label(28, 273, 'P / D 可分别调度与扩容；两侧仍需相容的模型状态。', 14, MUTED, 55),
              label(28, 304, '收益受排队、网络与 KV 传输影响，并非保证加速。', 14, MUTED, 55)]
    elif kind == 'comparison':
        for i, node in enumerate(nodes):
            x, y = 28 + (i % 2) * 402, 60 + (i // 2) * 147
            p.append(box(x, y, 382, 126, node, i+1, i==3))
        p.append(label(28, 389, '并列概念或比较维度 · 不表示执行顺序', 13, MUTED, 55))
    elif kind == 'branch':
        p += [box(28, 155, 216, 112, nodes[0], 1),
              box(312, 70, 216, 112, nodes[1], 2),
              box(312, 255, 216, 112, nodes[2], 3),
              box(596, 155, 216, 112, nodes[3], 4, True),
              arrow('M248 201 H274 V126 H300'),
              arrow('M248 221 H274 V311 H300'),
              arrow('M532 126 H560 V201 H584'),
              arrow('M532 311 H560 V221 H584'),
              label(28, 399, '两条分支表示备选或并行路径；选择条件见正文。', 13, MUTED, 55)]
    elif kind == 'cycle':
        coords = [(70, 65), (490, 65), (490, 240), (70, 240)]
        for i, ((x, y), node) in enumerate(zip(coords, nodes)):
            p.append(box(x, y, 280, 112, node, i+1, i==3))
        p += [arrow('M356 121 H478'), arrow('M630 183 V228'),
              arrow('M484 296 H362'), arrow('M210 234 V189', True),
              label(28, 399, '反馈循环 · 每轮都要检查预算、权限和停止条件', 13, MUTED, 55)]
    elif kind == 'timeline':
        p.append('<path d="M55 87 H785" stroke="#bdcdb8" stroke-width="3"/>')
        for i, node in enumerate(nodes):
            x = 28 + i * 204
            p.append(f'<circle cx="{x+26}" cy="87" r="8" fill="{GREEN}"/>')
            p.append(box(x, 114, 174, 133, node, i+1, i==3))
        p.append(label(28, 299, '时间或处理阶段示意 · 方块宽度不代表耗时比例', 13, MUTED, 55))
    else:
        for i, node in enumerate(nodes):
            x = 28 + i * 204
            p.append(box(x, 94, 174, 145, node, i+1, i==3))
            if i < 3:
                p.append(arrow(f'M{x+180} 166 H{x+196}'))
        p.append(label(28, 295, '从左向右阅读 · 简化流程，实际实现可能不同', 13, MUTED, 55))
    p.append('</g></svg>')
    return ''.join(p)
