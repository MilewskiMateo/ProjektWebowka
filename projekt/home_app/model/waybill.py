import uuid
from fpdf import FPDF


class Waybill:

    def __init__(self, sender, recipient):
        self.__sender = sender
        self.__recipient = recipient

    def generate_and_save(self, filename, photo_path=False):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        self.__add_table_to_pdf(pdf)

        if not photo_path == False:
            pdf.image(photo_path, w = 100, h = 100 ,y=80, x= 50)
        pdf.output(filename)


    def __add_table_to_pdf(self, pdf):
        n_cols = 2
        col_width = (pdf.w - pdf.l_margin - pdf.r_margin) / n_cols / 2
        font_size = pdf.font_size
        n_lines = 6

        pdf.cell(col_width, n_lines * font_size, "Sender", border=1)
        pdf.multi_cell(col_width, font_size, txt=self.__sender.str_full(), border=1)
        pdf.ln(0)
        pdf.cell(col_width, n_lines * font_size, "Recipient", border=1)
        pdf.multi_cell(col_width, font_size, txt=self.__recipient.str_full(), border=1)



class Person:

    def __init__(self, name: str, surname: str, telephone: str, address):
        self.__name = name
        self.__surname = surname
        self.__telephone = telephone
        self.__address = address

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_telephone(self):
        return self.__telephone

    def get_fullname(self):
        return "{} {}".format(self.__name, self.__surname)

    def get_address(self):
        return self.__address

    def str_full(self):
        return "{}\n{}\n{}".format(self.get_fullname(),self.get_telephone(), self.__address.str_full())


class Address:

    def __init__(self, street: str, nr:str, postal_code: str, country: str):
        self.__street = street +" " + nr
        self.__postal_code = postal_code
        self.__country = country

    def get_street(self):
        return self.__street
        
    def get_postal_code(self):
        return self.__postal_code
    
    def get_country(self):
        return self.__country

    def str_full(self):
        result = ""
        for field_value in self.__dict__.values():
            result += "\n{}".format(field_value)

        return result