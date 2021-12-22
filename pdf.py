from fpdf import FPDF


class PDF(FPDF):
    title = "Total Teams and Groups"

    def header(self):
        self.set_font(family='helvetica', style='B', size=24)
        # Calculate width of title and position
        title_width = self.get_string_width(PDF.title) + 6
        self.set_x((self.w - title_width) / 2)
        # Colors of text
        self.set_text_color(30,144,255) # dodgerblue
        # Title
        self.cell(title_width, 10, PDF.title, 0, 1, 'C')
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('helvetica', 'B', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def page_setup(self):
        self.add_page(orientation='P', format='A4', same=False)

    def teams(self, lst: list):

        self.set_font(family='helvetica', style='B', size=20)
        self.set_text_color(0,191,255) # deepskyblue
        self.cell(w=0, h=10, txt="Teams", border=0, ln=1)
        # for teams
        self.set_font(family='helvetica', style='', size=16)
        self.set_text_color(176,224,230)  # powderblue
        for l in lst:
            self.cell(w=0, h=10, txt=l, border=0, ln=1)

    def groups(self, dic: dict):
        self.set_font(family='helvetica', style='B', size=20)
        self.set_text_color(0, 191, 255)  # deepskyblue
        self.set_auto_page_break(auto=True, margin=15)
        self.cell(w=0, h=10, txt="Groups", border=0, ln=1)
        for k, v in dic.items():
            self.ln(4)
            # for group names
            self.set_font(family='helvetica', style='', size=16)
            self.set_text_color(135, 206, 250)  # lightskyblue
            self.cell(w=0, h=10, txt=k, border=0, ln=1)
            # for teams
            self.set_font(family='helvetica', style='', size=16)
            self.set_text_color(176, 224, 230)  # powderblue
            for t in v:
                self.cell(w=0, h=10, txt=t, border=0, ln=1)
