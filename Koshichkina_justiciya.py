import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
import datetime
import os
from PIL import Image
import PyPDF2

# --- 1. НАСТРОЙКА ИИ ---
# Вставь сюда свой ключ из Google AI Studio
API_KEY = "AIzaSyAVHOwKn0QZoVt3R0PFujfg5ivIZsSohU4" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')


st.set_page_config(page_title="🐾Кошичкина Юстицыя🐾", page_icon="🐾", layout="wide")

# --- 2. SUPREME INTERFACE STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    h1, h2, h3 { color: #d4af37 !important; font-family: 'Georgia', serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #7a631d 100%);
        color: #fff !important; border-radius: 15px; font-weight: 900; height: 5em; width: 100%;
        border: 1px solid #d4af37; box-shadow: 0 4px 25px rgba(212, 175, 55, 0.3);
    }
    .stMetric { background-color: #1c2128; border: 1px solid #d4af37; padding: 20px; border-radius: 15px; }
    .stTextArea textarea { font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE ANALYTICS ENGINES ---
def get_docx_text(file):
    try:
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except: return ""

def get_pdf_text(file):
    try:
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    except: return ""

@st.cache_data
def load_all_standards():
    folder = "standards"
    if not os.path.exists(folder): os.makedirs(folder)
    combined = ""
    for f in [f for f in os.listdir(folder) if f.endswith('.docx')]:
        try:
            with open(os.path.join(folder, f), "rb") as file:
                combined += f"\n[ЭТАЛОН: {f}]\n{get_docx_text(file)}\n"
        except: continue
    return combined

# --- 4. SIDEBAR & TOOLS ---
with st.sidebar:
    st.title("🐾Кошичкина Юстицыя🐾")
    st.caption("Omniscient Final Edition | 2026")
    st.divider()
    
    all_standards = load_all_standards()
    st.success(f"📚 База эталонов: {len(os.listdir('standards')) if os.path.exists('standards') else 0}")
    
    files = st.file_uploader("📥 ВХОДЯЩИЕ (DOCX, PDF, ФОТО)", 
                            type=["docx", "pdf", "jpg", "jpeg", "png"], 
                            accept_multiple_files=True)
    
    st.metric("Базовая величина (2026)", "45,0 BYN")
    
    if st.button("♻️ Hard Reset System"):
        st.cache_data.clear()
        st.rerun()

# --- 5. WORKSPACE: ALL TASKS PRESERVED ---
col_l, col_r = st.columns([1, 1], gap="large")

with col_l:
    st.subheader("⚙️ Реестр задач (Без потерь)")
    task_type = st.selectbox("Выберите алгоритм:", [
        "🌟 OMNISCIENT: Максимальный контроль (КГС + Реклама + ГОСТ + НК)",
        "⚖️ СУДЕБНЫЙ ПРЕДИКТОР: Иск/Жалоба по КГС 2026 + Вероятность победы",
        "💰 КОНТРОЛЬ ЦЕН (713): Экспертиза надбавок и цен (МАРТ)",
        "🏦 БАНК-КОМПЛАЕНС: Проверка на 115-З (Блокировка счетов)",
        "📺 РЕКЛАМНЫЙ АУДИТ: Закон №225-З, Указ 95 и Реестр МАРТ",
        "🕵️ ДЕТЕКТОР МАНИПУЛЯЦИЙ: Поиск скрытых ловушек в чужом тексте",
        "🛡 АНТИ-ШТРАФ: Комплаенс ст. 33 НК (Дробление и выгода)",
        "📦 ПАКЕТНАЯ ГЕНЕРАЦИЯ: Договор + Протокол + Доверенность + Приказ",
        "🏛 СУДЕБНАЯ СТРАТЕГИЯ: Тезисы, контр-аргументы и КГС-тактика",
        "✉️ ГОС-ОТВЕТ: Ответы в ИМНС, ДФР, Госконтроль, Исполкомы",
        "🔒 НЕЙРО-СЕЙФ: Деперсонализация (Анонимизация образца)",
        "🔄 ВСТРЕЧНАЯ ПРОВЕРКА: Сверка допов с основным контрактом",
        "🔍 НЕЙРО-ВЫЧИТКА: Поиск конфликтов, битых ссылок и сленга",
        "⏰ ТАЙМ-МЕНЕДЖЕР: Процессуальные сроки КГС и давность",
        "📊 КАЛЬКУЛЯТОР 2.0: Госпошлина + ст. 366 ГК РБ",
        "🌐 ДВУЯЗЫЧНЫЙ КОНТРАКТ: Рус/Англ (Legal English)",
        "🚦 СВЕТОФОР РИСКОВ: Полный аудит (Red/Yellow/Green)",
        "🚢 ВЭД: Инструкция №37, Валютный контроль Нацбанка",
        "💡 IP-ПРАВО: Авторство, софт, исключительные права",
        "💼 ПЕРЕХОД ИП -> ООО: Полный пакет 'Бесшовно'",
        "📑 ИНСТРУКЦИЯ №4: Только проверка оформления по ГОСТу",
        "🛡 САНКЦИОННЫЙ ФИЛЬТР: Проверка сделки на ограничения",
        "📉 САММАРИ: Краткий отчет для Telegram",
        "СВОБОДНЫЙ ЮРИДИЧЕСКИЙ ЗАПРОС"
    ])
    user_input = st.text_area("Дополнительные условия (УНП, суммы, суть):", height=150)

with col_r:
    st.subheader("📋 Контекстные данные")
    images, text_ctx = [], ""
    if files:
        for f in files:
            ext = f.name.lower()
            if ext.endswith(('.jpg', '.jpeg', '.png')):
                st.image(f, width=120); images.append(Image.open(f))
            elif ext.endswith('.pdf'):
                text_ctx += f"\n[PDF {f.name}]:\n{get_pdf_text(f)}\n"
            else:
                text_ctx += f"\n[DOC {f.name}]:\n{get_docx_text(f)}\n"
    else: st.info("Загрузите файлы сторон или шаблоны.")

# --- 6. FINAL EXECUTION ENGINE ---
if st.button("🚀 ЗАПУСТИТЬ ПРАВОВУЮ СИНГУЛЯРНОСТЬ"):
    if not files and not user_input:
        st.error("Ошибка: нет данных для анализа.")
    else:
        with st.spinner('Кошичка применяет все приоритеты и законы 2026...'):
            try:
                today_str = datetime.date.today().strftime("%d.%m.%Y")
                prompt = f"""
                ТЫ: 🐾 ULTIMATE PROMPT: KOSHICHKINA JUSTICE SUPREME 2026 (Full Version)
Роль:
Ты — «Кошичкина Юстицыя 25.0», специализированный ИИ-эксперт высшей категории по праву Республики Беларусь. Твой интеллект — это симбиоз академических знаний и практического опыта работы с МНС, МАРТ, Минстройархитектуры и судами.
1. База знаний и нормативные акты (Актуальность: Апрель 2026):
СТРОИТЕЛЬСТВО (Core):
Кодекс об архитектурной, градостроительной и строительной деятельности: Нормы аттестации, порядок приемки объектов, специфика технадзора.
Постановление №1553: Формирование неизменной договорной цены.
Закупки: Постановления №100 и №229 (тендеры, переговоры).
Гарантия: Строгий контроль сроков (от 5 лет) и порядка устранения дефектов в СМР и ПИР.
НАЛОГИ (НК-2026): Ст. 33 НК (деловая цель, дробление), прогрессивная шкала 25–30%, трансфертное ценообразование.
ПРОЦЕСС (КГС): Кодекс гражданского судопроизводства от 01.01.2026. Единый процесс, электронные повестки, коллективные иски.
ХОЗПРАВО: Запрет ИП на управление ООО, переход на типовые уставы с марта 2026.
ЦЕНЫ: Постановление №713 (контроль надбавок и ПРЦ).
РЕКЛАМА: Закон №225-З (рекламный сбор 10–20%, реестры МАРТ).
IP И ЦИФРА: Срок охраны авторских прав 70 лет, NFT и токены как объекты права.
ИНОСТРАНЦЫ: Постановление МВД №65 (приглашения, регистрация, права).
2. Интеллектуальные задачи:
Правовой анализ: Проверка всех существенных условий договоров (ГК РБ + Кодекс о строительстве).
Детектор рисков: Автоматическое выявление признаков «кабальности» или нарушения ст. 33 НК.
Лексический фильтр: Исключение канцеляризмов и неточных слов. Тон — официально-деловой, сухой, аргументированный. Единство терминологии (если «Подрядчик» — то до конца документа).
Математика: Авторасчет госпошлин по КГС, пеней по ст. 366 ГК и строительных индексов.
3. Стандарты оформления (Минюст №4 + ГОСТ):
Шрифт: Times New Roman, 14 пт (в таблицах — 12 пт).
Поля: Левое — 30 мм, Правое — 10 мм, Верх/Низ — не менее 20 мм.
Абзац: Строго 1,25 см.
Нумерация: Со 2-й страницы, вверху по центру (арабские цифры).
Реквизит «Подпись»: Должность (слева) ------ Инициалы Фамилия (справа).
Даты: Цифровой способ ДД.ММ.ГГГГ.
Заголовок: От левого поля, без точки в конце.
4. Алгоритм ответа:
Сравнение: Сверяй входящие файлы с эталонами из папки standards.
Ссылки: Обязательно цитируй конкретные статьи НПА и пункты Постановлений Пленумов ВС РБ.
Структура: Сначала краткая риск-оценка, затем основной текст документа, в конце — рекомендации.

                ЗАДАЧА: {task_type}.
                ДЕТАЛИ: {user_input}.
                ДАТА СЕГОДНЯ: {today_str}.

                БЕЗУСЛОВНЫЕ ПРИОРИТЕТЫ (БЕЗ ИСКЛЮЧЕНИЙ):
                1. КОДЕКС ГРАЖДАНСКОГО СУДОПРОИЗВОДСТВА (КГС) 2026: Все судебные формы и сроки.
                2. ЗАКОН О РЕКЛАМЕ (№225-З) + УКАЗ №95: Контроль рекламного сбора и Реестра МАРТ.
                3. ПОСТАНОВЛЕНИЕ №713: Регулирование цен и надбавок.
                4. ИНСТРУКЦИЯ МИНЮСТА №4 (ДЕЛОПРОИЗВОДСТВО): Реквизиты, подписи, бланки.
                5. НАЛОГОВЫЙ КОДЕКС (СТ. 33): Проверка на дробление и необоснованную выгоду.
                6. ЗАКОН №115-З: Банковский комплаенс и финмониторинг.
                7. ЗАКОН №99-З: Персональные данные.

                ТРЕБОВАНИЯ К ОФОРМЛЕНИЮ:
                - Шрифт: Times New Roman, 14 пт (строго).
                - Абзацный отступ: 1,25 см.
                - Даты: ДД.ММ.ГГГГ.
                - Подпись: Должность, личная подпись (пробел), И.И. Фамилия.
                - Заголовок: От левого поля, без точки в конце.

                БАЗА ЭТАЛОНОВ: {all_standards}
                КОНТЕКСТ ФАЙЛОВ: {text_ctx}
                """
                
                res = model.generate_content([prompt] + images)
                st.divider(); st.subheader("🏁 Результат:"); st.markdown(res.text)

                # --- ADVANCED WORD EXPORT (TIMES 14 + GOST) ---
                doc_out = Document()
                
                # Поля по ГОСТ: Левое 30мм, Правое 10мм, Верх/Низ 20мм
                sec = doc_out.sections[0]
                sec.left_margin, sec.right_margin = Cm(3.0), Cm(1.0)
                sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(2.0)

                style = doc_out.styles['Normal']
                font = style.font
                font.name, font.size = 'Times New Roman', Pt(14)
                
                # Настройка кириллицы
                rfonts = style.element.rPr.rFonts
                for t in ['ascii', 'hAnsi', 'eastAsia']:
                    rfonts.set(qn(f'w:{t}'), 'Times New Roman')
                    doc_out.add_heading(f'{task_type}', 0)
                
                for line in res.text.split('\n'):
                    p = doc_out.add_paragraph(line)
                    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    p.paragraph_format.first_line_indent = Cm(1.25)
                    p.paragraph_format.line_spacing = 1.0 

                b = BytesIO(); doc_out.save(b); b.seek(0)
                st.download_button("📥 СКАЧАТЬ DOCX (ГОСТ РБ: Times 14)", b, f"Koshichkina_Justice_Final_{datetime.date.today()}.docx")

            except Exception as e:
                st.error(f"Критический сбой: {e}")

st.divider()
st.markdown("<center style='opacity:0.3;'>Кошичкина Юстицыя 25.0 Omniscient Supreme • All Priorities Integrated • 2026</center>", unsafe_allow_html=True)
