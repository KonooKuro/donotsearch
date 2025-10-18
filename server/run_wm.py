import sys
sys.path.append('server/src')
from watermark_JunyiShen.wm_embedfile_v1 import METHOD_INSTANCE as WM

secret = 'lin-phase2-demo'

with open('/tmp/in.pdf', 'rb') as f:
    data = f.read()

out = WM.add_watermark(data, secret=secret, key='')  # key may be empty
with open('/tmp/out.pdf', 'wb') as f:
    f.write(out)

with open('/tmp/out.pdf', 'rb') as f:
    recovered = WM.read_secret(f.read())

print('READ:', recovered)
print('RESULT:', 'OK' if recovered == secret else 'MISMATCH')
