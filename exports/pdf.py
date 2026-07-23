from datetime import datetime
from components import fmt
from constants import ECG_ACHADOS


def gerar_pdf(df, ind):
    try:
        from fpdf import FPDF

        class PDF(FPDF):
            def header(self):
                self.set_font("Helvetica", "B", 14)
                self.cell(0, 10, "Relatorio Cardiovascular - UFVJM", 0, 1, "C")
                self.set_font("Helvetica", "", 8)
                self.cell(0, 5, f"Gerado em {datetime.now():%d/%m/%Y %H:%M}", 0, 1, "C")
                self.ln(4)

            def footer(self):
                self.set_y(-15)
                self.set_font("Helvetica", "I", 7)
                self.cell(0, 10, "PIBIC/UFVJM - Saude Digital Movel - LGPD", 0, 0, "C")

            def section(self, title):
                self.set_font("Helvetica", "B", 11)
                self.set_fill_color(30, 30, 30)
                self.set_text_color(226, 75, 74)
                self.cell(0, 8, f"  {title}", 0, 1, "L", fill=True)
                self.set_text_color(50, 50, 50)
                self.ln(2)

            def kv(self, label, value):
                self.set_font("Helvetica", "", 9)
                self.cell(70, 6, f"{label}:", 0, 0)
                self.set_font("Helvetica", "B", 9)
                self.cell(0, 6, str(value), 0, 1)

        pdf = PDF()
        pdf.add_page()
        pdf.section("Resumo Executivo")
        for k, v in [("Total", fmt(ind["n"])), ("Municipios", ind["n_muns"]),
                      ("Idade media", ind["avg_age"]), ("Arritmias", ind["n_arr"]),
                      ("Bloqueios", ind["n_blk"]), ("Alterados", f"{ind['alt_pct']}%")]:
            pdf.kv(k, v)
        pdf.ln(4)
        for cat in ECG_ACHADOS:
            df_a = ind["achados"].get(cat)
            if df_a is not None and not df_a.empty:
                pdf.section(cat)
                for _, r in df_a.iterrows():
                    pdf.kv(r["Achado"], f"{r['Casos']} ({r['%']}%)")
                pdf.ln(3)
        pdf.section("Comorbidades")
        for _, label, total, pct in ind["comorb_resumo"]:
            pdf.kv(label, f"{total} ({pct}%)")
        raw = pdf.output(dest="S")
        return bytes(raw) if isinstance(raw, (bytes, bytearray)) else raw.encode("latin-1")
    except ImportError:
        return None