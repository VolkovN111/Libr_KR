from fpdf import FPDF

class PDFFile(FPDF): 
            
    def create_pdf(self):
        self.add_page()
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 14)
        
    def write_pdf(self, text: str):
        self.write(h=12, txt=text)
        
    def output_pdf(self):
        self.output('book_list.pdf')