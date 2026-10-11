# 시연·홍보 영상 대본 (실제 프로그램 조작 녹화용) — 대본 원문: 영상작업/대본_초안.md
# kind: card(검은 화면 큰 글씨, 앱은 뒤에서 준비) · demo(실제 앱 조작, 위쪽 이름표)
# card: lines=큰 글씨 줄들(**로 감싼 줄은 강조 색), sub=작은 출처 글씨
# act: tools/video3/rec3.mjs 의 ACT[이름] (그 장면에서 실제로 할 조작)
VOICE = 'ko-KR-SunHiNeural'
RATE = '+8%'
SEG = [
    # ① 문제 제기
    dict(id='p1', kind='card', lines=['새 업무를 맡은 첫날', '전임자는 떠났고, 남은 건 메모 몇 장'],
         voice='새 업무를 맡은 첫날. 전임자는 이미 떠났고, 남은 건 개인 메모 몇 장뿐입니다.', act='prep'),
    dict(id='p2', kind='card', lines=['**72.2%**', '전임자·개인 경험에 의존'], sub='부산소방 조직혁신 TF 설문 (2026. 9., 1,383명)',
         voice='부산소방 직원의 72.2퍼센트가, 업무를 전임자와 개인 경험에 의존한다고 답했습니다.'),
    dict(id='p3', kind='card', lines=['**33건**', '절차 누락·오류 감사 지적'], sub='2026. 7. 부산시 종합감사',
         voice='그 빈틈은 감사 지적으로 돌아옵니다. 재공고 누락, 심사기준 위반, 기록물 임의 폐기.'),
    # ② 제목
    dict(id='title', kind='card', title=True, lines=['업무 내비게이터', '길을 몰라도, 업무의 끝까지'],
         voice='그래서 만들었습니다. 길을 몰라도 업무의 끝까지, 업무 내비게이터.'),
    # ③ 실제 시연
    dict(id='d1', kind='demo', label='아침엔 오늘 챙길 일부터', act='morning',
         voice='아침에 켜면, 오늘 챙길 마감부터 알려 줍니다. 지금부터 연습 업무, 소모품 구매 계약으로 직접 따라가 보겠습니다.'),
    dict(id='d2', kind='demo', label='지금 어디까지 왔는지', act='open',
         voice='업무는 단계와 할 일로 된 체크리스트입니다. 지금 어느 단계인지, 몇 퍼센트 왔는지 한눈에 보입니다.'),
    dict(id='d4', kind='demo', label='놓치기 쉬운 것은 맨 위에', act='tip',
         voice='할 일마다 전임자의 노하우가 붙어 있습니다. 놓치기 쉬운 것은 맨 위 빨간 상자에, 근거 법령은 맨 아래에. 쪼개기 계약 금지처럼, 감사에서 지적되는 바로 그 지점을 미리 짚어 줍니다.'),
    dict(id='d3', kind='demo', label='체크하면 다음 할 일로', act='check',
         voice='할 일을 체크하면, 다음 할 일로 자연스럽게 넘어갑니다.'),
    dict(id='d6', kind='demo', label='갈림길은 버튼 하나로', act='branch',
         voice='금액에 따라 절차가 갈리는 곳에서는 버튼 하나면 됩니다. 1인 견적을 고르면, 해당 없는 절차가 사유와 함께 정리됩니다.'),
    dict(id='d5', kind='demo', label='서식·예시는 그 자리에서', act='forms',
         voice='필요한 서식은 그 자리에서 바로 열고, 작성 예시와 사진도 넘겨 가며 봅니다.'),
    dict(id='d7', kind='demo', label='한 일은 기록으로, 마감은 미리', act='result',
         voice='처리한 내용은 할 일마다 기록으로 남고, 마감일을 정해 두면 놓치기 전에 알려 줍니다.'),
    dict(id='d8', kind='demo', label='보고서는 바로', act='report',
         voice='보고가 필요할 땐, 진행상황을 공무원 보고서 형식으로 바로 뽑아 냅니다. 체크리스트 그대로 인쇄해 증빙으로 남길 수도 있습니다.'),
    dict(id='d9', kind='demo', label='파일 하나로 인수인계', act='handover',
         voice='업무를 마치면 레퍼런스로 남아, 다음 담당자의 출발점이 됩니다. 체크리스트와 업무팁, 서식, 기록까지. 파일 하나만 넘겨주면 인수인계가 끝납니다.'),
    # ④ 안전·가벼움 (클라이맥스)
    dict(id='s1', kind='card', climax=True, lines=['**설치 0 · 서버 0**'], voice='설치도, 서버도 필요 없습니다.'),
    dict(id='s2', kind='card', climax=True, lines=['**HTML 파일 하나**', '약 4MB'], voice='4메가바이트 남짓한 HTML 파일 하나.'),
    dict(id='s3', kind='card', climax=True, lines=['**인터넷 없이**', '외부로 나가는 통신은 차단'],
         voice='인터넷 없이 내 PC 안에서만 돌아가고, 외부로 나가는 통신은 아예 막아 두었습니다.'),
    # ⑤ 마무리
    dict(id='e1', kind='card', lines=['숙달된 직원의 노하우를,', '처음 맡은 직원에게'],
         voice='숙달된 직원의 노하우를, 처음 맡은 직원에게 안전하게 전하는 길.'),
    dict(id='e2', kind='card', lines=['새 업무 앞에서,', '더 이상 혼자 헤매지 않도록'], voice='새 업무 앞에서, 더 이상 혼자 헤매지 않도록.'),
    dict(id='end', kind='card', title=True, end=True, lines=['업무 내비게이터', '지금, 연습 업무로 시작해 보세요'], sub='v1.5.6 · 부산 사하소방서 청문감사담당관',
         voice='업무 내비게이터. 지금, 연습 업무로 시작해 보세요.'),
]
