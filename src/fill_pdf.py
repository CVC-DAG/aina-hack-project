import os
import random
from fillpdf import fillpdfs


def fill_pdf(path_to_pdf, answers):
    fields = fillpdfs.get_form_fields(path_to_pdf)

    for answer in answers:
        if type(answer['pdf_key']) == str:
            fields[answer['pdf_key']] = answer['answer']

    new_pdf_path = os.path.join(os.path.dirname(path_to_pdf), f'filled_{random.randint(0, 100000)}.pdf')
    fillpdfs.write_fillable_pdf(path_to_pdf, new_pdf_path, fields)

    return new_pdf_path


if __name__ == '__main__':
    import json
    with open('cupons_answers.json', 'r') as f:
        answers = json.load(f)

    new_pdf_path = fill_pdf('dades/cupons.pdf', answers)
    print(new_pdf_path)