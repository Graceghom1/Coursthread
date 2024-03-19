from fpdf import FPDF


pdf = FPDF()
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font('Times', '', 8)
for i in range(1, 41):
    pdf.multi_cell(0, 10, 'Printing line number ' + str(i), 0, 1)
pdf.output('tuto2.pdf', 'F')
