import json, io
d = json.load(io.open(r'E:/新建文件夹/exp2-vue/.workbuddy/tmp/table.json', encoding='utf-8'))
cells = d['block']['table']['cells']
for c in cells:
    if c.get('mc'):
        continue
    txt = c.get('text', '')
    marks = []
    if c.get('grid_span'): marks.append('gs%d' % c['grid_span'])
    if c.get('v_merge'): marks.append('vm:%s' % c['v_merge'])
    print('[r%s c%s]%s %s' % (c.get('row'), c.get('col'), (' ' + ','.join(marks)) if marks else '', repr(txt)))
