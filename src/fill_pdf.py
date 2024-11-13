import os
import random
from fillpdf import fillpdfs


def fill_pdf(path_to_pdf, answers):
    fields = fillpdfs.get_form_fields(path_to_pdf)

    for answer in answers:
        print(answer)
        if type(answer['pdf_key']) == str:
            fields[answer['pdf_key']] = answer['answer']

    new_pdf_path = os.path.join(os.path.join("templates", "static"), f'filled_{random.randint(0, 100000)}.pdf')
    fillpdfs.write_fillable_pdf(path_to_pdf, new_pdf_path, fields)

    return new_pdf_path


if __name__ == '__main__':
    import json
    with open('DiH4CAT_answers.json', 'r') as f:
        answers = json.load(f)[0]

    new_pdf_path = fill_pdf('data/DIH4CAT.pdf', answers)
    print(new_pdf_path)