from parser_class import sutochno_parser
from logger_func import clean_logs

# ПАРСИМ КАМЧАТСКИЙ КРАЙ, 30 - 31 ОКТЯБРЯ, 1 ВЗРОСЛЫЙ, КВАРТИРЫ И АПАРТАМЕНТЫ

def main():
    clean_logs()

    parser = sutochno_parser()
    parser.open_page()
    parser.accept_cookies()
    while True:
        parser.get_links_on_the_page()
        if not parser.go_to_the_next_page():
            break
    parser.reinit_driver()
    parser.get_info()
    
    parser.to_csv()

if __name__ == "__main__":
    main()