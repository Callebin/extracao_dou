from fpdf import FPDF

class Gerador(FPDF):
    def __init__(self):
        super().__init__()
        self.page_width = 210
        self.page_height = 297
        self.set_margins(25, 10, 25)
        self.set_auto_page_break(True, margin=10)
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Extração Diária DOU - CGU', 0, 1, 'C')
        self.ln()
        self.set_font('Arial', '', 12)
        
    def add_port(self, port_num, orgs, data_text):
        # Calculate the height of the data text
        data_height = self.font_size * len(data_text.split('\n')) + 4
        
        # If the data would extend past the bottom of the page, start a new page
        if self.get_y() + data_height > self.page_height - self.b_margin:
            self.add_page()
            
        # Write the port number, organizations, and data to the PDF
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f'{port_num}', 0, 1, align='C')
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f'{orgs}', 0, 1, align='C')
        self.set_xy(self.l_margin, self.get_y())
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, f'{data_text}', 0, align='C')
        self.ln()
pdf = Gerador()
data = [
    ('PORTARIA 1', 'ORG 1', 'ESCOPO 1 PARAPAPAPAPA'),
    ('PORTARIA 2', 'ORG 2', 'ESCOPO 2 PARAPAPAPAPATIBUMTBUMTIBUM'),
    ('PORTARIA 3', 'ORG 3', 'ESCOPO 3 PARAPAPAPAPAT IBUMTBUMTIBUML OASDAS DADASDASDASDA SDADSDASIOLLALAALLALAA')
]
for port_num, orgs, data_text in data:
    pdf.add_port(port_num, orgs, data_text)
pdf.output('v5.pdf', 'F')
