import requests
import os
import re

BASE = 'http://127.0.0.1:8000'
IMAGE = os.path.join('Dataset','test','glaucoma','EyePACS-TRAIN-RG-3223.jpg')

s = requests.Session()

# helper to get csrf token from cookies
def get_csrf(session):
    return session.cookies.get('csrftoken','')

print('1) Register doctor user')
resp = s.get(BASE + '/login/register/')
csrftoken = get_csrf(s)
print(' got csrf', bool(csrftoken))
reg_data = {'username':'e2e_doctor','password':'e2e_pass','email':'e2e@example.com','csrfmiddlewaretoken':csrftoken}
resp = s.post(BASE + '/login/register/', data=reg_data, headers={'Referer': BASE + '/login/register/'})
print(' register status', resp.status_code)

print('2) Login as doctor')
resp = s.get(BASE + '/login/')
csrftoken = get_csrf(s)
login_data = {'username':'e2e_doctor','password':'e2e_pass','csrfmiddlewaretoken':csrftoken}
resp = s.post(BASE + '/login/', data=login_data, headers={'Referer': BASE + '/login/'}, allow_redirects=True)
print(' login status', resp.status_code)

print('3) Upload image')
if not os.path.exists(IMAGE):
    print(' sample image not found at', IMAGE)
    raise SystemExit(1)
resp = s.get(BASE + '/upload/')
csrftoken = get_csrf(s)
with open(IMAGE,'rb') as f:
    files = {'image': ('sample.jpg', f, 'image/jpeg')}
    data = {'csrfmiddlewaretoken': csrftoken}
    resp = s.post(BASE + '/upload/', files=files, data=data, headers={'Referer': BASE + '/upload/'}, allow_redirects=True)
print(' upload status', resp.status_code)

print('4) Check doctor dashboard for latest result and PDF link')
resp = s.get(BASE + '/detect/dashboard/')
content = resp.text
m = re.search(r'/report/\?case=(\d+)&result=([^&]+)&prob=([0-9.]+)', content)
if m:
    case_id, result_label, prob = m.group(1), m.group(2), m.group(3)
    print(' found case', case_id, result_label, prob)
    pdf_url = BASE + f'/report/?case={case_id}&result={result_label}&prob={prob}'
    r2 = s.get(pdf_url)
    print(' pdf status', r2.status_code, 'content-type', r2.headers.get('Content-Type'))
else:
    print(' no report link found; show snippet:')
    print(content[:800])

print('5) Login as admin and export CSV')
# logout first
s.get(BASE + '/login/logout/')
resp = s.get(BASE + '/login/')
csrftoken = get_csrf(s)
admin_login = {'username':'admin','password':'adminpass','csrfmiddlewaretoken':csrftoken}
resp = s.post(BASE + '/login/', data=admin_login, headers={'Referer': BASE + '/login/'}, allow_redirects=True)
print(' admin login status', resp.status_code)
# download CSV
csv_url = BASE + '/dashboard/admin/admin-dashboard/download/'
r = s.get(csv_url)
print(' csv status', r.status_code, 'content-type', r.headers.get('Content-Type'))
if r.status_code==200:
    print(' csv length', len(r.content))

print('E2E test completed')
