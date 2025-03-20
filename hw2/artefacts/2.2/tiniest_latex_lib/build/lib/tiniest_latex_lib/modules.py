import subprocess


def generate_latex_from_matrix(matrix, fname='table'):
    """Generating the most basic .tex with table structure"""

    max_w = max([len(r) for r in matrix])
    with open(fname+'.tex', 'w') as tf:

        cols = '|' + 'c|' * max_w
        tf.write('\\begin{tabular}{ ' + cols + ' }\n')
        tf.write('\\hline\n')

        for r in matrix:
            for i in range(max_w - len(r)):
                r.append(' ')
            tf.write(' & '.join(map(str, r)) + ' \\\\ \n')

        tf.write('\\hline\n')
        tf.write('\\end{tabular}')

    return fname


def generate_latex_from_image(impath, fname='image'):
    """Generating the most basic .tex with image"""

    with open(fname+'.tex', 'w') as tf:
        tf.write('\\begin{figure}\n')
        tf.write(f'\\includegraphics[width=8cm]{{ {impath} }}')
        tf.write('\\end{figure}\n')

    return fname


def generate_latex_pdf(matrix, impath, pdf_fname='out'):
    with open(pdf_fname+'.tex', 'w') as full_file:
        full_file.write('\\documentclass{article}\n')
        full_file.write('\\usepackage{graphicx}\n')
        full_file.write('\\begin{document}\n')

        tablef = generate_latex_from_matrix(matrix)
        with open(tablef+'.tex', 'r') as tf:
            full_file.write(tf.read()+'\n')

        imagef = generate_latex_from_image(impath)
        with open(imagef+'.tex', 'r') as tf:
            full_file.write(tf.read() + '\n')

        full_file.write('\\end{document}\n')

    subprocess.run(['pdflatex', pdf_fname+'.tex'])

    return pdf_fname+'.pdf'
