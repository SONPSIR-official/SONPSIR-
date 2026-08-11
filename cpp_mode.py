import re, sys

def выр(с):
    с = с.replace('!=', '\x01')
    с = с.replace('&&', ' and ').replace('||', ' or ')
    с = re.sub(r'!(\w)', r'not \1', с)
    с = с.replace('\x01', '!=')
    с = с.replace('true', 'True').replace('false', 'False')
    с = с.replace('std::', '')
    return с

def перевести_cpp(код):
    out = []
    ind = 0
    for raw in код.split('\n'):
        стр = raw.strip()
        if not стр or стр.startswith('#') or стр.startswith('using namespace'):
            continue
        if re.match(r'int\s+main\s*\(', стр) or стр in ('return 0;', 'return 0'):
            continue
        if стр == '}':
            ind = max(0, ind - 1)
            continue
        pad = '    ' * ind
        if стр.endswith('{'):
            head = стр[:-1].strip()
            m = re.match(r'(int|float|double|void|bool|string|auto)\s+(\w+)\s*\(([^)]*)\)', head)
            if m:
                args = [a.strip().split()[-1] for a in m.group(3).split(',') if a.strip()]
                out.append(pad + 'def %s(%s):' % (m.group(2), ', '.join(args)))
            elif re.match(r'for\s*\(', head):
                m2 = re.match(r'for\s*\(\s*(?:int\s+)?(\w+)\s*=\s*(\d+)\s*;\s*\w+\s*<\s*([^;]+);\s*\w+\+\+\s*\)', head)
                out.append(pad + ('for %s in range(%s, %s):' % (m2.group(1), m2.group(2), выр(m2.group(3))) if m2 else 'for _ in range(1):'))
            elif re.match(r'else\s+if', head):
                out.append(pad + 'elif %s:' % выр(re.sub(r'else\s+if\s*\((.*)\)', r'\1', head)))
            elif re.match(r'\}\s*else\s+if', head):
                ind = max(0, ind - 1)
                out.append('    ' * ind + 'elif %s:' % выр(re.sub(r'.*?\((.*)\)', r'\1', head)))
                ind += 1
                continue
            elif re.match(r'\}\s*else', head):
                ind = max(0, ind - 1)
                out.append('    ' * ind + 'else:')
                ind += 1
                continue
            elif head == 'else':
                out.append(pad + 'else:')
            elif re.match(r'if\s*\(', head):
                out.append(pad + 'if %s:' % выр(re.sub(r'if\s*\((.*)\)', r'\1', head)))
            elif re.match(r'while\s*\(', head):
                out.append(pad + 'while %s:' % выр(re.sub(r'while\s*\((.*)\)', r'\1', head)))
            else:
                out.append(pad + '# ' + head)
            ind += 1
            continue
        стр = стр.rstrip(';').strip()
        m = re.match(r'cin\s*>>\s*(\w+)$', стр)
        if m:
            out.append(pad + '%s = input()' % m.group(1)); continue
        if стр.startswith('cout'):
            parts = [выр(p.strip()) for p in стр[4:].split('<<') if p.strip() and p.strip() != 'endl']
            out.append(pad + 'print(%s, sep="")' % ', '.join(parts)); continue
        m = re.match(r'^(\w+)\+\+$', стр)
        if m:
            out.append(pad + '%s += 1' % m.group(1)); continue
        m = re.match(r'^(\w+)--$', стр)
        if m:
            out.append(pad + '%s -= 1' % m.group(1)); continue
        m = re.match(r'(int|float|double|bool|string|auto|char)\s+(\w+)\s*=\s*(.+)$', стр)
        if m:
            out.append(pad + '%s = %s' % (m.group(2), выр(m.group(3)))); continue
        m = re.match(r'(int|float|double|bool|string|auto|char)\s+(\w+)$', стр)
        if m:
            out.append(pad + '%s = 0' % m.group(2)); continue
        m = re.match(r'(int|float|double|void|bool|string|auto)\s+(\w+)\s*\(([^)]*)\)$', стр)
        if m:
            args = [a.strip().split()[-1] for a in m.group(3).split(',') if a.strip()]
            out.append(pad + 'def %s(%s):' % (m.group(2), ', '.join(args)))
            ind += 1
            continue
        out.append(pad + выр(стр))
    return '\n'.join(out)

if __name__ == '__main__':
    код = open(sys.argv[1], encoding='utf-8').read()
    питон = перевести_cpp(код)
    print("=== ПЕРЕВЕДЕНО ===")
    print(питон)
    print("=== ВЫПОЛНЯЮ ===")
    exec(питон)
