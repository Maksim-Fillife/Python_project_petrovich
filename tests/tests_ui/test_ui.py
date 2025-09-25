


def test_login_success(main_page, login_page):
    main_page.open()
    main_page.open_login_modal()
    login_page.fill_email()
    login_page.fill_password()
    login_page.submit_authorization()
    login_page.check_successful_auth()


def test_search_product_by_keyword(main_page, product_page):
    main_page.open()
    main_page.search_product("перфоратор")
    main_page.get_product_cards()
    product_name = main_page.select_random_product()
    product_title = product_page.get_product_title()
    assert product_name.lower() in product_title.lower(), \
        f"Название товара не совпадает: ожидалось '{product_name}', получено '{product_title}'"




































