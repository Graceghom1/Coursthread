from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet


class PDF_Generator:
    @staticmethod
    def generate_pdf(audit_results, file_path='rapport_audit.pdf'):
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        for result in audit_results:
            # elements.append(Paragraph(f"URL: {result['url']}", styles['Title']))
            elements.append(Spacer(1, 12))

            for task in ['Page', 'Temps de chargement', 'Présence H1', 'Poids des images (KB)',
                         'Taille des vidéos (KB)', 'Top mots (fréquence)', "Alt Tags", "Top mots (pertinence)"]:
                message = result[task]['message']
                task_text = task.replace('', ' ').capitalize()
                color = colors.green if result[task]['result'] == 'OK' else colors.red
                paragraph_text = f"{task_text}: {message}" if task != 'mots_frequents' else f"{task_text}: {result[task]['message']}"
                paragraph = Paragraph(paragraph_text, styles['Normal'])
                elements.append(paragraph)
                elements.append(Spacer(1, 12))

            elements.append(PageBreak())

        doc.build(elements)
