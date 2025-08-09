import random
import re
from flask import Flask, render_template, jsonify
from PyPDF2 import PdfReader

ARABIC_DIACRITICS = re.compile(r'[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]')

def normalize(text: str) -> str:
    """Convert common Allah ligature and strip diacritics for robust matching."""
    text = text.replace('\ufdf2', 'الله')  # Allah ligature
    return ARABIC_DIACRITICS.sub('', text)

app = Flask(__name__)

LETTER_MEANINGS = {
    'ا': 'iyidir',
    'ب': 'iyidir',
    'ت': 'iyidir',
    'ث': 'iyidir',
    'ج': 'iyidir',
    'ح': 'iyidir',
    'خ': 'istiğfar edip niyeti üzerine sabr etmek gerektir',
    'د': "pek iyi değilse de, sonunda Allah'ın yardımı ile muradı hasıl olurdur",
    'ذ': 'celal, kerem ve azamet sahibi olur',
    'ر': 'iyidir',
    'ز': 'iyidir',
    'س': 'iyidir',
    'ش': 'iyi değildir, bir çok korkulu şeylerle karşılaşmaktır, sabr edilirse, iyi olabilir',
    'ص': 'iyidir fakat seferden sakınmalıdır',
    'ض': 'iyidir',
    'ط': 'iyidir',
    'ظ': 'iyidir',
    'ع': 'niyetinden sakınmak tevbe ve istiğfar etmek gerekir',
    'غ': 'iyidir',
    'ف': 'iyidir',
    'ق': 'iyidir',
    'ك': 'istiğfar ve tevbe etmek,günahlardan son derece sakınmak, helal maldan sadaka vermek gerekir',
    'ل': 'iyidir',
    'م': 'iyidir',
    'ن': 'tevbe ve istiğfar ederek beklemek gerekir',
    'و': 'iyidir',
    'ه': 'iyidir',
    'لا': 'zahmet ve meşakkat çekmektir, sonu hayır olabilir',
    'ي': 'iyidir'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/istihare')
def istihare():
    reader = PdfReader('kuran.pdf')
    num_pages = len(reader.pages)
    right_index = random.randrange(1, num_pages, 2)
    text = reader.pages[right_index].extract_text() or ""
    norm_text = normalize(text)
    count = norm_text.count("الله")
    target_index = max(0, right_index - count)
    target_text = reader.pages[target_index].extract_text() or ""
    lines = [normalize(line.strip()) for line in target_text.splitlines() if line.strip()]
    if count > 0 and lines:
        line_idx = min(count - 1, len(lines) - 1)
    else:
        line_idx = 0
    line_text = lines[line_idx] if lines else ""
    letter = line_text[-2:] if line_text.endswith('لا') else line_text[-1:]
    meaning = LETTER_MEANINGS.get(letter, 'Belirsiz')
    return jsonify({
        'right_page': right_index + 1,
        'count': count,
        'target_page': target_index + 1,
        'line_number': line_idx + 1,
        'letter': letter,
        'meaning': meaning
    })

if __name__ == '__main__':
    app.run(debug=True)
