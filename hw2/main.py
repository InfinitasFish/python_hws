import sys
#sys.path.append('C:\\my_pp_\\latex_venv\\Lib\\site-packages')
from tiniest_latex_lib import generate_latex_pdf


if __name__ == '__main__':
    incomplete_matrix = [[1,2,3,4,5], [1,2,3,4], [1,2,3], [1,2], [1]]
    image_path = 'image.png'
    # generate_latex_from_matrix(incomplete_matrix)
    # generate_latex_from_image(image_path)
    generate_latex_pdf(incomplete_matrix, image_path)
