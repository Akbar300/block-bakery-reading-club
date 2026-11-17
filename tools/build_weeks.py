"""Turn the Fluff Squad Reading Academy weeks into Block Bakery "Big Reads".
python3 tools/build_weeks.py tools/academy_weeks.json  -> rewrites the WEEKREADS block in index.html
academy_weeks.json = the Academy's DATA.weeks (released VDOE items are NOT included: they stay private)."""
import json, re, sys, random
src = sys.argv[1] if len(sys.argv) > 1 else 'tools/academy_weeks.json'
weeks = json.load(open(src))
QAR = {'right': 'Right there: the answer is in the text. Look back and find the words.',
       'search': 'Think and search: the clues are in more than one place. Look back at the text.',
       'author': 'Author and me: use clues from the text plus what you already know.',
       '': 'Look back at the text and find the part that answers the question.'}
BUDDIES = ['mochi', 'sprout', 'sparky']
def skill(q):
    return re.sub(r'[^a-z]+', '', (q.get('skill') or 'reading').lower())[:14] or 'reading'
def conv(q, nparas):
    t = q['t']; hint = QAR.get(q.get('qar') or '', QAR[''])
    if t == 'mc':
        g = dict(t='mc', skill=skill(q), q=q['stem'].replace(' —', ':'), ch=q['opts'], a=q['ans'], hint=hint)
        if q.get('why'): g['why'] = q['why']
        m = re.search(r'paragraph (\d+)', q['stem'])
        if m and int(m.group(1)) <= nparas: g['ev'] = int(m.group(1)) - 1
        return g
    if t == 'hot':
        return dict(t='evidence', skill='evidence', q=q['stem'], a=q['ans'], hint='Not that one. ' + hint)
    if t == 'order':
        return dict(t='order', skill='sequence', q=q['stem'], items=q['items'])
    if t == 'multi':
        items = [[o, 0 if i in q['ans'] else 1] for i, o in enumerate(q['opts'])]
        return dict(t='sort', skill=skill(q), q=q['stem'].replace('Which TWO ideas', 'Sort the ideas: which') , bins=['In BOTH texts', 'Only in one text'], items=items,
                    hint='Is it in the story AND the article? If it is only in one, it goes in the other box.')
    if t == 'fill':
        slots, bank, ans = q['slots'], q['bank'], q['ans']
        if any(s is None for s in slots) and len(ans) == len(bank):
            first = [s for s in slots if s is not None]
            return dict(t='order', skill='sequence', q=q['stem'].replace('Complete the chart', 'Put the steps in order'), items=first + [bank[i] for i in ans])
        bins = [s for s in slots]; extra = len(bank) > len(ans)
        if extra: bins = bins + ['Does not belong']
        items = []
        for bi, idx in enumerate(ans): items.append([bank[idx], bi])
        for i, b in enumerate(bank):
            if i not in ans: items.append([b, len(bins) - 1])
        return dict(t='sort', skill=skill(q), q=q['stem'].replace('Complete the chart. Put one box under each heading.', 'Sort each box under the right heading.'), bins=bins, items=items,
                    hint=QAR.get(q.get('qar') or '', QAR['']))
    return None
out = []
for w in weeks:
    texts = []
    for ti, t in enumerate(w['texts']):
        paras, heads = [], []
        multi = len(t['parts']) > 1
        for p in t['parts']:
            ph = p.get('heads') or [None] * len(p['paras'])
            for i, para in enumerate(p['paras']):
                paras.append(para); heads.append((p['title'] if (multi and i == 0) else ph[i]) if (multi and i == 0) or ph[i] else None)
        cap = next((p.get('caption') for p in t['parts'] if p.get('caption')), None)
        games = [g for g in (conv(q, len(paras)) for q in t['qs']) if g]
        texts.append(dict(id=f"wk{w['n']}{t['key'][0]}", key=t['key'], kind='Story' if t['key'] == 'story' else 'Article', title=t['title'],
                          text=paras, heads=heads if any(heads) else None, caption=cap, games=games, buddy=BUDDIES[(w['n'] + ti) % 3]))
    wd = dict(n=w['n'], start=w['start'], focus=w['focus'], rule=w.get('rule') or '', boxes=w.get('boxes'), spell=w['spell'], quiz=w.get('quiz') or {},
              words=[[x['w'], x['m']] for x in w['words']], meaning=w.get('meaning'), purpose=w.get('purpose') or '', texts=texts)
    out.append(wd)
js = 'const WEEKREADS=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';'
p = 'index.html'; s = open(p).read()
a, b = '/*WEEKREADS-START*/', '/*WEEKREADS-END*/'
assert a in s and b in s, 'markers missing'
s = s[:s.index(a) + len(a)] + js + s[s.index(b):]
open(p, 'w').write(s)
print('weeks', len(out), 'texts', sum(len(w['texts']) for w in out), 'games', sum(len(t['games']) for w in out for t in w['texts']), 'bytes', len(js))
