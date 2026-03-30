with open('C:/Users/LJG/Documents/GitHub/portfolio/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Swap tab labels
content = content.replace(
    'switchCaseTab(this,1)"><span class="case-tab-badge">#2</span> 메모리 누수 \u2192 Redis</button>',
    'switchCaseTab(this,1)"><span class="case-tab-badge">#2</span> 느린 API \u2192 Redis 캐싱</button>'
)
content = content.replace(
    'switchCaseTab(this,2)"><span class="case-tab-badge">#3</span> 느린 API \u2192 Redis 캐싱</button>',
    'switchCaseTab(this,2)"><span class="case-tab-badge">#3</span> 메모리 누수 \u2192 Redis</button>'
)

# 2. Swap panel contents (keep IDs, swap inner HTML)
def extract_panel(html, pid):
    opener = '<div class="case-panel" id="' + pid + '">'
    s = html.find(opener)
    if s == -1:
        return None, -1, -1
    body_start = s + len(opener)
    depth = 1
    i = body_start
    while i < len(html) and depth > 0:
        o = html.find('<div', i)
        c = html.find('</div>', i)
        if o == -1:
            o = len(html)
        if c == -1:
            break
        if o < c:
            depth += 1
            i = o + 4
        else:
            depth -= 1
            if depth == 0:
                return html[body_start:c], s, c + 6
            i = c + 6
    return None, -1, -1

inner1, s1, e1 = extract_panel(content, 'case-panel-1')
inner2, s2, e2 = extract_panel(content, 'case-panel-2')

if inner1 is None or inner2 is None:
    print('ERROR: panel not found')
    exit(1)

new_p1 = '<div class="case-panel" id="case-panel-1">' + inner2 + '</div>'
new_p2 = '<div class="case-panel" id="case-panel-2">' + inner1 + '</div>'

between = content[e1:s2]
new_content = content[:s1] + new_p1 + between + new_p2 + content[e2:]

with open('C:/Users/LJG/Documents/GitHub/portfolio/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Done!')
print('Tab2 => 느린 API -> Redis 캐싱')
print('Tab3 => 메모리 누수 -> Redis')
