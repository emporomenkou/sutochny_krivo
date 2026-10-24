from parser_class import sutochno_parser
from logger_func import logger

# ПАРСИМ КАМЧАТСКИЙ КРАЙ, 30 - 31 ОКТЯБРЯ, 1 ВЗРОСЛЫЙ, КВАРТИРЫ И АПАРТАМЕНТЫ

def main():
    parser = sutochno_parser()
    parser.accept_cookies()
    while True:
        parser.get_links_on_the_page()
        if not parser.go_to_the_next_page():
            break
    parser.get_info()
    print(parser.info_list)
    parser.to_csv()

if __name__ == "__main__":
    main()