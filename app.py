from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from pathlib import Path

app = Flask(__name__)

current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
EXCEL_FILE = current_dir / 'allinone.xlsx'

# Load or create DataFrame
if EXCEL_FILE.exists():
    df = pd.read_excel(EXCEL_FILE)
else:
    df = pd.DataFrame(columns=['tarih', 'baslangickm', 'mazot', 'katedilenyol', 'toplamyol', 'toplammazot', 'ortalama100', 'kumulatif100'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tarih = request.form['tarih']
        baslangickm = int(request.form['baslangickm'])
        mazot = int(request.form['mazot'])

        # Calculate values
        toplammazot = df['mazot'].sum() + mazot
        katedilenyol = baslangickm - df.iloc[-1]['baslangickm'] if not df.empty else 0
        toplam_yol = df['katedilenyol'].sum() + katedilenyol
        
        ortalama100 = (100 / katedilenyol) * mazot if katedilenyol > 0 else 0
        kumulatif100 = (100 / toplam_yol) * mazot if toplam_yol > 0 else 0

        new_record = {
            'tarih': tarih,
            'baslangickm': baslangickm,
            'mazot': mazot,
            'katedilenyol': katedilenyol,
            'toplamyol': toplam_yol,
            'toplammazot': toplammazot,
            'ortalama100': ortalama100,
            'kumulatif100': kumulatif100
        }

        df.loc[len(df)] = new_record
        df.to_excel(EXCEL_FILE, index=False)

        return redirect(url_for('index'))

    return render_template('index.html', data=df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
