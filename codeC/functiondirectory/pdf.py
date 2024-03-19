from fpdf import FPDF


def get_string(titre, dic):
    espace = "                   "
    if titre == "Page":
        return str(titre + " : " + str(dic))
    else:
        return str(espace + titre + " : " + str(dic))


class PDF_Generator2:
    @staticmethod
    def generate_pdf(audit_results):
        espace = "            "
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 8)
        for r in audit_results:
            for task in ['Page', 'Temps de chargement', 'Présence H1', 'Poids des images (KB)',
                         'Taille des vidéos (KB)', 'Top mots (fréquence)', "Alt Tags", "Top mots (pertinence)"]:
                 print(str(r[task]))
                 pdf.multi_cell(0, 5, get_string(task,r[task]))
            # Line break
            pdf.ln()

        pdf.output('tuto1.pdf', 'F')
