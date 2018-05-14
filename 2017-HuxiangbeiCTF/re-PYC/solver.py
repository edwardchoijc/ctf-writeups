table = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
print len(table)


def decode(s):
    a = s >> 16
    b = (s >> 8) & 0xFF
    c = s & 0xff
    sa = binary(a)
    sb = binary(b)
    sc = binary(c)
    return table[int(sa[2:], 2)] + table[int(sb[4:] + sa[:2], 2)] + table[int(sc[6:] + sb[:4], 2)] + table[int(sc[:6], 2)]


def binary(b):
    ret = ''
    for i in [128, 64, 32, 16, 8, 4, 2, 1]:
        ret += '1' if b & i else '0'
    return ret


key_enc = open('key.enc', 'rb')
key_enc = key_enc.read()
ans = ""
for i in xrange(0, len(key_enc), 3):
    ans += decode(int(key_enc[i:i + 3].encode('hex'), 16))
print ans
ans = ''.join(map(lambda c: table[(table.index(c) + 63) % 64], ans))
print ans
