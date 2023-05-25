import requests

payload = {'Flag': '0'}

r = requests.post(' http://127.0.0.1:5001/mh/MH2CE', data=payload)

print(r.text)
print(r.json())
print(r.json().get('c2'))

print(type(r.json()))

c2 = '1c6985bbb92d7c3d24eeea97ce9a2aa11e4a63c89a2ecfc49fda641d169072d4c4bc732b70964c1a064aeb3160845482faf26594067eea5d401ff62b948a0181dd04317e8f5db026953a680f1cb82d68f4974466213e2769c8da65ecc606056129dffcfa84b76ac6b83bd2accb9317b5818ec6b52ee8c36a57bb3671ad613808666cdda4e14e924fa64c77030cf5a27fd4b1e428ce94114a5b2894ca'
c2 = ''