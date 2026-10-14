# 내 정보 시험 대본 → steps3.json
# 처음 켤 때 창(이름만 꼭·[나중에]·업무 없을 때 안내) · 오른쪽 위 이름 첫 글자 동그라미 → 내 정보 고치기 ·
# 환경설정 일반 순서(내 정보 → 음성안내 → 화면 → 주소록) · [고치기] → [취소]/[저장] · Esc는 고치기만 취소 · 진행상황 출력 작성자 창도 같은 칸
# 실행: (tools 폴더에서) python mk_me_test.py && node cdp3.mjs <index.html 경로>
import json, os
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);"
     "const me=()=>JSON.stringify(app._collabMe());const av=()=>{const b=$('meAvatarBtn');return b?(b.textContent.trim()||'(사람 아이콘)')+(b.querySelector('.me-dot')?'+점':''):'없음'};"
     "const groups=()=>[...document.querySelectorAll('#prefsPanel .prefs-group-title')].map(t=>t.childNodes[0].textContent.trim()).join(' → ');")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(b): return P + b + E
S = []
def step(label, body): S.append({"label": label, "js": J(body)})
def pt(expr, dx="Math.min(40,b.width/2)"): S.append({"pt": True, "js": J("const el=" + expr + ";if(!el)throw new Error('대상 없음');const b=el.getBoundingClientRect();return JSON.stringify([b.left+" + dx + ",b.top+b.height/2])")})
def click(expr): pt(expr); S.append({"clickpt": 1})
def typ(t): S.append({"text": t})
def key(k, vk=0, ktext=None): S.append({"key": k, "vk": vk, **({"ktext": ktext} if ktext else {})})

# ① 처음 켤 때 (새 프로필: 업무 없음 · 내 정보 없음)
step("A 처음 켤 때 창", "await W(800);const m=$('welcomeModal');return '창='+!!(m&&m.classList.contains('show'))+' | 업무 없음 안내='+!!(m&&m.querySelector('.welcome-empty'))+' | 칸='+[...m.querySelectorAll('.me-fields label')].map(l=>l.childNodes[0].textContent.trim()).join(',')+' | 동그라미='+av()+' | 마감 알림 먼저 안 뜸='+!(document.getElementById('deadlineBanner')||{}).classList?.contains('show')")
S.append({"shot": "me_welcome.png"})
click("$('welcomeSave')")
step("B 이름 없이 [시작하기] → 안내, 창 그대로", "await W(200);return '창='+!!$('welcomeModal')+' | 안내='+(document.querySelector('#welcomeFields .me-err-msg')||{}).textContent+' | 이름 칸 빨강='+$('welcomeName').classList.contains('me-err')")
click("$('welcomeName')")
typ("홍길동")
click("$('welcomeRank')")
typ("소방위")
click("$('welcomeDept')")
typ("사하소방서 예방과")
key("Enter", 13)
step("C Enter → 저장 · 창 닫힘 · 동그라미 「홍」", "await W(500);return '창='+!!$('welcomeModal')+' | 내 정보='+me()+' | 동그라미='+av()+' | 말풍선='+$('meAvatarBtn').title")
S.append({"shot": "me_avatar.png"})
step("D 다시 열어도 처음 창 안 나옴", "location.reload();return 'ok'")
step("D2", "await W(4000);return '창='+!!$('welcomeModal')+' | 동그라미='+av()")
# ② 동그라미 → 환경설정 일반 맨 위 내 정보를 바로 고치는 상태로
click("$('meAvatarBtn')")
step("E 동그라미 → 환경설정 일반 · 내 정보 고치는 중", "await W(400);return '설정 창='+$('prefsModal').classList.contains('show')+' | 순서='+groups()+' | 고치는 중='+!!$('prefsMeName')+' | 초점='+(document.activeElement||{}).id+' | 안내='+(document.querySelector('#prefsMeGroup .me-note')||{}).textContent")
S.append({"shot": "me_prefs_edit.png"})
# 취소: 바뀐 것 없음
click("$('prefsMeRank')")
key("End", 35); typ("X")
click("$('prefsMeCancel')")
step("F [취소] → 그대로 · 카드 모양", "await W(200);return '내 정보='+me()+' | 카드='+(document.querySelector('#prefsMeGroup .me-card-txt')||{}).textContent.replace(/\\s+/g,' ').trim()")
# 고치기 → 저장
click("[...document.querySelectorAll('#prefsMeGroup button')].find(b=>b.textContent.trim()==='고치기')")
click("$('prefsMePhone')")
typ("4521")
click("$('prefsMeSave')")
step("G [고치기] → [저장]", "await W(300);return '내 정보='+me()+' | 카드='+(document.querySelector('#prefsMeGroup .me-card-txt')||{}).textContent.replace(/\\s+/g,' ').trim()")
S.append({"shot": "me_prefs_card.png"})
# Esc는 고치기만 취소(설정 창은 그대로)
click("[...document.querySelectorAll('#prefsMeGroup button')].find(b=>b.textContent.trim()==='고치기')")
click("$('prefsMeName')")
key("Escape", 27)
step("H Esc → 고치기만 취소 · 설정 창 그대로", "await W(200);return '설정 창='+$('prefsModal').classList.contains('show')+' | 고치는 중='+!!$('prefsMeName')")
# 이름 비우고 저장 → 안내
click("[...document.querySelectorAll('#prefsMeGroup button')].find(b=>b.textContent.trim()==='고치기')")
step("I0 이름 지우기", "$('prefsMeName').value='';return 'ok'")
click("$('prefsMeSave')")
step("I 이름 없이 저장 → 안내 · 바뀌지 않음", "await W(200);return '안내='+(document.querySelector('#prefsMeFields .me-err-msg')||{}).textContent+' | 내 정보 이름='+app._collabMe().name")
step("J 메뉴로 열면 카드 모양(고치는 중 아님)", "app.closeModal('prefsModal');await W(300);app.openPreferences('general');await W(300);const r='고치는 중='+!!$('prefsMeName')+' | 순서='+groups();app.closeModal('prefsModal');await W(200);return r")
# ③ 진행상황 출력 작성자 창도 같은 칸
step("K 작성자 창", "app._askAuthor(()=>{}, {edit:true});await W(300);const m=$('authorInfoModal');return '창='+!!m+' | 같은 칸='+!!m.querySelector('.me-fields')+' | 이름='+$('authorName').value+' | 연락처='+$('authorPhone').value")
S.append({"shot": "me_author.png"})
click("$('authorRank')")
key("End", 35); typ(" (팀장)")
key("Enter", 13)
step("K2 작성자 창에서 Enter 저장 → 내 정보·동그라미 말풍선 같이 바뀜", "await W(300);return '창='+!!$('authorInfoModal')+' | 내 정보='+me()+' | 말풍선='+$('meAvatarBtn').title")
# ④ [나중에]
step("L0 처음 상태로", "['collabMyName','collabMyDept','collabMyRank','collabMyPhone','welcomeShown','authorInfoSet'].forEach(k=>localStorage.removeItem(k));app.renderMeAvatar();app.checkWelcome();await W(300);return '창='+!!$('welcomeModal')")
click("$('welcomeCancel')")
step("L [나중에] → 창 닫힘 · 동그라미에 점", "await W(300);return '창='+!!$('welcomeModal')+' | 동그라미='+av()")
step("L2 다시 열어도 처음 창 안 나옴", "location.reload();return 'ok'")
step("L3", "await W(4000);return '창='+!!$('welcomeModal')+' | 동그라미='+av()")
# ⑤ 업무가 있으면 「업무 없음」 안내는 안 나옴
step("M 업무가 있을 때", "await app.insertPracticeWorkflows();await W(1200);localStorage.removeItem('welcomeShown');app.checkWelcome();await W(300);const m=$('welcomeModal');const r='창='+!!m+' | 업무 없음 안내='+!!(m&&m.querySelector('.welcome-empty'));app._welcomeClose();return r")
step("N 다크 모드", "document.documentElement.classList.add('dark-mode');app._collabSetMe({name:'홍길동',rank:'소방위',dept:'사하소방서 예방과',phone:'4521'});app.openMyInfo();await W(400);return 'ok'")
S.append({"shot": "me_dark.png"})
step("정리", "app.closeModal('prefsModal');document.documentElement.classList.remove('dark-mode');app.allData.workflows=app.allData.workflows.filter(w=>!/^\\[연습\\]/.test(w.title));app.saveData();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
