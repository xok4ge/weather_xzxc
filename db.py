import psycopg2
with open('24.txt', mode='r', encoding='utf-8') as file:
    q = file.read().strip()
    maxis = []
    m = 0
    wc = 0
    for a in range(len(q)-1):
        if q[a]+q[a+1] == 'WW':
            wc += 1
        if wc == 101:
            maxis.append(m)
            m, wc = 2, 0
        m += 1
print(max(maxis))
