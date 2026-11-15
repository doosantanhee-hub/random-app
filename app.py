import random
import time
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. 페이지 설정 및 아케이드/야구장 커스텀 CSS
# ==========================================
st.set_page_config(
    page_title="야구장 매점 타이쿤 ⚾",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;700;900&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.block-container {
    padding-top: 1.1rem !important;
    padding-bottom: 1.5rem !important;
    max-width: 1280px;
}

/* 전광판 스타일 */
.scoreboard-wrap {
    background: linear-gradient(180deg, #0b132b 0%, #1c2541 100%);
    border: 4px solid #3a506b;
    border-radius: 14px;
    padding: 12px 18px;
    color: #ffffff;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.35);
    margin-bottom: 10px;
}

.sb-title {
    font-family: 'Black Han Sans', sans-serif;
    color: #ffd166;
    font-size: 1.15rem;
    letter-spacing: 1px;
}

.sb-score-box {
    background: #050811;
    border: 2px solid #2b3a55;
    border-radius: 10px;
    padding: 6px 14px;
    text-align: center;
    font-family: 'Share Tech Mono', monospace;
}

.sb-team {
    font-size: 0.85rem;
    color: #94a3b8;
    font-weight: 700;
}

.sb-num {
    font-size: 1.8rem;
    font-weight: 900;
    color: #4ade80;
    line-height: 1.1;
}

.sb-num.away {
    color: #f87171;
}

.sbo-row {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.95rem;
    font-weight: 700;
    line-height: 1.35;
}

.dot-s { color: #facc15; }
.dot-b { color: #4ade80; }
.dot-o { color: #ef4444; }
.dot-off { color: #334155; }

.live-ticker {
    background: #050811;
    border-left: 4px solid #f59e0b;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 0.95rem;
    font-weight: 700;
    color: #fef08a;
    margin-top: 8px;
}

/* 주자 다이아몬드 미니 그래픽 */
.diamond-box {
    position: relative;
    width: 64px;
    height: 64px;
    margin: 0 auto;
}
.base {
    position: absolute;
    width: 16px;
    height: 16px;
    transform: rotate(45deg);
    border: 2px solid #94a3b8;
    background: #1e293b;
}
.base.active {
    background: #facc15;
    border-color: #fef08a;
    box-shadow: 0 0 10px #facc15;
}
.base-2 { top: 4px; left: 24px; }
.base-3 { top: 24px; left: 4px; }
.base-1 { top: 24px; left: 44px; }
.base-home { top: 44px; left: 24px; border-color: #64748b; background: #cbd5e1; }

/* HUD 상태바 */
.hud-bar {
    background: #f8fafc;
    border: 2px solid #cbd5e1;
    border-radius: 12px;
    padding: 10px 14px;
    margin-bottom: 10px;
}
.hud-item-label {
    font-size: 0.78rem;
    color: #64748b;
    font-weight: 700;
}
.hud-item-val {
    font-size: 1.25rem;
    font-weight: 900;
    color: #0f172a;
}

/* 손님 카드 */
.cust-card {
    background: #ffffff;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    padding: 10px 12px;
    margin-bottom: 8px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.05);
}
.cust-card.urgent {
    border-color: #ef4444;
    background: #fef2f2;
}
.cust-card.empty {
    background: #f8fafc;
    border: 2px dashed #cbd5e1;
    color: #94a3b8;
    text-align: center;
    padding: 24px 10px;
}

/* 조리대 카드 */
.cook-card {
    background: #fffbeb;
    border: 2px solid #fcd34d;
    border-radius: 12px;
    padding: 10px 12px;
    margin-bottom: 8px;
}
.cook-card.ready {
    background: #ecfdf5;
    border-color: #10b981;
}
.cook-card.burned {
    background: #1f2937;
    border-color: #ef4444;
    color: #f9fafb;
}

/* 파울볼 긴급 경고 */
@keyframes pulseAlert {
    0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.8); }
    50% { transform: scale(1.015); box-shadow: 0 0 22px 6px rgba(239, 68, 68, 0.6); }
    100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.8); }
}
.foul-banner {
    background: linear-gradient(90deg, #dc2626, #ea580c, #dc2626);
    color: white;
    padding: 10px 16px;
    border-radius: 12px;
    font-weight: 900;
    font-size: 1.15rem;
    text-align: center;
    animation: pulseAlert 0.65s infinite;
    margin-bottom: 8px;
}

/* 파울볼 놓쳤을 때 흔들림 페널티 */
@keyframes shakeCounter {
    0%, 100% { transform: translateX(0); }
    20% { transform: translateX(-10px) rotate(-1deg); }
    40% { transform: translateX(10px) rotate(1deg); }
    60% { transform: translateX(-8px); }
    80% { transform: translateX(8px); }
}
.shake-penalty {
    animation: shakeCounter 0.35s infinite;
    background: #450a0a;
    color: #fecaca;
    border: 2px solid #ef4444;
    border-radius: 12px;
    padding: 10px;
    text-align: center;
    font-weight: 900;
    margin-bottom: 8px;
}

/* 피버 타임 야간 경기장 조명 & 관중 율동 애니메이션 */
@keyframes cheerDance {
    0%, 100% { transform: translateY(0) rotate(-6deg) scale(1); }
    50% { transform: translateY(-7px) rotate(6deg) scale(1.12); }
}
.crowd-wave {
    display: inline-block;
    font-size: 1.45rem;
    animation: cheerDance 0.45s infinite ease-in-out;
    letter-spacing: 3px;
}

.fever-banner {
    background: linear-gradient(90deg, #7e22ce, #db2777, #f59e0b, #10b981, #7e22ce);
    background-size: 300% 300%;
    animation: feverGradient 2s ease infinite;
    color: #ffffff;
    border-radius: 12px;
    padding: 8px 14px;
    text-align: center;
    font-weight: 900;
    font-size: 1.05rem;
    margin-bottom: 8px;
    box-shadow: 0 0 20px rgba(236, 72, 153, 0.65);
}
@keyframes feverGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* 영수증 결과창 */
.receipt-paper {
    background: #fffdf7;
    border: 2px dashed #475569;
    border-radius: 8px;
    padding: 24px 28px;
    max-width: 540px;
    margin: 0 auto;
    font-family: 'Share Tech Mono', 'Noto Sans KR', monospace;
    color: #1e293b;
    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
}
.receipt-header {
    text-align: center;
    border-bottom: 2px dashed #94a3b8;
    padding-bottom: 12px;
    margin-bottom: 14px;
}
.receipt-row {
    display: flex;
    justify-content: space-between;
    padding: 5px 0;
    font-size: 1.02rem;
}
.receipt-total {
    border-top: 2px dashed #94a3b8;
    border-bottom: 2px dashed #94a3b8;
    margin-top: 10px;
    padding: 10px 0;
    font-size: 1.3rem;
    font-weight: 900;
    color: #b91c1c;
    display: flex;
    justify-content: space-between;
}
.title-badge {
    background: linear-gradient(135deg, #fef3c7, #fde68a);
    border: 2px solid #f59e0b;
    border-radius: 10px;
    padding: 12px;
    text-align: center;
    margin-top: 14px;
}
</style>
"""

FEVER_BG_CSS = """
<style>
.stApp {
    background: radial-gradient(circle at 20% 10%, rgba(250, 204, 21, 0.22), transparent 40%),
                radial-gradient(circle at 80% 10%, rgba(236, 72, 153, 0.22), transparent 40%),
                linear-gradient(180deg, #1e1b4b 0%, #311042 100%) !important;
}
.stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label {
    color: #f8fafc !important;
}
.cust-card, .cook-card, .hud-bar {
    color: #0f172a !important;
}
.cust-card p, .cook-card p, .hud-bar p, .hud-item-val {
    color: #0f172a !important;
}
</style>
"""

NORMAL_BG_CSS = """
<style>
.stApp {
    background: linear-gradient(180deg, #ecfdf5 0%, #f1f5f9 100%) !important;
}
</style>
"""

# ==========================================
# 2. 게임 상수 및 메뉴 설정
# ==========================================
MENUS = {
    "생맥주": {
        "icon": "🍺",
        "price": 4000,
        "cook_time": 0,
        "can_burn": False,
        "weight": 35,
    },
    "나초 & 치즈": {
        "icon": "🧀",
        "price": 5000,
        "cook_time": 0,
        "can_burn": False,
        "weight": 30,
    },
    "순살치킨": {
        "icon": "🍗",
        "price": 9000,
        "cook_time": 3,
        "can_burn": True,
        "burn_limit": 7,
        "weight": 20,
    },
    "크림새우 & 떡볶이 세트": {
        "icon": "🍤",
        "price": 14000,
        "cook_time": 5,
        "can_burn": False,
        "weight": 15,
    },
}

CUSTOMER_PROFILES = [
    ("🧔", "치맥 열혈팬"),
    ("👩", "직관 10년차"),
    ("🧑", "응원단장 지망생"),
    ("👧", "유니폼 꼬마팬"),
    ("👨", "퇴근 후 직관러"),
    ("👩‍🦱", "먹방 유튜버"),
]

# 이닝별 목표 매출(골드) 및 제한 시간(초)
INNING_CONFIG = {
    1: {"target": 22000, "duration": 35},
    2: {"target": 32000, "duration": 35},
    3: {"target": 42000, "duration": 35},
    4: {"target": 52000, "duration": 38},
    5: {"target": 62000, "duration": 38},
    6: {"target": 74000, "duration": 38},
    7: {"target": 86000, "duration": 40},
    8: {"target": 98000, "duration": 40},
    9: {"target": 115000, "duration": 42},
}


# ==========================================
# 3. Web Audio API 신시사이저 (외부 파일 불필요)
# ==========================================
def render_sound_engine(sound_id: int, sound_type: str, is_fever: bool, muted: bool):
    """HTML5 Web Audio API로 효과음 및 피버 타임 8비트 응원가 비트를 직접 생성해 재생"""
    js_fever = "true" if (is_fever and not muted) else "false"
    js_muted = "true" if muted else "false"

    html_code = f"""
    <script>
    (function() {{
        const SOUND_ID = {sound_id};
        const SOUND_TYPE = "{sound_type}";
        const IS_FEVER = {js_fever};
        const IS_MUTED = {js_muted};

        const parentWin = window.parent || window;
        if (!parentWin._baseballAudioCtx) {{
            const AudioCtx = parentWin.AudioContext || parentWin.webkitAudioContext;
            if (AudioCtx) {{
                parentWin._baseballAudioCtx = new AudioCtx();
            }}
        }}
        const ctx = parentWin._baseballAudioCtx;
        if (!ctx) return;

        // 사용자 클릭 시 오디오 컨텍스트 활성화
        const unlockAudio = () => {{
            if (ctx.state === 'suspended') {{
                ctx.resume();
            }}
        }};
        unlockAudio();
        try {{
            parentWin.document.addEventListener('pointerdown', unlockAudio, {{ once: true }});
        }} catch(e) {{}}

        // 기존 피버 BGM 루프 정리
        if (parentWin._feverTimer) {{
            clearInterval(parentWin._feverTimer);
            parentWin._feverTimer = null;
        }}

        if (IS_MUTED) return;

        function playTone(freq, type, startTime, duration, vol=0.14) {{
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, startTime);
            gain.gain.setValueAtTime(vol, startTime);
            gain.gain.exponentialRampToValueAtTime(0.001, startTime + duration);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(startTime);
            osc.stop(startTime + duration);
        }}

        function playNoise(startTime, duration, vol=0.18) {{
            const bufferSize = ctx.sampleRate * duration;
            const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
            const data = buffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) {{
                data[i] = Math.random() * 2 - 1;
            }}
            const noise = ctx.createBufferSource();
            noise.buffer = buffer;
            const gain = ctx.createGain();
            gain.gain.setValueAtTime(vol, startTime);
            gain.gain.exponentialRampToValueAtTime(0.001, startTime + duration);
            noise.connect(gain);
            gain.connect(ctx.destination);
            noise.start(startTime);
        }}

        // 새로운 효과음 이벤트가 있을 때만 단발성 사운드 재생
        if (parentWin._lastPlayedSoundId !== SOUND_ID) {{
            parentWin._lastPlayedSoundId = SOUND_ID;
            const now = ctx.currentTime;

            if (SOUND_TYPE === "foul_alert") {{
                // 경쾌한 배트 타격음 + 긴급 경고 사이렌
                playNoise(now, 0.08, 0.3);
                playTone(920, "triangle", now, 0.09, 0.25);
                playTone(880, "sawtooth", now + 0.12, 0.16, 0.16);
                playTone(620, "sawtooth", now + 0.29, 0.16, 0.16);
                playTone(880, "sawtooth", now + 0.46, 0.18, 0.16);
            }} else if (SOUND_TYPE === "foul_catch") {{
                // 파울볼 캐치 성공 팡파르
                playTone(523.25, "square", now, 0.09, 0.15);
                playTone(659.25, "square", now + 0.09, 0.09, 0.15);
                playTone(783.99, "square", now + 0.18, 0.09, 0.15);
                playTone(1046.5, "square", now + 0.27, 0.28, 0.18);
            }} else if (SOUND_TYPE === "foul_miss") {{
                // 매점 충돌 페널티
                playNoise(now, 0.28, 0.25);
                playTone(180, "sawtooth", now, 0.22, 0.2);
                playTone(120, "sawtooth", now + 0.18, 0.25, 0.2);
            }} else if (SOUND_TYPE === "serve") {{
                // 서빙 성공 코인음
                playTone(987.77, "sine", now, 0.07, 0.14);
                playTone(1318.51, "sine", now + 0.07, 0.14, 0.14);
            }} else if (SOUND_TYPE === "burn") {{
                // 음식 탄 경고음
                playTone(220, "sawtooth", now, 0.14, 0.15);
                playTone(165, "sawtooth", now + 0.15, 0.2, 0.15);
            }} else if (SOUND_TYPE === "fever_start") {{
                // 홈런/피버 발동 사이렌
                [523, 659, 784, 1046, 1318].forEach((f, idx) => {{
                    playTone(f, "square", now + idx * 0.06, 0.14, 0.14);
                }});
            }} else if (SOUND_TYPE === "inning_clear") {{
                // 이닝 클리어
                [440, 554, 659, 880].forEach((f, idx) => {{
                    playTone(f, "triangle", now + idx * 0.09, 0.18, 0.16);
                }});
            }} else if (SOUND_TYPE === "gameover") {{
                // 경기 종료 휘슬
                playTone(440, "triangle", now, 0.2, 0.16);
                playTone(392, "triangle", now + 0.22, 0.2, 0.16);
                playTone(349, "triangle", now + 0.44, 0.4, 0.16);
            }}
        }}

        // 피버 타임 전용 8비트 야구장 응원가 비트 루프
        if (IS_FEVER) {{
            const cheerMelody = [
                523.25, 523.25, 659.25, 783.99,
                659.25, 783.99, 1046.50, 0,
                880.00, 880.00, 783.99, 659.25,
                587.33, 659.25, 523.25, 0
            ];
            const bassLine = [
                130.81, 196.00, 130.81, 196.00,
                164.81, 196.00, 164.81, 196.00,
                174.61, 220.00, 174.61, 220.00,
                196.00, 246.94, 130.81, 196.00
            ];
            let step = 0;
            const playCheerBeat = () => {{
                if (ctx.state !== 'running') return;
                const t = ctx.currentTime;
                const note = cheerMelody[step % cheerMelody.length];
                const bass = bassLine[step % bassLine.length];
                if (note > 0) {{
                    playTone(note, "square", t, 0.14, 0.08);
                }}
                playTone(bass, "triangle", t, 0.15, 0.10);
                if (step % 2 === 1) {{
                    playNoise(t, 0.05, 0.06); // 응원 막대 박수 비트
                }}
                step++;
            }};
            playCheerBeat();
            parentWin._feverTimer = setInterval(playCheerBeat, 175);
        }}
    }})();
    </script>
    """
    components.html(html_code, height=0, width=0)


# ==========================================
# 4. 게임 상태 초기화 및 헬퍼 함수
# ==========================================
def trigger_sound(sound_type: str):
    st.session_state.sound_id += 1
    st.session_state.sound_type = sound_type


def spawn_customer(now: float, is_fever: bool):
    if len(st.session_state.customers) >= 4:
        return
    menu_names = list(MENUS.keys())
    weights = [MENUS[m]["weight"] for m in menu_names]
    chosen_menu = random.choices(menu_names, weights=weights, k=1)[0]
    avatar, role = random.choice(CUSTOMER_PROFILES)

    # 피버 타임엔 손님이 더 자주 몰리지만 기본 인내심도 넉넉히 부여
    base_patience = random.randint(15, 20) if not is_fever else random.randint(13, 17)
    st.session_state.customer_seq += 1
    st.session_state.customers.append(
        {
            "id": st.session_state.customer_seq,
            "avatar": avatar,
            "role": role,
            "menu": chosen_menu,
            "spawn_time": now,
            "max_patience": base_patience,
        }
    )


def init_inning(inning: int, now: float):
    st.session_state.inning = inning
    st.session_state.inning_gold = 0
    st.session_state.inning_start_time = now
    st.session_state.customers = []
    st.session_state.foul_active = False
    st.session_state.foul_deadline = 0.0
    st.session_state.stun_until = 0.0
    # 이닝 시작 시 손님 2명 즉시 입장
    spawn_customer(now, False)
    spawn_customer(now, False)


def start_new_game():
    now = time.time()
    st.session_state.phase = "playing"
    st.session_state.victory = False
    st.session_state.total_gold = 0
    st.session_state.combo = 0
    st.session_state.max_combo = 0
    st.session_state.fever_gauge = 0
    st.session_state.fever_until = 0.0
    st.session_state.foul_catches = 0
    st.session_state.burned_count = 0
    st.session_state.customer_seq = 0
    st.session_state.sold_counts = {m: 0 for m in MENUS}

    # 조리 슬롯 (순살치킨 2구, 크림새우&떡볶이 2구)
    st.session_state.chicken_slots = [
        {"state": "idle", "start_time": 0.0, "ready_time": 0.0},
        {"state": "idle", "start_time": 0.0, "ready_time": 0.0},
    ]
    st.session_state.shrimp_slots = [
        {"state": "idle", "start_time": 0.0, "ready_time": 0.0},
        {"state": "idle", "start_time": 0.0, "ready_time": 0.0},
    ]

    # 전광판 상태
    st.session_state.home_score = 2
    st.session_state.away_score = 2
    st.session_state.strikes = 0
    st.session_state.balls = 0
    st.session_state.outs = 0
    st.session_state.bases = [False, False, False]  # 1루, 2루, 3루
    st.session_state.ticker_msg = "⚾ 1회초 경기 시작! 첫 손님들이 매점으로 몰려옵니다!"

    st.session_state.last_sec_tick = now
    st.session_state.last_foul_end = now
    init_inning(1, now)
    trigger_sound("inning_clear")


def ensure_state():
    if "phase" not in st.session_state:
        st.session_state.phase = "start"
        st.session_state.sound_id = 0
        st.session_state.sound_type = ""
        st.session_state.sound_muted = False


# ==========================================
# 5. 실시간 게임 로직 업데이트 (1초 주기)
# ==========================================
def activate_fever(now: float, reason: str):
    st.session_state.fever_gauge = 100
    st.session_state.fever_until = now + 10.0
    st.session_state.ticker_msg = f"🔥 {reason} 10초간 피버 타임 발동!! (조리 1초 / 수익 1.5배)"
    trigger_sound("fever_start")


def advance_scoreboard(now: float, is_fever: bool):
    """전광판 실시간 경기 시뮬레이션 및 홈런/득점 시 피버 발동"""
    events = ["ball", "strike", "foul_tip", "hit", "double", "homerun", "out"]
    weights = [28, 28, 12, 13, 6, 4, 9]
    ev = random.choices(events, weights=weights, k=1)[0]

    b1, b2, b3 = st.session_state.bases

    if ev == "ball":
        st.session_state.balls += 1
        if st.session_state.balls >= 4:
            st.session_state.balls = 0
            st.session_state.strikes = 0
            # 밀어내기 진루
            if b1 and b2 and b3:
                st.session_state.home_score += 1
                st.session_state.ticker_msg = "🚶 볼넷 밀어내기 득점! 홈팀 1점 추가!"
                if not is_fever:
                    activate_fever(now, "밀어내기 득점!")
            else:
                if b1 and b2:
                    b3 = True
                if b1:
                    b2 = True
                b1 = True
                st.session_state.ticker_msg = "👀 볼넷 출루! 주자가 쌓입니다."
        else:
            st.session_state.ticker_msg = f"⚾ 볼! (B:{st.session_state.balls} S:{st.session_state.strikes})"

    elif ev == "strike":
        st.session_state.strikes += 1
        if st.session_state.strikes >= 3:
            st.session_state.strikes = 0
            st.session_state.balls = 0
            st.session_state.outs += 1
            st.session_state.ticker_msg = "🔥 삼진 아웃! 투수의 강속구가 꽂힙니다!"
        else:
            st.session_state.ticker_msg = f"⚡ 스트라이크! (B:{st.session_state.balls} S:{st.session_state.strikes})"

    elif ev == "foul_tip":
        if st.session_state.strikes < 2:
            st.session_state.strikes += 1
        st.session_state.ticker_msg = "💥 커트 파울! 팽팽한 승부가 이어집니다."

    elif ev == "hit":
        st.session_state.balls = 0
        st.session_state.strikes = 0
        runs = 1 if b3 else 0
        b3 = b2
        b2 = b1
        b1 = True
        if runs > 0:
            st.session_state.home_score += runs
            st.session_state.ticker_msg = "👏 중전 적시타!! 홈팀 득점 성공!"
            if not is_fever:
                activate_fever(now, "적시타 득점 터졌다!")
        else:
            st.session_state.ticker_msg = "🏏 깔끔한 안타! 주자 진루합니다."

    elif ev == "double":
        st.session_state.balls = 0
        st.session_state.strikes = 0
        runs = (1 if b3 else 0) + (1 if b2 else 0)
        b3 = b1
        b2 = True
        b1 = False
        if runs > 0:
            st.session_state.home_score += runs
            st.session_state.ticker_msg = f"🔥 우중간 가르는 2루타! {runs}득점!!"
            if not is_fever:
                activate_fever(now, "장타 득점 폭발!")
        else:
            st.session_state.ticker_msg = "💨 외야 깊숙한 2루타! 득점권 찬스!"

    elif ev == "homerun":
        st.session_state.balls = 0
        st.session_state.strikes = 0
        runs = 1 + sum([b1, b2, b3])
        b1, b2, b3 = False, False, False
        st.session_state.home_score += runs
        st.session_state.ticker_msg = f"🎆 초대형 {runs}점 홈런!! 구장이 떠나갈 듯 들썩입니다!!"
        if not is_fever:
            activate_fever(now, f"{runs}점 홈런 폭발!!")

    elif ev == "out":
        st.session_state.balls = 0
        st.session_state.strikes = 0
        st.session_state.outs += 1
        st.session_state.ticker_msg = "🧤 외야 뜬공 아웃!"

    if st.session_state.outs >= 3:
        st.session_state.outs = 0
        st.session_state.balls = 0
        st.session_state.strikes = 0
        b1, b2, b3 = False, False, False
        if random.random() < 0.35:
            st.session_state.away_score += 1
            st.session_state.ticker_msg = "🔄 공수 교대! 원정팀이 1점 따라붙습니다."
        else:
            st.session_state.ticker_msg = "🔄 3아웃 공수 교대! 다음 공격 준비!"

    st.session_state.bases = [b1, b2, b3]


def process_game_tick():
    if st.session_state.phase != "playing":
        return

    now = time.time()

    # 1) 피버 타임 종료 체크
    if st.session_state.fever_until > 0 and now >= st.session_state.fever_until:
        st.session_state.fever_until = 0.0
        st.session_state.fever_gauge = 0
        st.session_state.ticker_msg = "📣 피버 타임 종료! 다시 집중해서 서빙하세요!"

    is_fever = now < st.session_state.fever_until

    # 2) 파울볼 제한시간(3초) 초과 체크 -> 매점 흔들림 & 2초 정지 페널티
    if st.session_state.foul_active and now >= st.session_state.foul_deadline:
        st.session_state.foul_active = False
        st.session_state.last_foul_end = now
        st.session_state.stun_until = now + 2.0
        st.session_state.combo = 0
        trigger_sound("foul_miss")
        st.toast("💥 파울볼이 매점에 떨어졌습니다! 2초간 조리/서빙 정지 & 콤보 초기화!", icon="⚠️")

    # 3) 조리대 상태 갱신 (치킨 3초->완성->7초 후 탄다 / 크림새우 5초->완성 / 피버 시 1초)
    chicken_cook_req = 1.0 if is_fever else float(MENUS["순살치킨"]["cook_time"])
    burn_limit = float(MENUS["순살치킨"]["burn_limit"])
    for slot in st.session_state.chicken_slots:
        if slot["state"] == "cooking":
            if now - slot["start_time"] >= chicken_cook_req:
                slot["state"] = "ready"
                slot["ready_time"] = now
        elif slot["state"] == "ready":
            if now - slot["ready_time"] >= burn_limit:
                slot["state"] = "burned"
                st.session_state.combo = 0
                st.session_state.burned_count += 1
                trigger_sound("burn")
                st.toast("🔥 순살치킨이 새까맣게 탔습니다! 폐기 버튼을 누르세요! (콤보 초기화)", icon="💀")

    shrimp_cook_req = 1.0 if is_fever else float(MENUS["크림새우 & 떡볶이 세트"]["cook_time"])
    for slot in st.session_state.shrimp_slots:
        if slot["state"] == "cooking":
            if now - slot["start_time"] >= shrimp_cook_req:
                slot["state"] = "ready"
                slot["ready_time"] = now

    # 4) 손님 인내심 초과 체크
    remaining_customers = []
    for cust in st.session_state.customers:
        if now - cust["spawn_time"] >= cust["max_patience"]:
            st.session_state.combo = 0
            st.toast(f"😡 {cust['role']} 손님이 기다리다 화나서 떠났습니다! (콤보 초기화)", icon="💨")
        else:
            remaining_customers.append(cust)
    st.session_state.customers = remaining_customers

    # 5) 1초 주기 이벤트 (전광판 진행, 손님 입장, 파울볼 랜덤 발생)
    if now - st.session_state.last_sec_tick >= 0.95:
        st.session_state.last_sec_tick = now
        advance_scoreboard(now, is_fever)

        # 피버 타임에는 주문 폭주(매초 빈자리 즉시 채움), 평상시엔 약 45% 확률로 손님 입장
        if is_fever:
            spawn_customer(now, True)
            if len(st.session_state.customers) < 3:
                spawn_customer(now, True)
        else:
            if len(st.session_state.customers) == 0 or random.random() < 0.45:
                spawn_customer(now, False)

        # 파울볼 돌발 이벤트 (파울볼 진행 중이 아니고, 스턴 상태가 아니며, 직전 종료 후 4초 경과 시)
        if (
            not st.session_state.foul_active
            and now >= st.session_state.stun_until
            and (now - st.session_state.last_foul_end) >= 4.0
            and random.random() < 0.12
        ):
            st.session_state.foul_active = True
            st.session_state.foul_deadline = now + 3.0
            trigger_sound("foul_alert")

    # 6) 현재 이닝 제한 시간 종료 판정
    inning = st.session_state.inning
    cfg = INNING_CONFIG[inning]
    time_left = cfg["duration"] - (now - st.session_state.inning_start_time)
    if time_left <= 0:
        if st.session_state.inning_gold >= cfg["target"]:
            if inning < 9:
                trigger_sound("inning_clear")
                st.toast(f"🎉 {inning}회 목표 매출 달성! {inning + 1}회로 진출합니다!", icon="⚾")
                init_inning(inning + 1, now)
            else:
                st.session_state.phase = "gameover"
                st.session_state.victory = True
                trigger_sound("inning_clear")
                st.rerun()
        else:
            st.session_state.phase = "gameover"
            st.session_state.victory = False
            trigger_sound("gameover")
            st.rerun()


# ==========================================
# 6. 플레이어 액션 핸들러
# ==========================================
def complete_serving(menu_name: str) -> bool:
    """해당 메뉴를 주문한 손님 중 인내심이 가장 적게 남은 손님에게 서빙"""
    now = time.time()
    if now < st.session_state.stun_until:
        st.toast("💫 매점이 흔들려 잠시 움직일 수 없습니다!", icon="⏳")
        return False

    matching = [c for c in st.session_state.customers if c["menu"] == menu_name]
    if not matching:
        st.toast(f"❓ '{menu_name}'을(를) 주문한 손님이 없습니다!", icon="😅")
        return False

    # 가장 급한 손님 우선 서빙
    matching.sort(key=lambda c: c["max_patience"] - (now - c["spawn_time"]))
    target_cust = matching[0]
    st.session_state.customers = [c for c in st.session_state.customers if c["id"] != target_cust["id"]]

    is_fever = now < st.session_state.fever_until
    base_price = MENUS[menu_name]["price"]
    st.session_state.combo += 1
    st.session_state.max_combo = max(st.session_state.max_combo, st.session_state.combo)

    combo_tip = st.session_state.combo * 400
    earned = int((base_price + combo_tip) * (1.5 if is_fever else 1.0))

    st.session_state.inning_gold += earned
    st.session_state.total_gold += earned
    st.session_state.sold_counts[menu_name] += 1

    if not is_fever:
        st.session_state.fever_gauge = min(100, st.session_state.fever_gauge + 14)
        if st.session_state.fever_gauge >= 100:
            activate_fever(now, "피버 게이지 100% 충전!")
        else:
            trigger_sound("serve")
    else:
        trigger_sound("serve")

    return True


def handle_start_cook(slot_list_key: str, idx: int):
    now = time.time()
    if now < st.session_state.stun_until:
        st.toast("💫 매점이 흔들려 조리를 시작할 수 없습니다!", icon="⏳")
        return
    slot = st.session_state[slot_list_key][idx]
    if slot["state"] == "idle":
        slot["state"] = "cooking"
        slot["start_time"] = now
        slot["ready_time"] = 0.0


def handle_serve_cooked(slot_list_key: str, idx: int, menu_name: str):
    slot = st.session_state[slot_list_key][idx]
    if slot["state"] == "ready":
        if complete_serving(menu_name):
            slot["state"] = "idle"
            slot["start_time"] = 0.0
            slot["ready_time"] = 0.0


def handle_discard_burned(idx: int):
    slot = st.session_state.chicken_slots[idx]
    if slot["state"] == "burned":
        slot["state"] = "idle"
        slot["start_time"] = 0.0
        slot["ready_time"] = 0.0
        st.toast("🗑️ 탄 치킨을 폐기했습니다. 다시 조리할 수 있습니다.", icon="🧹")


def handle_catch_foul():
    now = time.time()
    if st.session_state.foul_active and now < st.session_state.foul_deadline:
        st.session_state.foul_active = False
        st.session_state.last_foul_end = now
        st.session_state.foul_catches += 1

        bonus = 12000
        st.session_state.inning_gold += bonus
        st.session_state.total_gold += bonus
        trigger_sound("foul_catch")
        st.toast("🧤 나이스 캐치!! 보너스 +12,000G & 피버 게이지 +45% 상승!", icon="⚾")

        if now >= st.session_state.fever_until:
            st.session_state.fever_gauge = min(100, st.session_state.fever_gauge + 45)
            if st.session_state.fever_gauge >= 100:
                activate_fever(now, "파울볼 슈퍼 캐치로 피버 폭발!")


# ==========================================
# 7. UI 렌더링 함수
# ==========================================
def render_scoreboard(now: float, is_fever: bool):
    inning = st.session_state.inning
    s = st.session_state.strikes
    b = st.session_state.balls
    o = st.session_state.outs
    b1, b2, b3 = st.session_state.bases

    b_dots = "".join(['<span class="dot-b">●</span>' if i < b else '<span class="dot-off">●</span>' for i in range(3)])
    s_dots = "".join(['<span class="dot-s">●</span>' if i < s else '<span class="dot-off">●</span>' for i in range(2)])
    o_dots = "".join(['<span class="dot-o">●</span>' if i < o else '<span class="dot-off">●</span>' for i in range(2)])

    crowd_html = (
        '<span class="crowd-wave">🙌📣⚾🔥🙌📣⚾🔥</span>'
        if is_fever
        else '<span style="font-size:1.1rem; opacity:0.85;">⚾🏟️🧢🌭</span>'
    )

    html = f"""
    <div class="scoreboard-wrap">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <div>
                <div class="sb-title">🏟️ JAMSIL ARCADE STADIUM LIVE</div>
                <div style="font-size:0.9rem; color:#cbd5e1; margin-top:2px;">
                    현재 경기: <strong style="color:#facc15; font-size:1.05rem;">{inning}회말 공격</strong> &nbsp;|&nbsp; {crowd_html}
                </div>
            </div>
            <div style="display:flex; gap:10px; align-items:center;">
                <div class="sb-score-box">
                    <div class="sb-team">AWAY</div>
                    <div class="sb-num away">{st.session_state.away_score}</div>
                </div>
                <div style="font-weight:900; color:#64748b; font-size:1.2rem;">VS</div>
                <div class="sb-score-box">
                    <div class="sb-team">HOME</div>
                    <div class="sb-num">{st.session_state.home_score}</div>
                </div>
            </div>
            <div style="display:flex; gap:16px; align-items:center; background:#050811; padding:6px 14px; border-radius:10px; border:1px solid #2b3a55;">
                <div class="sbo-row">
                    <div>B {b_dots}</div>
                    <div>S {s_dots}</div>
                    <div>O {o_dots}</div>
                </div>
                <div class="diamond-box">
                    <div class="base base-2 {'active' if b2 else ''}"></div>
                    <div class="base base-3 {'active' if b3 else ''}"></div>
                    <div class="base base-1 {'active' if b1 else ''}"></div>
                    <div class="base base-home"></div>
                </div>
            </div>
        </div>
        <div class="live-ticker">📢 중계석: {st.session_state.ticker_msg}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_hud(now: float, is_fever: bool):
    inning = st.session_state.inning
    cfg = INNING_CONFIG[inning]
    time_left = max(0.0, cfg["duration"] - (now - st.session_state.inning_start_time))
    inning_gold = st.session_state.inning_gold
    target_gold = cfg["target"]
    goal_pct = min(100, int((inning_gold / target_gold) * 100))

    fever_left = max(0.0, st.session_state.fever_until - now) if is_fever else 0.0
    fever_pct = 100 if is_fever else st.session_state.fever_gauge

    c1, c2, c3, c4, c5 = st.columns([1.1, 1.4, 1.1, 1.0, 1.3])
    with c1:
        time_color = "#dc2626" if time_left <= 8 else "#0f172a"
        st.markdown(
            f"""<div class="hud-bar">
                <div class="hud-item-label">⏱️ {inning}회 남은 시간</div>
                <div class="hud-item-val" style="color:{time_color} !important;">{time_left:.1f}초</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        clear_tag = "✅ 달성!" if inning_gold >= target_gold else f"({goal_pct}%)"
        st.markdown(
            f"""<div class="hud-bar">
                <div class="hud-item-label">🎯 {inning}회 매출 / 목표 {clear_tag}</div>
                <div class="hud-item-val">{inning_gold:,} / {target_gold:,}G</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""<div class="hud-bar">
                <div class="hud-item-label">💰 누적 총 매출</div>
                <div class="hud-item-val">{st.session_state.total_gold:,}G</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""<div class="hud-bar">
                <div class="hud-item-label">🔥 콤보 / 🧤캐치</div>
                <div class="hud-item-val">{st.session_state.combo}콤보 / {st.session_state.foul_catches}회</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c5:
        label = f"⚡ FEVER ({fever_left:.1f}s)" if is_fever else f"🔥 피버 게이지 ({fever_pct}%)"
        st.markdown(
            f"""<div class="hud-bar">
                <div class="hud-item-label">{label}</div>
                <div style="background:#e2e8f0; border-radius:6px; height:14px; margin-top:6px; overflow:hidden;">
                    <div style="width:{fever_pct}%; height:100%; background:linear-gradient(90deg,#f59e0b,#ec4899);"></div>
                </div>
            </div>""",
            unsafe_allow_html=True,
        )


def render_alerts(now: float, is_fever: bool):
    if is_fever:
        fever_left = max(0.0, st.session_state.fever_until - now)
        st.markdown(
            f"""<div class="fever-banner">
                <span class="crowd-wave">🙌📣⚾🔥</span>
                &nbsp; FEVER TIME 발동 중! ({fever_left:.1f}초) — 모든 조리 1초 완성 & 판매가 1.5배! &nbsp;
                <span class="crowd-wave">🔥⚾📣🙌</span>
            </div>""",
            unsafe_allow_html=True,
        )

    if st.session_state.foul_active:
        foul_left = max(0.0, st.session_state.foul_deadline - now)
        col_msg, col_btn = st.columns([2.2, 1])
        with col_msg:
            st.markdown(
                f'<div class="foul-banner">⚠️ 파울볼 날아옴! {foul_left:.1f}초 안에 글러브로 잡아내세요!</div>',
                unsafe_allow_html=True,
            )
        with col_btn:
            st.button(
                "🧤 글러브로 캐치! (+12,000G)",
                key="btn_catch_foul",
                type="primary",
                use_container_width=True,
                on_click=handle_catch_foul,
            )
    elif now < st.session_state.stun_until:
        stun_left = max(0.0, st.session_state.stun_until - now)
        st.markdown(
            f'<div class="shake-penalty">💥 콰당!! 파울볼 충격으로 매점 흔들림! ({stun_left:.1f}초간 조리/서빙 일시 정지)</div>',
            unsafe_allow_html=True,
        )


def render_customers(now: float, is_fever: bool):
    st.subheader("🙋‍♂️ 주문 대기 손님 (최대 4팀)")
    grid_cols = st.columns(2)
    customers = st.session_state.customers

    for i in range(4):
        with grid_cols[i % 2]:
            if i < len(customers):
                cust = customers[i]
                menu_name = cust["menu"]
                info = MENUS[menu_name]
                rem = max(0.0, cust["max_patience"] - (now - cust["spawn_time"]))
                ratio = max(0.0, min(1.0, rem / cust["max_patience"]))
                urgent_cls = "urgent" if ratio <= 0.35 else ""

                bar_color = "#22c55e" if ratio > 0.55 else ("#f59e0b" if ratio > 0.35 else "#ef4444")
                disp_price = int(info["price"] * (1.5 if is_fever else 1.0))

                st.markdown(
                    f"""
                    <div class="cust-card {urgent_cls}">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-weight:800; font-size:0.95rem;">{cust['avatar']} {cust['role']}</span>
                            <span style="font-size:0.82rem; font-weight:700; color:{bar_color};">⏳ {rem:.1f}초</span>
                        </div>
                        <div style="font-size:1.1rem; font-weight:900; margin:6px 0 4px 0;">
                            {info['icon']} {menu_name}
                        </div>
                        <div style="font-size:0.82rem; color:#475569; margin-bottom:6px;">
                            기본가 {disp_price:,}G + 콤보팁
                        </div>
                        <div style="background:#e2e8f0; height:8px; border-radius:4px; overflow:hidden;">
                            <div style="width:{int(ratio*100)}%; height:100%; background:{bar_color};"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="cust-card empty">👟 다음 손님 입장 대기 중...</div>',
                    unsafe_allow_html=True,
                )


def render_kitchen(now: float, is_fever: bool):
    st.subheader("🍳 매점 조리대 & 즉시 서빙")
    stunned = now < st.session_state.stun_until

    # 1) 즉시 서빙 메뉴 (생맥주, 나초 & 치즈)
    st.markdown("**⚡ 즉시 서빙 코너 (클릭 즉시 서빙)**")
    ic1, ic2 = st.columns(2)
    with ic1:
        p_beer = int(MENUS["생맥주"]["price"] * (1.5 if is_fever else 1.0))
        st.button(
            f"🍺 생맥주 서빙 ({p_beer:,}G)",
            key="serve_beer",
            use_container_width=True,
            disabled=stunned,
            on_click=complete_serving,
            args=("생맥주",),
        )
    with ic2:
        p_nacho = int(MENUS["나초 & 치즈"]["price"] * (1.5 if is_fever else 1.0))
        st.button(
            f"🧀 나초 & 치즈 서빙 ({p_nacho:,}G)",
            key="serve_nacho",
            use_container_width=True,
            disabled=stunned,
            on_click=complete_serving,
            args=("나초 & 치즈",),
        )

    st.markdown("---")

    # 2) 순살치킨 조리대 (조리 3초, 방치 7초 시 탄다)
    c_cook_req = 1.0 if is_fever else 3.0
    p_chicken = int(MENUS["순살치킨"]["price"] * (1.5 if is_fever else 1.0))
    st.markdown(f"**🍗 순살치킨 튀김기 ({p_chicken:,}G | 조리 {int(c_cook_req)}초 · 완성 후 7초 내 서빙 필수!)**")
    cc1, cc2 = st.columns(2)
    for idx, col in enumerate([cc1, cc2]):
        slot = st.session_state.chicken_slots[idx]
        with col:
            if slot["state"] == "idle":
                st.markdown(
                    f'<div class="cook-card"><strong>튀김기 #{idx+1}</strong><br><span style="font-size:0.85rem;">대기 중</span></div>',
                    unsafe_allow_html=True,
                )
                st.button(
                    f"🔥 치킨 조리 시작 ({int(c_cook_req)}초)",
                    key=f"chk_start_{idx}",
                    use_container_width=True,
                    disabled=stunned,
                    on_click=handle_start_cook,
                    args=("chicken_slots", idx),
                )
            elif slot["state"] == "cooking":
                elapsed = now - slot["start_time"]
                rem = max(0.0, c_cook_req - elapsed)
                pct = min(100, int((elapsed / c_cook_req) * 100))
                st.markdown(
                    f"""<div class="cook-card">
                        <strong>튀김기 #{idx+1} · 조리 중... ({rem:.1f}초)</strong>
                        <div style="background:#fde68a; height:8px; border-radius:4px; margin-top:6px;">
                            <div style="width:{pct}%; height:100%; background:#d97706;"></div>
                        </div>
                    </div>""",
                    unsafe_allow_html=True,
                )
                st.button("⏳ 튀기는 중...", key=f"chk_wait_{idx}", use_container_width=True, disabled=True)
            elif slot["state"] == "ready":
                burn_rem = max(0.0, 7.0 - (now - slot["ready_time"]))
                burn_pct = min(100, int((burn_rem / 7.0) * 100))
                st.markdown(
                    f"""<div class="cook-card ready">
                        <strong>✅ 순살치킨 완성! (타기까지 {burn_rem:.1f}초)</strong>
                        <div style="background:#a7f3d0; height:8px; border-radius:4px; margin-top:6px;">
                            <div style="width:{burn_pct}%; height:100%; background:#dc2626;"></div>
                        </div>
                    </div>""",
                    unsafe_allow_html=True,
                )
                st.button(
                    "🍗 치킨 서빙하기!",
                    key=f"chk_serve_{idx}",
                    type="primary",
                    use_container_width=True,
                    disabled=stunned,
                    on_click=handle_serve_cooked,
                    args=("chicken_slots", idx, "순살치킨"),
                )
            elif slot["state"] == "burned":
                st.markdown(
                    f'<div class="cook-card burned"><strong>💀 튀김기 #{idx+1} · 새까맣게 탐!</strong><br><span style="font-size:0.82rem;">폐기해야 다시 조리 가능</span></div>',
                    unsafe_allow_html=True,
                )
                st.button(
                    "🗑️ 탄 치킨 폐기하기",
                    key=f"chk_burn_{idx}",
                    use_container_width=True,
                    on_click=handle_discard_burned,
                    args=(idx,),
                )

    st.markdown("---")

    # 3) 크림새우 & 떡볶이 세트 조리대 (조리 5초, 고단가)
    s_cook_req = 1.0 if is_fever else 5.0
    p_shrimp = int(MENUS["크림새우 & 떡볶이 세트"]["price"] * (1.5 if is_fever else 1.0))
    st.markdown(f"**🍤 크림새우 & 떡볶이 세트 팬 ({p_shrimp:,}G | 조리 {int(s_cook_req)}초 · 고단가 프리미엄)**")
    sc1, sc2 = st.columns(2)
    for idx, col in enumerate([sc1, sc2]):
        slot = st.session_state.shrimp_slots[idx]
        with col:
            if slot["state"] == "idle":
                st.markdown(
                    f'<div class="cook-card"><strong>전용 팬 #{idx+1}</strong><br><span style="font-size:0.85rem;">대기 중</span></div>',
                    unsafe_allow_html=True,
                )
                st.button(
                    f"🔥 세트 조리 시작 ({int(s_cook_req)}초)",
                    key=f"shr_start_{idx}",
                    use_container_width=True,
                    disabled=stunned,
                    on_click=handle_start_cook,
                    args=("shrimp_slots", idx),
                )
            elif slot["state"] == "cooking":
                elapsed = now - slot["start_time"]
                rem = max(0.0, s_cook_req - elapsed)
                pct = min(100, int((elapsed / s_cook_req) * 100))
                st.markdown(
                    f"""<div class="cook-card">
                        <strong>전용 팬 #{idx+1} · 조리 중... ({rem:.1f}초)</strong>
                        <div style="background:#fde68a; height:8px; border-radius:4px; margin-top:6px;">
                            <div style="width:{pct}%; height:100%; background:#d97706;"></div>
                        </div>
                    </div>""",
                    unsafe_allow_html=True,
                )
                st.button("⏳ 조리 중...", key=f"shr_wait_{idx}", use_container_width=True, disabled=True)
            elif slot["state"] == "ready":
                st.markdown(
                    f'<div class="cook-card ready"><strong>✅ 크림새우 & 떡볶이 완성!</strong><br><span style="font-size:0.82rem;">서빙 준비 완료</span></div>',
                    unsafe_allow_html=True,
                )
                st.button(
                    "🍤 세트 서빙하기!",
                    key=f"shr_serve_{idx}",
                    type="primary",
                    use_container_width=True,
                    disabled=stunned,
                    on_click=handle_serve_cooked,
                    args=("shrimp_slots", idx, "크림새우 & 떡볶이 세트"),
                )


# ==========================================
# 8. 시작 화면 & 영수증 결과창
# ==========================================
def render_start_screen():
    st.markdown(NORMAL_BG_CSS, unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align:center; padding: 20px 10px 10px 10px;">
            <div style="font-size:3.2rem;">⚾🍺🍗🍤</div>
            <h1 style="font-family:'Black Han Sans', sans-serif; font-size:2.6rem; margin-bottom:6px; color:#0f172a;">
                야구장 매점 알바 타이쿤
            </h1>
            <p style="font-size:1.1rem; color:#475569; font-weight:700;">
                1회부터 9회말까지 직관 관중들의 주문을 처리하고, 날아오는 파울볼을 글러브로 캐치하세요!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1, 2.2, 1])
    with c2:
        st.info(
            """
            **📋 알바생 근무 수칙**
            1. **이닝 목표 달성**: 1회~9회 각 이닝 제한 시간 내에 목표 매출(골드)을 달성해야 다음 이닝으로 넘어갑니다.
            2. **4종 메뉴 조리 & 서빙**:
               - 🍺 **생맥주** / 🧀 **나초 & 치즈**: 클릭 즉시 바로 서빙!
               - 🍗 **순살치킨**: 조리 **3초** 소요! 완성 후 **7초** 이상 방치하면 새까맣게 타버려 폐기해야 합니다.
               - 🍤 **크림새우 & 떡볶이 세트**: 조리 **5초** 소요되는 고단가 효자 메뉴!
            3. **돌발 파울볼 캐치**: 경고음이 울리면 **3초** 안에 `[🧤 글러브로 캐치!]`를 누르세요! 놓치면 2초간 매점이 마비됩니다.
            4. **피버 타임 (응원가 모드)**: 피버 게이지 100% 또는 전광판 홈런/득점 시 **10초간 피버 타임** 발동! 조리 1초 단축 & 매출 1.5배!
            """
        )
        col_btn, col_mute = st.columns([3, 1])
        with col_btn:
            if st.button("⚾ 매점 아르바이트 출근하기!", type="primary", use_container_width=True):
                start_new_game()
                st.rerun()
        with col_mute:
            mute_label = "🔇 음소거됨" if st.session_state.sound_muted else "🔊 사운드 ON"
            if st.button(mute_label, use_container_width=True):
                st.session_state.sound_muted = not st.session_state.sound_muted
                st.rerun()


def evaluate_title():
    sold = st.session_state.sold_counts
    top_menu = max(sold, key=lambda k: sold[k]) if sum(sold.values()) > 0 else "없음"
    top_cnt = sold.get(top_menu, 0)
    burned = st.session_state.burned_count
    catches = st.session_state.foul_catches
    gold = st.session_state.total_gold
    max_combo = st.session_state.max_combo
    victory = st.session_state.victory

    if burned >= 4:
        return "🔥 잠실벌의 치킨 방화범", f"치킨을 {burned}번이나 태워먹은 전설의 숯불 장인!"
    if catches >= 5:
        return "🧤 KBO 골든글러브 매점 부문 수상자", f"파울볼 {catches}개 슈퍼 캐치! 선수보다 수비를 잘합니다."
    if victory and gold >= 550000:
        return "👑 구단주가 스카우트하려는 매점의 신", "9회말까지 매출 신기록을 갈아치운 직관의 지배자!"
    if top_menu == "생맥주" and top_cnt >= 12:
        return "🍺 잠실의 생맥주 거품 장인", f"생맥주 {top_cnt}잔 판매! 목마른 관중들의 영원한 오아시스!"
    if top_menu == "크림새우 & 떡볶이 세트" and top_cnt >= 8:
        return "🍤 크림새우 & 떡볶이 완판 신화", f"프리미엄 세트 {top_cnt}개 돌파! 객단가 수직 상승의 주역!"
    if max_combo >= 15:
        return "⚡ 리듬게임 고인물 출신 서빙 머신", f"최대 {max_combo}콤보 달성! 한 치의 오차도 없는 손놀림!"
    if victory:
        return "⚾ 9회말 역전승의 숨은 MVP", "끝까지 매점을 지켜낸 듬직한 야구장 에이스 알바생!"
    return "🐣 병아리 매점 수습생", "아쉽게 목표 매출 미달! 다음 경기에선 파울볼과 손님 인내심을 사수하세요!"


def render_gameover_screen():
    st.markdown(NORMAL_BG_CSS, unsafe_allow_html=True)
    render_sound_engine(
        st.session_state.sound_id,
        st.session_state.sound_type,
        False,
        st.session_state.sound_muted,
    )

    sold = st.session_state.sold_counts
    if sum(sold.values()) > 0:
        top_menu = max(sold, key=lambda k: sold[k])
        top_menu_str = f"{MENUS[top_menu]['icon']} {top_menu} ({sold[top_menu]}개)"
    else:
        top_menu_str = "판매 내역 없음"

    title_name, title_desc = evaluate_title()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_text = "🎉 9회말 경기 종료 (완주 성공!)" if st.session_state.victory else f"💥 {st.session_state.inning}회 영업 종료 (목표 미달)"

    st.markdown(
        f"""
        <div class="receipt-paper">
            <div class="receipt-header">
                <div style="font-size:1.5rem; font-weight:900;">🧾 야구장 매점 영수증</div>
                <div style="font-size:0.85rem; color:#64748b; margin-top:4px;">JAMSIL STADIUM SNACK BAR</div>
                <div style="font-size:0.82rem; color:#64748b;">발행일시: {now_str}</div>
                <div style="font-weight:800; color:#0f172a; margin-top:6px;">{status_text}</div>
            </div>
            <div class="receipt-row"><span>🍺 생맥주 판매량</span><span>{sold['생맥주']} 잔</span></div>
            <div class="receipt-row"><span>🧀 나초 & 치즈 판매량</span><span>{sold['나초 & 치즈']} 개</span></div>
            <div class="receipt-row"><span>🍗 순살치킨 판매량</span><span>{sold['순살치킨']} 마리</span></div>
            <div class="receipt-row"><span>🍤 크림새우&떡볶이 세트</span><span>{sold['크림새우 & 떡볶이 세트']} 세트</span></div>
            <div style="border-top:1px dashed #cbd5e1; margin:8px 0;"></div>
            <div class="receipt-row"><span>🏆 최다 판매 메뉴</span><span><strong>{top_menu_str}</strong></span></div>
            <div class="receipt-row"><span>🧤 파울볼 캐치 횟수</span><span><strong>{st.session_state.foul_catches} 회</strong></span></div>
            <div class="receipt-row"><span>🔥 최대 연속 콤보</span><span><strong>{st.session_state.max_combo} 콤보</strong></span></div>
            <div class="receipt-row"><span>💀 치킨 폐기 횟수</span><span>{st.session_state.burned_count} 회</span></div>
            <div class="receipt-total">
                <span>총 매출액 (TOTAL)</span>
                <span>{st.session_state.total_gold:,} G</span>
            </div>
            <div class="title-badge">
                <div style="font-size:0.8rem; color:#92400e; font-weight:700;">[ 오늘의 알바생 칭호 ]</div>
                <div style="font-size:1.3rem; font-weight:900; color:#78350f; margin:4px 0;">{title_name}</div>
                <div style="font-size:0.88rem; color:#92400e;">{title_desc}</div>
            </div>
            <div style="text-align:center; font-size:0.8rem; color:#94a3b8; margin-top:14px;">
                *** 이용해 주셔서 감사합니다! THANK YOU! ***
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    c1, c2, c3 = st.columns([1.2, 1.6, 1.2])
    with c2:
        if st.button("🔄 다음 경기 다시 도전하기!", type="primary", use_container_width=True):
            start_new_game()
            st.rerun()


# ==========================================
# 9. 실시간 게임 플레이 루프 (st.fragment)
# ==========================================
@st.fragment(run_every=1)
def run_gameplay_fragment():
    process_game_tick()
    if st.session_state.phase != "playing":
        return

    now = time.time()
    is_fever = now < st.session_state.fever_until

    # 피버 타임에 따른 배경 조명 전환
    st.markdown(FEVER_BG_CSS if is_fever else NORMAL_BG_CSS, unsafe_allow_html=True)

    # Web Audio API 사운드 및 피버 응원가 비트 재생
    render_sound_engine(
        st.session_state.sound_id,
        st.session_state.sound_type,
        is_fever,
        st.session_state.sound_muted,
    )

    # 상단 사운드 토글 & 중도 종료 미니 컨트롤
    top_l, top_r1, top_r2 = st.columns([5, 1, 1])
    with top_l:
        st.markdown(
            f"<div style='font-weight:900; font-size:1.25rem;'>⚾ 야구장 매점 타이쿤 — {st.session_state.inning}회 / 9회</div>",
            unsafe_allow_html=True,
        )
    with top_r1:
        mute_txt = "🔇 음소거" if st.session_state.sound_muted else "🔊 소리ON"
        if st.button(mute_txt, key="frag_mute", use_container_width=True):
            st.session_state.sound_muted = not st.session_state.sound_muted
    with top_r2:
        if st.button("🧾 정산종료", key="frag_quit", use_container_width=True):
            st.session_state.phase = "gameover"
            st.session_state.victory = False
            trigger_sound("gameover")
            st.rerun()

    # 1) 최상단 야구장 전광판
    render_scoreboard(now, is_fever)

    # 2) 이닝 매출/시간/콤보/피버 HUD
    render_hud(now, is_fever)

    # 3) 파울볼 긴급 이벤트 / 피버 배너 / 페널티 알림
    render_alerts(now, is_fever)

    # 4) 메인 플레이 영역: 좌측 손님 대기석 / 우측 조리 및 서빙 카운터
    left_col, right_col = st.columns([1.05, 1.15], gap="medium")
    with left_col:
        render_customers(now, is_fever)
    with right_col:
        render_kitchen(now, is_fever)


# ==========================================
# 10. 메인 진입점
# ==========================================
def main():
    st.markdown(BASE_CSS, unsafe_allow_html=True)
    ensure_state()

    if st.session_state.phase == "start":
        render_start_screen()
    elif st.session_state.phase == "playing":
        run_gameplay_fragment()
    elif st.session_state.phase == "gameover":
        render_gameover_screen()


if __name__ == "__main__":
    main()
