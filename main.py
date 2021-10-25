from util import create_conn, get_data, get_list_view_data, quit_conn, calculate_pages
from settings import PATH
from list import categories, product_type_list

for i in range(0, len(categories)):
    for product_type in product_type_list[i]:
        total_pages = calculate_pages(PATH, product_type=product_type)
        for page in range(1, total_pages + 1):
            conn = create_conn(PATH, product_type=product_type, page=page)

            get_data(conn, category=categories[i], product_type=product_type)

quit_conn(conn)