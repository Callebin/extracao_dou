from fpdf import FPDF


class Gerador(FPDF):
    def __init__(self):
        super().__init__()
        self.page_width = 210
        self.page_height = 297
        self.set_margins(25, 10, 25)
        self.set_auto_page_break(True, margin=10)
        self.add_page()
        self.set_font("Arial", "B", 16)
        self.set_fill_color(26, 4, 136)
        self.cell(0, 10, "Extração Diária DOU - CGU", 0, 1, "C")
        self.ln()
        self.set_font("Arial", "", 12)

    def add_port(self, portaria, org, destaque, link):
        # Calculate the height of the data text
        data_height = self.font_size * 20

        # If the data would extend past the bottom of the page, start a new page
        if self.get_y() + data_height > self.page_height - self.b_margin:
            self.add_page()

        # Write the port number, organizations, and data to the PDF
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", "B", 11)
        self.multi_cell(
            self.page_width - self.r_margin - self.l_margin,
            7,
            f"{portaria}",
            0,
            align="C",
        )

        self.set_text_color(105, 105, 105)
        self.set_font("Arial", "B", 10)
        self.multi_cell(
            self.page_width - self.r_margin - self.l_margin, 7, f"{org}", 0, align="C"
        )

        self.set_xy(self.l_margin, self.get_y())
        self.set_font("Arial", "", 9)
        self.multi_cell(
            self.page_width - self.r_margin - self.l_margin,
            7,
            f"{destaque}",
            0,
            align="C",
        )

        self.set_text_color(70, 130, 180)
        self.set_font("Arial", "B", 8)
        self.multi_cell(
            self.page_width - self.r_margin - self.l_margin, 7, f"{link}", 0, align="C"
        )

        self.ln()
