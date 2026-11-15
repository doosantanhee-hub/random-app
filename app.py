import random
import time
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. 페이지 설정 및 반응형/아케이드 커스텀 CSS
# ==========================================
st.set_page_config(
    page_title="야구장 매점 타이쿤: 프로야구 에디션 ⚾",
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
    padding-top: 0.85rem !important;
    padding-bottom: 1.5rem !important;
    max-width: 1320px;
}

/* 전광판 스타일 */
.scoreboard-wrap {
    background: linear-gradient(180deg, #0b132b 0%, #1c2541 100%);
    border: 4px solid #3a506b;
    border-radius: 14px;
    padding: 10px 16px;
    color: #ffffff;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.35);
    margin-bottom: 8px;
}

.sb-title {
    font-family: 'Black Han Sans', sans-serif;
    color: #ffd166;
    font-size: 1.1rem;
    letter-spacing: 1px;
}

.sb-score-box {
    background: #050811;
    border: 2px solid #2b3a55;
    border-radius: 10px;
    padding: 5px 12px;
    text-align: center;
    font-family: 'Share Tech Mono', monospace;
}

.sb-team {
    font-size: 0.78rem;
    color: #94a3b8;
    font-weight: 700;
}

.sb-num {
    font-size: 1.65rem;
    font-weight: 900;
    color: #4ade80;
    line-height: 1.1;
}

.sb-num.away {
    color: #f87171;
}

.sbo-row {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.9rem;
    font-weight: 700;
    line-height: 1.3;
}

.dot-s { color: #facc15; }
.dot-b { color: #4ade80; }
.dot-o { color: #ef4444; }
.dot-off { color: #334155; }

.live-ticker {
    background: #050811;
    border-left: 4px solid #f59e0b;
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 0.9rem;
    font-weight: 700;
    color: #fef08a;
    margin-top: 6px;
}

/* 주자 다이아몬드 미니 그래픽 */
.diamond-box {
    position: relative;
    width: 58px;
    height: 58px;
    margin: 0 auto;
}
.base {
    position: absolute;
    width: 14px;
    height: 14px;
    transform: rotate(45deg);
    border: 2px solid #94a3b8;
    background: #1e293b;
}
.base.active {
    background: #facc15;
    border-color: #fef08a;
    box-shadow: 0 0 10px #facc15;
}
.base-2 { top: 4px; left: 22px; }
.base-3 { top: 22px; left: 4px; }
.base-1 { top: 22px; left: 40px; }
.base-home { top: 40px; left: 22px; border-color: #64748b; background: #cbd5e1; }

/* HUD 상태바 */
.hud-bar {
    background: #f8fafc;
    border: 2px solid #cbd5e1;
    border-radius: 10px;
    padding: 8px 12px;
    margin-bottom: 8px;
}
.hud-item-label {
    font-size: 0.75rem;
    color: #64748b;
    font-weight: 700;
}
.hud-item-val {
    font-size: 1.12rem;
    font-weight: 900;
    color: #0f172a;
}

/* 손님 카드 */
.cust-card {
    background: #ffffff;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    padding: 8px 10px;
    margin-bottom: 6px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.05);
}
.cust-card.urgent {
    border-color: #ef4444;
    background: #fef2f2;
}
.cust-card.vip-cheer {
    border-color: #8b5cf6;
    background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
}
.cust-card.vip-rush {
    border-color: #f59e0b;
    background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
}
.cust-card.vip-saint {
    border-color: #0ea5e9;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
}
.cust-card.vip-catcher {
    border-color: #10b981;
    background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
}
.cust-card.empty {
    background: #f8fafc;
    border: 2px dashed #cbd5e1;
    color: #94a3b8;
    text-align: center;
    padding: 18px 10px;
}

.vip-badge {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 900;
    padding: 1px 6px;
    border-radius: 6px;
    margin-left: 4px;
}
.vip-badge.cheer { background: #7c3aed; color: #ffffff; }
.vip-badge.rush { background: #d97706; color: #ffffff; }
.vip-badge.saint { background: #0284c7; color: #ffffff; }
.vip-badge.catcher { background: #059669; color: #ffffff; }

/* 조리대 카드 */
.cook-card {
    background: #fffbeb;
    border: 2px solid #fcd34d;
    border-radius: 10px;
    padding: 8px 10px;
    margin-bottom: 6px;
}
.cook-card.ready {
    background: #ecfdf5;
    border-color: #10b981;
}
.cook-card.ready-match {
    background: #d1fae5;
    border: 3px solid #059669;
    box-shadow: 0 0 12px rgba(16, 185, 129, 0.45);
}
.cook-card.burned {
    background: #1f2937;
    border-color: #ef4444;
    color: #f9fafb;
}

/* 서빙 성공 즉각 피드백 팝업 배너 */
@keyframes popGain {
    0% { transform: scale(0.96); opacity: 0.85; }
    50% { transform: scale(1.02); opacity: 1; }
    100% { transform: scale(1); opacity: 1; }
}
.gain-popup {
    background: linear-gradient(90deg, #059669, #10b981);
    color: #ffffff;
    font-weight: 900;
    font-size: 0.95rem;
    padding: 7px 14px;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 8px;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
    animation: popGain 0.35s ease;
}

/* 특수 이벤트 배너 (클리닝 타임 / 비디오 판독 / 풀카운트) */
.special-banner {
    background: linear-gradient(90deg, #1d4ed8, #3b82f6, #1d4ed8);
    color: #ffffff;
    font-weight: 900;
    font-size: 0.95rem;
    padding: 7px 14px;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 8px;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35);
}

.var-banner {
    background: linear-gradient(90deg, #b45309, #f59e0b, #b45309);
    color: #ffffff;
    font-weight: 900;
    font-size: 0.98rem;
    padding: 8px 14px;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 8px;
    border: 2px solid #fef08a;
}

/* 파울볼 / 홈런볼 긴급 경고 */
@keyframes pulseAlert {
    0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.8); }
    50% { transform: scale(1.015); box-shadow: 0 0 22px 6px rgba(239, 68, 68, 0.6); }
    100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.8); }
}
.foul-banner {
    background: linear-gradient(90deg, #dc2626, #ea580c, #dc2626);
    color: white;
    padding: 9px 14px;
    border-radius: 10px;
    font-weight: 900;
    font-size: 1.05rem;
    text-align: center;
    animation: pulseAlert 0.65s infinite;
    margin-bottom: 6px;
}
.foul-banner.linedrive {
    background: linear-gradient(90deg, #991b1b, #dc2626, #7f1d1d);
    border: 2px solid #fde047;
}
.foul-banner.homerunball {
    background: linear-gradient(90deg, #6d28d9, #db2777, #f59e0b);
    border: 2px solid #fef08a;
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
    border-radius: 10px;
    padding: 9px;
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
    font-size: 1.35rem;
    animation: cheerDance 0.45s infinite ease-in-out;
    letter-spacing: 3px;
}

.fever-banner {
    background: linear-gradient(90deg, #7e22ce, #db2777, #f59e0b, #10b981, #7e22ce);
    background-size: 300% 300%;
    animation: feverGradient 2s ease infinite;
    color: #ffffff;
    border-radius: 10px;
    padding: 7px 12px;
    text-align: center;
    font-weight: 900;
    font-size: 1rem;
    margin-bottom: 8px;
    box-shadow: 0 0 20px rgba(236, 72, 153, 0.65);
}
@keyframes feverGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* 튜토리얼 가이드 바 */
.tutorial-tip {
    background: #eff6ff;
    border-left: 5px solid #3b82f6;
    color: #1e3a8a;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 700;
    margin-bottom: 8px;
}

/* 명예의 전당 카드 */
.hof-card {
    background: #ffffff;
    border: 2px solid #cbd5e1;
    border-radius: 12px;
    padding: 14px 16px;
    margin-top: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

/* 영수증 결과창 */
.receipt-paper {
    background: #fffdf7;
    border: 2px dashed #475569;
    border-radius: 8px;
    padding: 22px 26px;
    max-width: 560px;
    margin: 0 auto;
    font-family: 'Share Tech Mono', 'Noto Sans KR', monospace;
    color: #1e293b;
    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
}
.receipt-header {
    text-align: center;
    border-bottom: 2px dashed #94a3b8;
    padding-bottom: 10px;
    margin-bottom: 12px;
}
.receipt-row {
    display: flex;
    justify-content: space-between;
    padding: 4px 0;
    font-size: 1rem;
}
.receipt-total {
    border-top: 2px dashed #94a3b8;
    border-bottom: 2px dashed #94a3b8;
    margin-top: 10px;
    padding: 10px 0;
    font-size: 1.25rem;
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
    margin-top: 12px;
}

/* 모바일 화면 대응 */
@media (max-width: 768px) {
    .block-container {
        padding-top: 0.4rem !important;
        padding-left: 0.6rem !important;
        padding-right: 0.6rem !important;
    }
    .scoreboard-wrap { padding: 8px 10px; }
    .sb-num { font-size: 1.35rem; }
    .hud-bar { padding: 6px 8px; margin-bottom: 4px; }
    .hud-item-val { font-size: 0.98rem; }
    .cust-card, .cook-card { padding: 7px 9px; }
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
.cust-card, .cook-card, .hud-bar, .hof-card {
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
# 2. 구장 테마, 메뉴 및 야구팬 특수 손님 설정
# ==========================================
STADIUMS = {
    "잠실야구장 (치맥의 성지)": {
        "en_name": "JAMSIL BASEBALL STADIUM",
        "desc": "🍺 생맥주 & 🍗 순살치킨 주문 집중! 정통 치맥 직관 구장",
        "weights": {"생맥주": 40, "나초 & 치즈": 20, "순살치킨": 30, "크림새우 & 떡볶이 세트": 10},
        "shrimp_mult": 1.0,
        "cheer_prob": 0.14,
        "hr_weight": 4,
    },
    "인천 SSG랜더스필드 (크림새우 랜드)": {
        "en_name": "INCHEON SSG LANDERS FIELD",
        "desc": "🍤 크림새우 & 떡볶이 세트 주문 폭증 & 세트 기본 판매가 +20% 보너스!",
        "weights": {"생맥주": 25, "나초 & 치즈": 20, "순살치킨": 20, "크림새우 & 떡볶이 세트": 35},
        "shrimp_mult": 1.2,
        "cheer_prob": 0.14,
        "hr_weight": 5,
    },
    "사직야구장 (열정의 구도)": {
        "en_name": "SAJIK BASEBALL STADIUM",
        "desc": "📣 열혈 응원단장 등장 확률 2배 & 서빙 시 피버 게이지 충전량 +30%!",
        "weights": {"생맥주": 35, "나초 & 치즈": 25, "순살치킨": 25, "크림새우 & 떡볶이 세트": 15},
        "shrimp_mult": 1.0,
        "cheer_prob": 0.30,
        "hr_weight": 4,
    },
    "대구 삼성라이온즈파크 (타자 친화 구장)": {
        "en_name": "DAEGU SAMSUNG LIONS PARK",
        "desc": "🎆 전광판 장타·홈런 폭발 확률 2배! 피버 타임이 자주 터지는 화끈한 구장",
        "weights": {"생맥주": 35, "나초 & 치즈": 25, "순살치킨": 25, "크림새우 & 떡볶이 세트": 15},
        "shrimp_mult": 1.0,
        "cheer_prob": 0.15,
        "hr_weight": 9,
    },
}

MENUS = {
    "생맥주": {
        "icon": "🍺",
        "price": 4000,
        "cook_time": 0,
        "can_burn": False,
    },
    "나초 & 치즈": {
        "icon": "🧀",
        "price": 5000,
        "cook_time": 0,
        "can_burn": False,
    },
    "순살치킨": {
        "icon": "🍗",
        "price": 9000,
        "cook_time": 3,
        "can_burn": True,
        "burn_limit": 7,
    },
    "크림새우 & 떡볶이 세트": {
        "icon": "🍤",
        "price": 14000,
        "cook_time": 5,
        "can_burn": False,
    },
}

CUSTOMER_PROFILES = [
    ("🧔", "치맥 열혈팬"),
    ("👩", "직관 10년차"),
    ("👧", "유니폼 꼬마팬"),
    ("👨", "퇴근 후 직관러"),
    ("👩‍🦱", "먹방 유튜버"),
]

# 이닝별 목표 매출(골드) 및 제한 시간(초)
INNING_CONFIG = {
    1: {"target": 22000, "duration": 36},
    2: {"target": 32000, "duration": 36},
    3: {"target": 42000, "duration": 36},
    4: {"target": 52000, "duration": 38},
    5: {"target": 65000, "duration": 42},  # 5회말 종료 후 클리닝 타임 러시 포함
    6: {"target": 76000, "duration": 38},
    7: {"target": 88000, "duration": 40},
    8: {"target": 100000, "duration": 40},
    9: {"target": 120000, "duration": 44},  # 9회말 끝내기 찬스 포함
}


# ==========================================
# 3. Web Audio API 신시사이저 (외부 파일 불필요)
# ==========================================
def render_sound_engine(sound_id: int, sound_type: str, is_fever: bool, muted: bool):
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

        const unlockAudio = () => {{
            if (ctx.state === 'suspended') {{
                ctx.resume();
            }}
        }};
        unlockAudio();
        try {{
            parentWin.document.addEventListener('pointerdown', unlockAudio, {{ once: true }});
        }} catch(e) {{}}

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

        if (parentWin._lastPlayedSoundId !== SOUND_ID) {{
            parentWin._lastPlayedSoundId = SOUND_ID;
            const now = ctx.currentTime;

            if (SOUND_TYPE === "foul_alert") {{
                playNoise(now, 0.08, 0.3);
                playTone(920, "triangle", now, 0.09, 0.25);
                playTone(880, "sawtooth", now + 0.12, 0.16, 0.16);
                playTone(620, "sawtooth", now + 0.29, 0.16, 0.16);
                playTone(880, "sawtooth", now + 0.46, 0.18, 0.16);
            }} else if (SOUND_TYPE === "linedrive_alert") {{
                playNoise(now, 0.06, 0.35);
                playTone(1150, "sawtooth", now, 0.08, 0.25);
                playTone(1350, "sawtooth", now + 0.09, 0.1, 0.25);
                playTone(1150, "sawtooth", now + 0.20, 0.12, 0.25);
            }} else if (SOUND_TYPE === "foul_catch") {{
                playTone(523.25, "square", now, 0.09, 0.15);
                playTone(659.25, "square", now + 0.09, 0.09, 0.15);
                playTone(783.99, "square", now + 0.18, 0.09, 0.15);
                playTone(1046.5, "square", now + 0.27, 0.28, 0.18);
            }} else if (SOUND_TYPE === "foul_miss") {{
                playNoise(now, 0.28, 0.25);
                playTone(180, "sawtooth", now, 0.22, 0.2);
                playTone(120, "sawtooth", now + 0.18, 0.25, 0.2);
            }} else if (SOUND_TYPE === "serve") {{
                playTone(987.77, "sine", now, 0.07, 0.14);
                playTone(1318.51, "sine", now + 0.07, 0.14, 0.14);
            }} else if (SOUND_TYPE === "burn") {{
                playTone(220, "sawtooth", now, 0.14, 0.15);
                playTone(165, "sawtooth", now + 0.15, 0.2, 0.15);
            }} else if (SOUND_TYPE === "fever_start") {{
                [523, 659, 784, 1046, 1318].forEach((f, idx) => {{
                    playTone(f, "square", now + idx * 0.06, 0.14, 0.14);
                }});
            }} else if (SOUND_TYPE === "var_start") {{
                playTone(660, "triangle", now, 0.12, 0.16);
                playTone(660, "triangle", now + 0.18, 0.12, 0.16);
            }} else if (SOUND_TYPE === "inning_clear") {{
                [440, 554, 659, 880].forEach((f, idx) => {{
                    playTone(f, "triangle", now + idx * 0.09, 0.18, 0.16);
                }});
            }} else if (SOUND_TYPE === "gameover") {{
                playTone(440, "triangle", now, 0.2, 0.16);
                playTone(392, "triangle", now + 0.22, 0.2, 0.16);
                playTone(349, "triangle", now + 0.44, 0.4, 0.16);
            }}
        }}

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
                    playNoise(t, 0.05, 0.06);
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


def go_home():
    st.session_state.phase = "start"
    st.session_state.paused = False
    st.session_state.foul_active = False
    st.session_state.fever_until = 0.0


def toggle_pause():
    now = time.time()
    if not st.session_state.paused:
        st.session_state.paused = True
        st.session_state.pause_started_at = now
    else:
        paused_dur = now - st.session_state.pause_started_at
        st.session_state.inning_start_time += paused_dur
        st.session_state.last_sec_tick += paused_dur
        st.session_state.last_foul_end += paused_dur
        if st.session_state.fever_until > 0:
            st.session_state.fever_until += paused_dur
        if st.session_state.foul_active:
            st.session_state.foul_deadline += paused_dur
        if st.session_state.stun_until > 0:
            st.session_state.stun_until += paused_dur
        if st.session_state.cleaning_until > 0:
            st.session_state.cleaning_until += paused_dur
        if st.session_state.var_until > 0:
            st.session_state.var_until += paused_dur

        for cust in st.session_state.customers:
            cust["spawn_time"] += paused_dur

        for slot in st.session_state.chicken_slots + st.session_state.shrimp_slots:
            if slot["start_time"] > 0:
                slot["start_time"] += paused_dur
            if slot["ready_time"] > 0:
                slot["ready_time"] += paused_dur

        st.session_state.paused = False
        st.session_state.pause_started_at = 0.0


def get_max_customer_slots(now: float) -> int:
    """5회말 클리닝 타임 러시 중에는 대기석 6칸 확장, 평상시 4칸"""
    return 6 if now < st.session_state.cleaning_until else 4


def spawn_customer(now: float, is_fever: bool):
    max_slots = get_max_customer_slots(now)
    if len(st.session_state.customers) >= max_slots:
        return

    stadium_cfg = STADIUMS[st.session_state.stadium]
    menu_names = list(MENUS.keys())
    weights = [stadium_cfg["weights"][m] for m in menu_names]
    chosen_menu = random.choices(menu_names, weights=weights, k=1)[0]

    inning = st.session_state.get("inning", 1)
    cust_type = "normal"

    # 야구팬 밈 특수 손님 확률 배정
    r = random.random()
    if r < stadium_cfg["cheer_prob"]:
        cust_type = "cheerleader"
    elif inning >= 2 and r < stadium_cfg["cheer_prob"] + 0.14:
        cust_type = "saint"  # 보살팬
    elif inning >= 3 and r < stadium_cfg["cheer_prob"] + 0.25:
        cust_type = "impatient"  # 성격 급한 단골
    elif inning >= 3 and r < stadium_cfg["cheer_prob"] + 0.33:
        cust_type = "catcher"  # 포수장비 풀착장 팬

    if cust_type == "cheerleader":
        avatar, role = "📣", "열혈 응원단장"
        base_patience = random.randint(17, 22)
    elif cust_type == "impatient":
        avatar, role = "⚡", "성격 급한 단골"
        base_patience = random.randint(11, 14)
    elif cust_type == "saint":
        avatar, role = "🙏", "해탈한 보살팬"
        base_patience = random.randint(25, 30)
    elif cust_type == "catcher":
        avatar, role = "🧤", "포수장비 풀착장팬"
        base_patience = random.randint(17, 21)
    else:
        avatar, role = random.choice(CUSTOMER_PROFILES)
        base_patience = random.randint(15, 20) if not is_fever else random.randint(14, 18)

    st.session_state.customer_seq += 1
    st.session_state.customers.append(
        {
            "id": st.session_state.customer_seq,
            "avatar": avatar,
            "role": role,
            "cust_type": cust_type,
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
    st.session_state.cleaning_triggered = False
    st.session_state.walkoff_triggered = False

    spawn_customer(now, False)
    spawn_customer(now, False)


def advance_to_next_inning():
    now = time.time()
    inning = st.session_state.inning
    cfg = INNING_CONFIG[inning]
    if st.session_state.inning_gold >= cfg["target"]:
        if inning < 9:
            trigger_sound("inning_clear")
            st.session_state.gain_banner = (f"⏭️ {inning}회 조기 달성! {inning + 1}회로 즉시 진출합니다!", now + 2.5)
            init_inning(inning + 1, now)
        else:
            finalize_game(victory=True)


def start_new_game():
    now = time.time()
    st.session_state.phase = "playing"
    st.session_state.paused = False
    st.session_state.pause_started_at = 0.0
    st.session_state.victory = False
    st.session_state.total_gold = 0
    st.session_state.combo = 0
    st.session_state.max_combo = 0
    st.session_state.fever_gauge = 0
    st.session_state.fever_until = 0.0
    st.session_state.cleaning_until = 0.0
    st.session_state.var_until = 0.0
    st.session_state.var_pending_type = ""
    st.session_state.foul_catches = 0
    st.session_state.linedrive_catches = 0
    st.session_state.foul_type = "fly"
    st.session_state.foul_pos = 1
    st.session_state.burned_count = 0
    st.session_state.customer_seq = 0
    st.session_state.sold_counts = {m: 0 for m in MENUS}
    st.session_state.gain_banner = ("", 0.0)
    st.session_state.records_saved = False

    st.session_state.chicken_slots = [
        {"state": "idle", "start_time": 0.0, "ready_time": 0.0},
        {"state": "idle", "start_time": 0.0, "ready_time": 0.0},
    ]
    st.session_state.shrimp_slots = [
        {"state": "idle", "start_time": 0.0, "ready_time": 0.0},
        {"state": "idle", "start_time": 0.0, "ready_time": 0.0},
    ]

    st.session_state.home_score = 2
    st.session_state.away_score = 2
    st.session_state.strikes = 0
    st.session_state.balls = 0
    st.session_state.outs = 0
    st.session_state.bases = [False, False, False]
    st.session_state.ticker_msg = f"⚾ {st.session_state.stadium} 플레이볼! 첫 손님들이 매점으로 몰려옵니다!"

    st.session_state.last_sec_tick = now
    st.session_state.last_foul_end = now
    init_inning(1, now)
    trigger_sound("inning_clear")


def ensure_state():
    if "phase" not in st.session_state:
        st.session_state.phase = "start"
        st.session_state.stadium = "잠실야구장 (치맥의 성지)"
        st.session_state.paused = False
        st.session_state.sound_id = 0
        st.session_state.sound_type = ""
        st.session_state.sound_muted = False
        st.session_state.best_gold = 0
        st.session_state.best_combo = 0
        st.session_state.best_catches = 0
        st.session_state.unlocked_titles = []


# ==========================================
# 5. 실시간 게임 로직 업데이트 (1초 주기)
# ==========================================
def activate_fever(now: float, reason: str):
    st.session_state.fever_gauge = 100
    st.session_state.fever_until = now + 10.0
    st.session_state.ticker_msg = f"🔥 {reason} 10초간 피버 타임 발동!! (조리 1초 / 수익 1.5배)"
    trigger_sound("fever_start")


def spawn_ball_event(now: float, ball_type: str):
    """파울 플라이(3.5s) / 총알 라인드라이브(2.0s) / 기록 홈런볼(2.8s) 발동"""
    # 대기석에 '포수장비 풀착장팬'이 있으면 파울볼을 대신 캐치해주는 야구팬 밈 기믹!
    catcher_fans = [c for c in st.session_state.customers if c.get("cust_type") == "catcher"]
    if catcher_fans and ball_type in ("fly", "linedrive"):
        fan = catcher_fans[0]
        st.session_state.foul_catches += 1
        st.session_state.last_foul_end = now
        bonus = 15000
        st.session_state.inning_gold += bonus
        st.session_state.total_gold += bonus
        st.session_state.gain_banner = (
            f"🧤 [{fan['role']}]이(가) 날아오는 파울볼을 대신 낚아챘습니다! (+15,000G 자동 캐치)",
            now + 2.8,
        )
        trigger_sound("foul_catch")
        return

    st.session_state.foul_active = True
    st.session_state.foul_type = ball_type
    st.session_state.foul_pos = random.choice([0, 1, 2])
    if ball_type == "linedrive":
        st.session_state.foul_deadline = now + 2.0
        trigger_sound("linedrive_alert")
    elif ball_type == "homerunball":
        st.session_state.foul_deadline = now + 2.8
        trigger_sound("foul_alert")
    else:
        st.session_state.foul_deadline = now + 3.5
        trigger_sound("foul_alert")


def advance_scoreboard(now: float, is_fever: bool):
    # 비디오 판독(VAR) 진행 중이면 판독 종료 시 결과 발표
    if st.session_state.var_until > 0:
        if now >= st.session_state.var_until:
            pending = st.session_state.var_pending_type
            st.session_state.var_until = 0.0
            st.session_state.var_pending_type = ""
            if random.random() < 0.65:
                # 판독 번복 세이프 / 홈런 인정!
                st.session_state.home_score += 1
                st.session_state.ticker_msg = f"📺 비디오 판독 결과: 원심 번복 [{pending} 인정!!] 구장이 열광합니다!"
                if not is_fever:
                    activate_fever(now, "비디오 판독 번복 득점!")
            else:
                st.session_state.outs = min(2, st.session_state.outs + 1)
                st.session_state.ticker_msg = f"📺 비디오 판독 결과: 원심 유지 [아웃] 관중석에서 탄식이 터집니다."
        return

    stadium_cfg = STADIUMS[st.session_state.stadium]
    events = ["ball", "strike", "foul_tip", "hit", "double", "homerun", "var_check", "out"]
    weights = [26, 26, 11, 13, 6, stadium_cfg["hr_weight"], 4, 10]
    ev = random.choices(events, weights=weights, k=1)[0]

    b1, b2, b3 = st.session_state.bases

    if ev == "var_check":
        st.session_state.var_until = now + 4.0
        st.session_state.var_pending_type = random.choice(["홈런/파울", "홈 태그 세이프"])
        st.session_state.ticker_msg = f"🚨 심판진 비디오 판독(VAR) 요청! ({st.session_state.var_pending_type} 판독 중...)"
        trigger_sound("var_start")
        return

    if ev == "ball":
        st.session_state.balls += 1
        if st.session_state.balls >= 4:
            st.session_state.balls = 0
            st.session_state.strikes = 0
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
        # 홈런 직후 낮은 확률로 매점 지붕 쪽 기록 홈런볼 쟁탈전 발동
        if not st.session_state.foul_active and random.random() < 0.45:
            spawn_ball_event(now, "homerunball")

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


def evaluate_title():
    sold = st.session_state.sold_counts
    top_menu = max(sold, key=lambda k: sold[k]) if sum(sold.values()) > 0 else "없음"
    top_cnt = sold.get(top_menu, 0)
    burned = st.session_state.burned_count
    catches = st.session_state.foul_catches
    ld_catches = st.session_state.linedrive_catches
    gold = st.session_state.total_gold
    max_combo = st.session_state.max_combo
    victory = st.session_state.victory

    if burned >= 4:
        return "🔥 잠실벌의 치킨 방화범", f"치킨을 {burned}번이나 태워먹은 전설의 숯불 장인!"
    if ld_catches >= 2:
        return "⚡ KBO 골든글러브 유격수 출신 알바", f"총알 라인드라이브 {ld_catches}개 슈퍼 캐치! 반사신경 괴물!"
    if catches >= 5:
        return "🧤 야구장 지붕 파울볼 수호신", f"파울볼 {catches}개 캐치! 선수보다 수비를 더 잘합니다."
    if victory and gold >= 600000:
        return "👑 구단주가 스카우트하려는 매점의 신", "9회말까지 매출 신기록을 갈아치운 직관의 지배자!"
    if top_menu == "생맥주" and top_cnt >= 12:
        return "🍺 야구장 생맥주 거품 장인", f"생맥주 {top_cnt}잔 판매! 목마른 관중들의 영원한 오아시스!"
    if top_menu == "크림새우 & 떡볶이 세트" and top_cnt >= 8:
        return "🍤 크림새우 & 떡볶이 완판 신화", f"프리미엄 세트 {top_cnt}개 돌파! 객단가 수직 상승의 주역!"
    if max_combo >= 15:
        return "🎯 리듬게임 고인물 출신 서빙 머신", f"최대 {max_combo}콤보 달성! 한 치의 오차도 없는 손놀림!"
    if victory:
        return "⚾ 9회말 끝내기 승리의 숨은 MVP", "끝까지 매점을 지켜낸 듬직한 야구장 에이스 알바생!"
    return "🐣 병아리 매점 수습생", "아쉽게 목표 매출 미달! 다음 경기에선 파울볼과 손님 인내심을 사수하세요!"


def finalize_game(victory: bool):
    st.session_state.phase = "gameover"
    st.session_state.paused = False
    st.session_state.victory = victory
    trigger_sound("inning_clear" if victory else "gameover")

    if not st.session_state.get("records_saved", False):
        st.session_state.records_saved = True
        st.session_state.best_gold = max(st.session_state.best_gold, st.session_state.total_gold)
        st.session_state.best_combo = max(st.session_state.best_combo, st.session_state.max_combo)
        st.session_state.best_catches = max(st.session_state.best_catches, st.session_state.foul_catches)
        t_name, _ = evaluate_title()
        if t_name not in st.session_state.unlocked_titles:
            st.session_state.unlocked_titles.append(t_name)


def process_game_tick():
    if st.session_state.phase != "playing" or st.session_state.paused:
        return

    now = time.time()
    inning = st.session_state.inning
    cfg = INNING_CONFIG[inning]
    elapsed_inning = now - st.session_state.inning_start_time
    time_left = cfg["duration"] - elapsed_inning
    is_bottom = elapsed_inning >= (cfg["duration"] / 2.0)

    # 5회말 시작 시(클리닝 타임 러시 발동: 12초간 손님 6칸 & 매출 2배)
    if inning == 5 and is_bottom and not st.session_state.cleaning_triggered:
        st.session_state.cleaning_triggered = True
        st.session_state.cleaning_until = now + 12.0
        st.session_state.ticker_msg = "🧹 5회말 클리닝 타임! 화장실·매점 관중 대폭발! (대기석 6칸 확장 & 매출 2배!)"
        trigger_sound("fever_start")
        for _ in range(3):
            spawn_customer(now, True)

    # 9회말 막판 14초 '끝내기 찬스' 발동
    if inning == 9 and is_bottom and not st.session_state.walkoff_triggered:
        st.session_state.walkoff_triggered = True
        st.session_state.bases = [True, True, True]
        st.session_state.outs = 2
        st.session_state.strikes = 2
        st.session_state.balls = 3
        activate_fever(now, "9회말 2아웃 만루 풀카운트 끝내기 찬스!!")

    # 1) 피버 타임 종료 체크
    if st.session_state.fever_until > 0 and now >= st.session_state.fever_until:
        st.session_state.fever_until = 0.0
        st.session_state.fever_gauge = 0
        st.session_state.ticker_msg = "📣 피버 타임 종료! 다시 집중해서 서빙하세요!"

    is_fever = now < st.session_state.fever_until

    # 2) 파울볼/홈런볼 제한시간 초과 체크
    if st.session_state.foul_active and now >= st.session_state.foul_deadline:
        b_type = st.session_state.foul_type
        st.session_state.foul_active = False
        st.session_state.last_foul_end = now
        if b_type == "homerunball":
            st.session_state.ticker_msg = "💨 아깝다! 기록 홈런볼이 옆 구역 관중에게 넘어갔습니다."
        else:
            st.session_state.stun_until = now + 2.0
            st.session_state.combo = 0
            trigger_sound("foul_miss")
            st.toast("💥 파울볼이 매점에 떨어졌습니다! 2초간 조리/서빙 정지 & 콤보 초기화!", icon="⚠️")

    # 3) 조리대 상태 갱신
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

    # 4) 손님 인내심 체크 (풀카운트 3B-2S 또는 비디오 판독 중에는 관중이 전광판을 보느라 인내심 감소 1초 보정!)
    is_full_count = (st.session_state.balls == 3 and st.session_state.strikes == 2)
    is_var = now < st.session_state.var_until
    if is_full_count or is_var:
        for cust in st.session_state.customers:
            cust["spawn_time"] += 0.9

    remaining_customers = []
    for cust in st.session_state.customers:
        if now - cust["spawn_time"] >= cust["max_patience"]:
            st.session_state.combo = 0
            st.toast(f"😡 {cust['role']} 손님이 기다리다 화나서 떠났습니다! (콤보 초기화)", icon="💨")
        else:
            remaining_customers.append(cust)
    st.session_state.customers = remaining_customers

    # 5) 1초 주기 이벤트
    if now - st.session_state.last_sec_tick >= 0.95:
        st.session_state.last_sec_tick = now
        advance_scoreboard(now, is_fever)

        is_cleaning = now < st.session_state.cleaning_until
        if is_fever or is_cleaning:
            spawn_customer(now, True)
            if len(st.session_state.customers) < get_max_customer_slots(now) - 1:
                spawn_customer(now, True)
        else:
            if len(st.session_state.customers) == 0 or random.random() < 0.45:
                spawn_customer(now, False)

        # 파울볼 돌발 이벤트 (플라이 70% / 총알 라인드라이브 30%)
        if (
            not st.session_state.foul_active
            and now >= st.session_state.stun_until
            and (now - st.session_state.last_foul_end) >= 4.0
            and random.random() < 0.13
        ):
            b_type = "linedrive" if random.random() < 0.30 else "fly"
            spawn_ball_event(now, b_type)

    # 6) 현재 이닝 제한 시간 종료 판정
    if time_left <= 0:
        if st.session_state.inning_gold >= cfg["target"]:
            if inning < 9:
                trigger_sound("inning_clear")
                st.toast(f"🎉 {inning}회 목표 매출 달성! {inning + 1}회로 진출합니다!", icon="⚾")
                init_inning(inning + 1, now)
            else:
                finalize_game(victory=True)
                st.rerun()
        else:
            finalize_game(victory=False)
            st.rerun()


# ==========================================
# 6. 플레이어 액션 핸들러
# ==========================================
def complete_serving(menu_name: str, target_cust_id: int = None) -> bool:
    now = time.time()
    if st.session_state.paused:
        return False
    if now < st.session_state.stun_until:
        st.toast("💫 매점이 흔들려 잠시 움직일 수 없습니다!", icon="⏳")
        return False

    if target_cust_id is not None:
        matching = [c for c in st.session_state.customers if c["id"] == target_cust_id and c["menu"] == menu_name]
    else:
        matching = [c for c in st.session_state.customers if c["menu"] == menu_name]

    if not matching:
        st.toast(f"❓ '{menu_name}'을(를) 주문한 손님이 없습니다!", icon="😅")
        return False

    matching.sort(key=lambda c: c["max_patience"] - (now - c["spawn_time"]))
    target_cust = matching[0]
    st.session_state.customers = [c for c in st.session_state.customers if c["id"] != target_cust["id"]]

    is_fever = now < st.session_state.fever_until
    is_cleaning = now < st.session_state.cleaning_until
    stadium_cfg = STADIUMS[st.session_state.stadium]

    base_price = MENUS[menu_name]["price"]
    if menu_name == "크림새우 & 떡볶이 세트":
        base_price = int(base_price * stadium_cfg["shrimp_mult"])

    st.session_state.combo += 1
    st.session_state.max_combo = max(st.session_state.max_combo, st.session_state.combo)

    cust_type = target_cust.get("cust_type", "normal")
    price_mult = 2.0 if cust_type == "cheerleader" else 1.0
    tip_mult = 3.0 if cust_type == "impatient" else 1.0
    event_mult = (1.5 if is_fever else 1.0) * (2.0 if is_cleaning else 1.0)

    combo_tip = int(st.session_state.combo * 400 * tip_mult)
    earned = int((base_price * price_mult + combo_tip) * event_mult)

    st.session_state.inning_gold += earned
    st.session_state.total_gold += earned
    st.session_state.sold_counts[menu_name] += 1

    bonus_tag = (
        " [응원단장 2배!]"
        if cust_type == "cheerleader"
        else (" [단골 팁 3배!]" if cust_type == "impatient" else (" [클리닝타임 2배!]" if is_cleaning else ""))
    )
    st.session_state.gain_banner = (
        f"💰 +{earned:,}G 획득! ({st.session_state.combo} COMBO!){bonus_tag}",
        now + 2.2,
    )

    if not is_fever:
        gauge_gain = 18 if "사직" in st.session_state.stadium else 14
        st.session_state.fever_gauge = min(100, st.session_state.fever_gauge + gauge_gain)
        if st.session_state.fever_gauge >= 100:
            activate_fever(now, "피버 게이지 100% 충전!")
        else:
            trigger_sound("serve")
    else:
        trigger_sound("serve")

    return True


def handle_direct_customer_serve(cust_id: int, menu_name: str):
    now = time.time()
    if st.session_state.paused or now < st.session_state.stun_until:
        return

    if MENUS[menu_name]["cook_time"] == 0:
        complete_serving(menu_name, target_cust_id=cust_id)
    elif menu_name == "순살치킨":
        for slot in st.session_state.chicken_slots:
            if slot["state"] == "ready":
                if complete_serving(menu_name, target_cust_id=cust_id):
                    slot["state"] = "idle"
                    slot["start_time"] = 0.0
                    slot["ready_time"] = 0.0
                return
    elif menu_name == "크림새우 & 떡볶이 세트":
        for slot in st.session_state.shrimp_slots:
            if slot["state"] == "ready":
                if complete_serving(menu_name, target_cust_id=cust_id):
                    slot["state"] = "idle"
                    slot["start_time"] = 0.0
                    slot["ready_time"] = 0.0
                return


def handle_start_cook(slot_list_key: str, idx: int):
    now = time.time()
    if st.session_state.paused:
        return
    if now < st.session_state.stun_until:
        st.toast("💫 매점이 흔들려 조리를 시작할 수 없습니다!", icon="⏳")
        return
    slot = st.session_state[slot_list_key][idx]
    if slot["state"] == "idle":
        slot["state"] = "cooking"
        slot["start_time"] = now
        slot["ready_time"] = 0.0


def handle_serve_cooked(slot_list_key: str, idx: int, menu_name: str):
    if st.session_state.paused:
        return
    slot = st.session_state[slot_list_key][idx]
    if slot["state"] == "ready":
        if complete_serving(menu_name):
            slot["state"] = "idle"
            slot["start_time"] = 0.0
            slot["ready_time"] = 0.0


def handle_discard_burned(idx: int):
    if st.session_state.paused:
        return
    slot = st.session_state.chicken_slots[idx]
    if slot["state"] == "burned":
        slot["state"] = "idle"
        slot["start_time"] = 0.0
        slot["ready_time"] = 0.0
        st.toast("🗑️ 탄 치킨을 폐기했습니다. 다시 조리할 수 있습니다.", icon="🧹")


def handle_catch_foul():
    now = time.time()
    if st.session_state.paused:
        return
    if st.session_state.foul_active and now < st.session_state.foul_deadline:
        b_type = st.session_state.foul_type
        st.session_state.foul_active = False
        st.session_state.last_foul_end = now
        st.session_state.foul_catches += 1

        if b_type == "linedrive":
            st.session_state.linedrive_catches += 1
            bonus = 25000
            gauge_add = 70
            msg = "⚡ 미친 반사신경! 총알 라인드라이브 슈퍼 캐치!! (+25,000G & 피버 +70%)"
        elif b_type == "homerunball":
            bonus = 50000
            gauge_add = 100
            msg = "🎆 전설의 기록 홈런볼 쟁탈 성공!! 잭팟 보너스 +50,000G!!"
        else:
            bonus = 12000
            gauge_add = 45
            msg = "🧤 나이스 캐치!! 파울볼 보너스 +12,000G & 피버 +45%!"

        st.session_state.inning_gold += bonus
        st.session_state.total_gold += bonus
        st.session_state.gain_banner = (msg, now + 2.6)
        trigger_sound("foul_catch")

        if now >= st.session_state.fever_until:
            st.session_state.fever_gauge = min(100, st.session_state.fever_gauge + gauge_add)
            if st.session_state.fever_gauge >= 100:
                activate_fever(now, "슈퍼 캐치로 피버 타임 폭발!")


# ==========================================
# 7. UI 렌더링 함수
# ==========================================
def render_scoreboard(now: float, is_fever: bool):
    inning = st.session_state.inning
    cfg = INNING_CONFIG[inning]
    elapsed_inning = now - st.session_state.inning_start_time
    half_str = f"{inning}회말 공격" if elapsed_inning >= (cfg["duration"] / 2.0) else f"{inning}회초 수비"

    s = st.session_state.strikes
    b = st.session_state.balls
    o = st.session_state.outs
    b1, b2, b3 = st.session_state.bases
    en_stadium = STADIUMS[st.session_state.stadium]["en_name"]

    b_dots = "".join(['<span class="dot-b">●</span>' if i < b else '<span class="dot-off">●</span>' for i in range(3)])
    s_dots = "".join(['<span class="dot-s">●</span>' if i < s else '<span class="dot-off">●</span>' for i in range(2)])
    o_dots = "".join(['<span class="dot-o">●</span>' if i < o else '<span class="dot-off">●</span>' for i in range(2)])

    crowd_html = (
        '<span class="crowd-wave">🙌📣⚾🔥🙌📣⚾🔥</span>'
        if is_fever
        else '<span style="font-size:1.05rem; opacity:0.85;">⚾🏟️🧢🌭</span>'
    )

    html = f"""
    <div class="scoreboard-wrap">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <div>
                <div class="sb-title">🏟️ {en_stadium} LIVE</div>
                <div style="font-size:0.88rem; color:#cbd5e1; margin-top:2px;">
                    현재 경기: <strong style="color:#facc15; font-size:1rem;">{half_str}</strong> &nbsp;|&nbsp; {crowd_html}
                </div>
            </div>
            <div style="display:flex; gap:8px; align-items:center;">
                <div class="sb-score-box">
                    <div class="sb-team">AWAY</div>
                    <div class="sb-num away">{st.session_state.away_score}</div>
                </div>
                <div style="font-weight:900; color:#64748b; font-size:1.1rem;">VS</div>
                <div class="sb-score-box">
                    <div class="sb-team">HOME</div>
                    <div class="sb-num">{st.session_state.home_score}</div>
                </div>
            </div>
            <div style="display:flex; gap:14px; align-items:center; background:#050811; padding:5px 12px; border-radius:10px; border:1px solid #2b3a55;">
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

    c1, c2, c3, c4, c5 = st.columns([1.05, 1.45, 1.05, 1.0, 1.3])
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
                <div style="background:#e2e8f0; border-radius:6px; height:12px; margin-top:6px; overflow:hidden;">
                    <div style="width:{fever_pct}%; height:100%; background:linear-gradient(90deg,#f59e0b,#ec4899);"></div>
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

    if inning_gold >= target_gold and not st.session_state.paused:
        next_label = (
            f"⏭️ {inning}회 목표 달성 완료! {inning + 1}회로 바로 넘어가기 (또는 남은 시간 동안 추가 콤보 사냥)"
            if inning < 9
            else "🏆 9회말 목표 달성 완료! 지금 바로 영업 종료 & 영수증 확인하기"
        )
        st.button(
            next_label,
            key=f"btn_early_next_{inning}",
            type="primary",
            use_container_width=True,
            on_click=advance_to_next_inning,
        )


def render_alerts(now: float, is_fever: bool):
    # 1회차 동적 가이드
    if st.session_state.inning == 1 and st.session_state.total_gold == 0 and st.session_state.customers:
        first_menu = st.session_state.customers[0]["menu"]
        if MENUS[first_menu]["cook_time"] == 0:
            tip_msg = f"💡 가이드: 첫 손님이 [{first_menu}]를 주문했습니다! 손님 카드의 [⚡ 바로 서빙] 또는 오른쪽 버튼을 누르세요!"
        else:
            tip_msg = f"💡 가이드: 첫 손님이 [{first_menu}]를 주문했습니다! 오른쪽 조리대에서 먼저 [🔥 조리 시작]을 누르세요!"
        st.markdown(f'<div class="tutorial-tip">{tip_msg}</div>', unsafe_allow_html=True)

    # 서빙 성공 즉각 시각 피드백 배너
    banner_msg, banner_until = st.session_state.gain_banner
    if banner_msg and now < banner_until:
        st.markdown(f'<div class="gain-popup">{banner_msg}</div>', unsafe_allow_html=True)

    # 5회말 클리닝 타임 러시 배너
    if now < st.session_state.cleaning_until:
        clean_left = max(0.0, st.session_state.cleaning_until - now)
        st.markdown(
            f'<div class="special-banner">🧹 5회말 클리닝 타임 러시! ({clean_left:.1f}초) — 대기석 6칸 확장 & 모든 판매가 2배!</div>',
            unsafe_allow_html=True,
        )

    # 비디오 판독(VAR) 또는 풀카운트(3B-2S) 관중 집중 보너스 안내
    if now < st.session_state.var_until:
        var_left = max(0.0, st.session_state.var_until - now)
        st.markdown(
            f'<div class="var-banner">📺 비디오 판독(VAR) 진행 중 ({var_left:.1f}초) — 관중들이 전광판에 집중하여 손님 인내심이 멈춥니다!</div>',
            unsafe_allow_html=True,
        )
    elif st.session_state.balls == 3 and st.session_state.strikes == 2:
        st.markdown(
            '<div class="special-banner">🔥 풀카운트(3B-2S) 승부! 손님들이 숨죽이고 경기를 지켜봐 인내심 감소가 멈춥니다!</div>',
            unsafe_allow_html=True,
        )

    if is_fever:
        fever_left = max(0.0, st.session_state.fever_until - now)
        st.markdown(
            f"""<div class="fever-banner">
                <span class="crowd-wave">🙌📣⚾🔥</span>
                &nbsp; FEVER TIME 발동 중! ({fever_left:.1f}초) — 조리 1초 단축 & 판매가 1.5배! &nbsp;
                <span class="crowd-wave">🔥⚾📣🙌</span>
            </div>""",
            unsafe_allow_html=True,
        )

    # 파울볼 / 라인드라이브 / 홈런볼 미니게임
    if st.session_state.foul_active:
        foul_left = max(0.0, st.session_state.foul_deadline - now)
        b_type = st.session_state.foul_type
        if b_type == "linedrive":
            alert_html = f'<div class="foul-banner linedrive">⚡ 총알 같은 파울 라인드라이브!! {foul_left:.1f}초 안에 즉각 반응하세요!</div>'
            btn_label = "⚡ 라인드라이브 슈퍼 캐치! (+25,000G)"
        elif b_type == "homerunball":
            alert_html = f'<div class="foul-banner homerunball">🎆 매점 지붕으로 기록 홈런볼이 날아옵니다!! {foul_left:.1f}초 안에 쟁탈하세요!</div>'
            btn_label = "🎆 전설의 홈런볼 쟁탈! (+50,000G)"
        else:
            alert_html = f'<div class="foul-banner">⚠️ 높이 뜬 파울 플라이! {foul_left:.1f}초 안에 글러브로 잡아내세요!</div>'
            btn_label = "🧤 글러브로 캐치! (+12,000G)"

        st.markdown(alert_html, unsafe_allow_html=True)
        f_cols = st.columns(3)
        pos = st.session_state.foul_pos
        with f_cols[pos]:
            st.button(
                btn_label,
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


def is_menu_ready_to_serve(menu_name: str) -> bool:
    if MENUS[menu_name]["cook_time"] == 0:
        return True
    if menu_name == "순살치킨":
        return any(s["state"] == "ready" for s in st.session_state.chicken_slots)
    if menu_name == "크림새우 & 떡볶이 세트":
        return any(s["state"] == "ready" for s in st.session_state.shrimp_slots)
    return False


def render_customers(now: float, is_fever: bool):
    max_slots = get_max_customer_slots(now)
    st.subheader(f"🙋‍♂️ 주문 대기 손님 (최대 {max_slots}팀)")
    grid_cols = st.columns(2)
    customers = st.session_state.customers
    stunned = now < st.session_state.stun_until
    is_cleaning = now < st.session_state.cleaning_until
    shrimp_mult = STADIUMS[st.session_state.stadium]["shrimp_mult"]

    for i in range(max_slots):
        with grid_cols[i % 2]:
            if i < len(customers):
                cust = customers[i]
                menu_name = cust["menu"]
                info = MENUS[menu_name]
                cust_type = cust.get("cust_type", "normal")
                rem = max(0.0, cust["max_patience"] - (now - cust["spawn_time"]))
                ratio = max(0.0, min(1.0, rem / cust["max_patience"]))

                type_cls_map = {
                    "cheerleader": "vip-cheer",
                    "impatient": "vip-rush",
                    "saint": "vip-saint",
                    "catcher": "vip-catcher",
                }
                card_cls = "urgent" if ratio <= 0.35 else type_cls_map.get(cust_type, "")
                bar_color = "#22c55e" if ratio > 0.55 else ("#f59e0b" if ratio > 0.35 else "#ef4444")

                base_p = info["price"] * (shrimp_mult if menu_name == "크림새우 & 떡볶이 세트" else 1.0)
                price_mult = 2.0 if cust_type == "cheerleader" else 1.0
                event_mult = (1.5 if is_fever else 1.0) * (2.0 if is_cleaning else 1.0)
                disp_price = int(base_p * price_mult * event_mult)

                vip_tag = ""
                if cust_type == "cheerleader":
                    vip_tag = '<span class="vip-badge cheer">기본가 2배</span>'
                elif cust_type == "impatient":
                    vip_tag = '<span class="vip-badge rush">팁 3배</span>'
                elif cust_type == "saint":
                    vip_tag = '<span class="vip-badge saint">보살 인내심</span>'
                elif cust_type == "catcher":
                    vip_tag = '<span class="vip-badge catcher">파울 대리캐치</span>'

                st.markdown(
                    f"""
                    <div class="cust-card {card_cls}">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-weight:800; font-size:0.88rem;">{cust['avatar']} {cust['role']}{vip_tag}</span>
                            <span style="font-size:0.8rem; font-weight:700; color:{bar_color};">⏳ {rem:.1f}초</span>
                        </div>
                        <div style="font-size:1.02rem; font-weight:900; margin:4px 0 2px 0;">
                            {info['icon']} {menu_name}
                        </div>
                        <div style="font-size:0.78rem; color:#475569; margin-bottom:4px;">
                            예상 {disp_price:,}G + 콤보팁
                        </div>
                        <div style="background:#e2e8f0; height:7px; border-radius:4px; overflow:hidden;">
                            <div style="width:{int(ratio*100)}%; height:100%; background:{bar_color};"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                can_serve = is_menu_ready_to_serve(menu_name)
                btn_txt = f"⚡ {info['icon']} 바로 서빙하기!" if can_serve else f"⏳ {menu_name} 조리 필요"
                st.button(
                    btn_txt,
                    key=f"direct_serve_{cust['id']}",
                    type="primary" if can_serve else "secondary",
                    use_container_width=True,
                    disabled=(not can_serve) or stunned,
                    on_click=handle_direct_customer_serve,
                    args=(cust["id"], menu_name),
                )
            else:
                st.markdown(
                    '<div class="cust-card empty">👟 다음 손님 입장 대기 중...</div>',
                    unsafe_allow_html=True,
                )


def render_kitchen(now: float, is_fever: bool):
    st.subheader("🍳 매점 조리대 & 즉시 서빙")
    stunned = now < st.session_state.stun_until
    is_cleaning = now < st.session_state.cleaning_until
    event_mult = (1.5 if is_fever else 1.0) * (2.0 if is_cleaning else 1.0)
    shrimp_mult = STADIUMS[st.session_state.stadium]["shrimp_mult"]
    wanted_menus = {c["menu"] for c in st.session_state.customers}

    st.markdown("**⚡ 즉시 서빙 코너 (주문 손님 있을 시 강조 표시)**")
    ic1, ic2 = st.columns(2)
    with ic1:
        p_beer = int(MENUS["생맥주"]["price"] * event_mult)
        beer_wanted = "생맥주" in wanted_menus
        st.button(
            f"🍺 생맥주 서빙 ({p_beer:,}G)" + (" 🔥주문!" if beer_wanted else ""),
            key="serve_beer",
            type="primary" if beer_wanted else "secondary",
            use_container_width=True,
            disabled=stunned,
            on_click=complete_serving,
            args=("생맥주",),
        )
    with ic2:
        p_nacho = int(MENUS["나초 & 치즈"]["price"] * event_mult)
        nacho_wanted = "나초 & 치즈" in wanted_menus
        st.button(
            f"🧀 나초 & 치즈 ({p_nacho:,}G)" + (" 🔥주문!" if nacho_wanted else ""),
            key="serve_nacho",
            type="primary" if nacho_wanted else "secondary",
            use_container_width=True,
            disabled=stunned,
            on_click=complete_serving,
            args=("나초 & 치즈",),
        )

    st.markdown("---")

    c_cook_req = 1.0 if is_fever else 3.0
    p_chicken = int(MENUS["순살치킨"]["price"] * event_mult)
    chicken_wanted = "순살치킨" in wanted_menus
    st.markdown(
        f"**🍗 순살치킨 튀김기 ({p_chicken:,}G | 조리 {int(c_cook_req)}초 · 완성 후 7초 내 서빙!)**"
        + (" — 🔥손님 주문 중!" if chicken_wanted else "")
    )
    cc1, cc2 = st.columns(2)
    for idx, col in enumerate([cc1, cc2]):
        slot = st.session_state.chicken_slots[idx]
        with col:
            if slot["state"] == "idle":
                st.markdown(
                    f'<div class="cook-card"><strong>튀김기 #{idx+1}</strong><br><span style="font-size:0.82rem;">대기 중</span></div>',
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
                        <strong>튀김기 #{idx+1} · 조리 중 ({rem:.1f}초)</strong>
                        <div style="background:#fde68a; height:7px; border-radius:4px; margin-top:5px;">
                            <div style="width:{pct}%; height:100%; background:#d97706;"></div>
                        </div>
                    </div>""",
                    unsafe_allow_html=True,
                )
                st.button("⏳ 튀기는 중...", key=f"chk_wait_{idx}", use_container_width=True, disabled=True)
            elif slot["state"] == "ready":
                burn_rem = max(0.0, 7.0 - (now - slot["ready_time"]))
                burn_pct = min(100, int((burn_rem / 7.0) * 100))
                ready_cls = "ready-match" if chicken_wanted else "ready"
                st.markdown(
                    f"""<div class="cook-card {ready_cls}">
                        <strong>✅ 치킨 완성! (타기까지 {burn_rem:.1f}초)</strong>
                        <div style="background:#a7f3d0; height:7px; border-radius:4px; margin-top:5px;">
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
                    f'<div class="cook-card burned"><strong>💀 튀김기 #{idx+1} · 새까맣게 탐!</strong><br><span style="font-size:0.8rem;">폐기해야 재사용 가능</span></div>',
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

    s_cook_req = 1.0 if is_fever else 5.0
    p_shrimp = int(MENUS["크림새우 & 떡볶이 세트"]["price"] * shrimp_mult * event_mult)
    shrimp_wanted = "크림새우 & 떡볶이 세트" in wanted_menus
    st.markdown(
        f"**🍤 크림새우 & 떡볶이 세트 팬 ({p_shrimp:,}G | 조리 {int(s_cook_req)}초 · 고단가)**"
        + (" — 🔥손님 주문 중!" if shrimp_wanted else "")
    )
    sc1, sc2 = st.columns(2)
    for idx, col in enumerate([sc1, sc2]):
        slot = st.session_state.shrimp_slots[idx]
        with col:
            if slot["state"] == "idle":
                st.markdown(
                    f'<div class="cook-card"><strong>전용 팬 #{idx+1}</strong><br><span style="font-size:0.82rem;">대기 중</span></div>',
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
                        <strong>전용 팬 #{idx+1} · 조리 중 ({rem:.1f}초)</strong>
                        <div style="background:#fde68a; height:7px; border-radius:4px; margin-top:5px;">
                            <div style="width:{pct}%; height:100%; background:#d97706;"></div>
                        </div>
                    </div>""",
                    unsafe_allow_html=True,
                )
                st.button("⏳ 조리 중...", key=f"shr_wait_{idx}", use_container_width=True, disabled=True)
            elif slot["state"] == "ready":
                ready_cls = "ready-match" if shrimp_wanted else "ready"
                st.markdown(
                    f'<div class="cook-card {ready_cls}"><strong>✅ 크림새우 & 떡볶이 완성!</strong><br><span style="font-size:0.8rem;">서빙 준비 완료</span></div>',
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
# 8. 시작 화면(홈) & 영수증 결과창
# ==========================================
def render_start_screen():
    st.markdown(NORMAL_BG_CSS, unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align:center; padding: 14px 10px 6px 10px;">
            <div style="font-size:2.9rem;">⚾🍺🍗🍤</div>
            <h1 style="font-family:'Black Han Sans', sans-serif; font-size:2.35rem; margin-bottom:4px; color:#0f172a;">
                야구장 매점 알바 타이쿤: 프로야구 에디션
            </h1>
            <p style="font-size:1.02rem; color:#475569; font-weight:700;">
                원하는 홈구장을 선택하고 1회초부터 9회말 끝내기 승부까지 직관의 열기를 책임지세요!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([0.9, 2.4, 0.9])
    with c2:
        # 구장 선택 셀렉터
        selected_stadium = st.selectbox(
            "🏟️ 오늘 출근할 홈구장을 선택하세요",
            options=list(STADIUMS.keys()),
            index=list(STADIUMS.keys()).index(st.session_state.stadium),
        )
        st.session_state.stadium = selected_stadium
        st.success(f"**구장 특화 보너스:** {STADIUMS[selected_stadium]['desc']}")

        st.info(
            """
            **📋 프로야구 매점 근무 수칙**
            1. **초/말 공수 교대 & 클리닝 타임**: 5회말이 시작되면 **12초간 클리닝 타임 러시(대기석 6칸 & 매출 2배)**가 열립니다.
            2. **비디오 판독(VAR) & 풀카운트**: 판독 중이거나 3B-2S 풀카운트 때는 관중이 경기에 집중해 **손님 인내심 감소가 멈춥니다**.
            3. **야구팬 특수 손님**: **📣 응원단장(기본가 2배)**, **⚡ 성격 급한 단골(팁 3배)**, **🙏 해탈한 보살팬(높은 인내심)**, **🧤 포수장비 풀착장팬(파울볼 자동 대리 캐치!)**
            4. **타구별 수비 미니게임**: 높이 뜬 플라이(3.5초)뿐 아니라 **총알 라인드라이브(2.0초 / 25,000G)**와 **전설의 홈런볼 쟁탈전(50,000G)**까지 잡아야 진정한 에이스!
            """
        )

        col_btn, col_mute = st.columns([3, 1])
        with col_btn:
            if st.button(f"⚾ [{selected_stadium.split()[0]}] 매점 출근하기!", type="primary", use_container_width=True):
                start_new_game()
                st.rerun()
        with col_mute:
            mute_label = "🔇 음소거됨" if st.session_state.sound_muted else "🔊 사운드 ON"
            if st.button(mute_label, use_container_width=True):
                st.session_state.sound_muted = not st.session_state.sound_muted
                st.rerun()

        titles_html = (
            " &nbsp;·&nbsp; ".join([f"<strong>{t}</strong>" for t in st.session_state.unlocked_titles])
            if st.session_state.unlocked_titles
            else "<span style='color:#94a3b8;'>아직 획득한 칭호가 없습니다. 첫 경기를 완주해 보세요!</span>"
        )
        st.markdown(
            f"""
            <div class="hof-card">
                <div style="font-weight:900; font-size:1rem; color:#0f172a; margin-bottom:8px;">
                    🏆 나의 매점 명예의 전당 (세션 기록)
                </div>
                <div style="display:flex; justify-content:space-around; text-align:center; background:#f8fafc; padding:8px; border-radius:8px; margin-bottom:8px;">
                    <div><div style="font-size:0.75rem; color:#64748b;">역대 최고 매출</div><div style="font-weight:900; color:#b91c1c;">{st.session_state.best_gold:,} G</div></div>
                    <div><div style="font-size:0.75rem; color:#64748b;">역대 최대 콤보</div><div style="font-weight:900; color:#d97706;">{st.session_state.best_combo} 콤보</div></div>
                    <div><div style="font-size:0.75rem; color:#64748b;">최다 파울 캐치</div><div style="font-weight:900; color:#059669;">{st.session_state.best_catches} 회</div></div>
                </div>
                <div style="font-size:0.82rem; color:#475569;">
                    🎖️ <strong>수집한 칭호 도감:</strong> {titles_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


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
    en_stadium = STADIUMS[st.session_state.stadium]["en_name"]
    status_text = (
        "🎉 9회말 경기 종료 (완주 성공!)"
        if st.session_state.victory
        else f"💥 {st.session_state.inning}회 영업 종료"
    )

    st.markdown(
        f"""
        <div class="receipt-paper">
            <div class="receipt-header">
                <div style="font-size:1.45rem; font-weight:900;">🧾 야구장 매점 영수증</div>
                <div style="font-size:0.82rem; color:#64748b; margin-top:3px;">{en_stadium}</div>
                <div style="font-size:0.8rem; color:#64748b;">발행일시: {now_str}</div>
                <div style="font-weight:800; color:#0f172a; margin-top:5px;">{status_text}</div>
            </div>
            <div class="receipt-row"><span>🍺 생맥주 판매량</span><span>{sold['생맥주']} 잔</span></div>
            <div class="receipt-row"><span>🧀 나초 & 치즈 판매량</span><span>{sold['나초 & 치즈']} 개</span></div>
            <div class="receipt-row"><span>🍗 순살치킨 판매량</span><span>{sold['순살치킨']} 마리</span></div>
            <div class="receipt-row"><span>🍤 크림새우&떡볶이 세트</span><span>{sold['크림새우 & 떡볶이 세트']} 세트</span></div>
            <div style="border-top:1px dashed #cbd5e1; margin:7px 0;"></div>
            <div class="receipt-row"><span>🏆 최다 판매 메뉴</span><span><strong>{top_menu_str}</strong></span></div>
            <div class="receipt-row"><span>🧤 총 수비 캐치 횟수</span><span><strong>{st.session_state.foul_catches} 회 (라인드라이브 {st.session_state.linedrive_catches}회)</strong></span></div>
            <div class="receipt-row"><span>🔥 최대 연속 콤보</span><span><strong>{st.session_state.max_combo} 콤보</strong></span></div>
            <div class="receipt-row"><span>💀 치킨 폐기 횟수</span><span>{st.session_state.burned_count} 회</span></div>
            <div class="receipt-total">
                <span>총 매출액 (TOTAL)</span>
                <span>{st.session_state.total_gold:,} G</span>
            </div>
            <div class="title-badge">
                <div style="font-size:0.78rem; color:#92400e; font-weight:700;">[ 오늘의 알바생 칭호 ]</div>
                <div style="font-size:1.25rem; font-weight:900; color:#78350f; margin:4px 0;">{title_name}</div>
                <div style="font-size:0.85rem; color:#92400e;">{title_desc}</div>
            </div>
            <div style="text-align:center; font-size:0.78rem; color:#94a3b8; margin-top:12px;">
                *** 이용해 주셔서 감사합니다! THANK YOU! ***
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    c1, c2, c3, c4 = st.columns([0.8, 1.3, 1.3, 0.8])
    with c2:
        if st.button("🏠 첫 화면(구장 선택)으로", use_container_width=True):
            go_home()
            st.rerun()
    with c3:
        if st.button("🔄 같은 구장에서 바로 재도전!", type="primary", use_container_width=True):
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

    now = st.session_state.pause_started_at if st.session_state.paused else time.time()
    is_fever = (not st.session_state.paused) and (now < st.session_state.fever_until)

    st.markdown(FEVER_BG_CSS if is_fever else NORMAL_BG_CSS, unsafe_allow_html=True)

    render_sound_engine(
        st.session_state.sound_id,
        st.session_state.sound_type,
        is_fever,
        st.session_state.sound_muted,
    )

    top_l, top_home, top_pause, top_mute, top_quit = st.columns([3.4, 1.0, 1.05, 1.0, 1.05])
    with top_l:
        short_stadium = st.session_state.stadium.split()[0]
        st.markdown(
            f"<div style='font-weight:900; font-size:1.18rem; padding-top:4px;'>⚾ {short_stadium} 매점 타이쿤 — {st.session_state.inning}회 / 9회</div>",
            unsafe_allow_html=True,
        )
    with top_home:
        if st.button("🏠 홈으로", key="frag_home", use_container_width=True):
            go_home()
            st.rerun()
    with top_pause:
        pause_txt = "▶️ 재개하기" if st.session_state.paused else "⏸️ 일시정지"
        if st.button(pause_txt, key="frag_pause", use_container_width=True):
            toggle_pause()
            st.rerun()
    with top_mute:
        mute_txt = "🔇 음소거" if st.session_state.sound_muted else "🔊 소리ON"
        if st.button(mute_txt, key="frag_mute", use_container_width=True):
            st.session_state.sound_muted = not st.session_state.sound_muted
    with top_quit:
        if st.button("🧾 정산종료", key="frag_quit", use_container_width=True):
            finalize_game(victory=False)
            st.rerun()

    if st.session_state.paused:
        st.warning("⏸️ **게임이 일시정지되었습니다.** 타이머와 손님 인내심이 멈춰 있습니다. 준비되면 상단의 **[▶️ 재개하기]** 버튼을 눌러주세요!")
        render_scoreboard(now, False)
        render_hud(now, False)
        return

    render_scoreboard(now, is_fever)
    render_hud(now, is_fever)
    render_alerts(now, is_fever)

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
