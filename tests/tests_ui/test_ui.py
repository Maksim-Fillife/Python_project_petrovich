from allure_commons.types import Severity
import allure


@allure.tag('Web')
@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.feature('Successful user login')
@allure.story('Authentication')
def test_login_success(main_page, login_page):
    main_page.open()
    main_page.open_login_modal()
    login_page.fill_email()
    login_page.fill_password()
    login_page.submit_authorization()
    login_page.check_successful_auth()


@allure.tag('Web')
@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.feature('Login with invalid password')
@allure.story('Authentication')
def test_login_with_wrong_password(main_page, login_page):
    main_page.open()
    main_page.open_login_modal()
    login_page.fill_email()
    login_page.fill_invalid_password()
    login_page.submit_authorization()
    login_page.check_unsuccessful_auth()


@allure.tag('Web')
@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.feature('User logout')
@allure.story('Authentication')
def test_logout(main_page, login_page):
    main_page.open()
    main_page.open_login_modal()
    login_page.fill_email()
    login_page.fill_password()
    login_page.submit_authorization()
    login_page.open_profile_popup()
    login_page.click_logout()
    login_page.check_logout()


@allure.tag('Web')
@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.feature('Search product by keyword')
@allure.story('Product Search')
def test_search_product_by_keyword(main_page, product_page):
    main_page.open()
    keyword='перфоратор'
    main_page.search_product(keyword)
    main_page.check_product_exist(keyword)


@allure.tag('Web')
@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.feature('Open product detail page')
@allure.story('Product Catalog')
def test_open_product_card(main_page, product_page):
    main_page.open()
    main_page.search_product('краска')
    main_page.select_random_product()
    main_page.get_title_cards()
    product_name = main_page.select_random_product()
    product_title = product_page.get_product_title()
    assert product_name.lower() in product_title.lower(), \
        f"Название товара не совпадает: ожидалось '{product_name}', получено '{product_title}'"


@allure.tag('Web')
@allure.severity(Severity.MINOR)
@allure.label('owner', 'Maksim-Fillife')
@allure.feature('Add product to favorites')
@allure.story('Wishlist')
def test_add_product_to_favorites(main_page, product_page):
    main_page.open()
    main_page.search_product('Водоснабжение')
    main_page.select_random_product()
    main_page.get_title_cards()
    product_page.add_to_favourite()
    product_page.check_added_to_favorite()


@allure.tag('Web')
@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.feature('Add product to cart')
@allure.story('Shopping Cart')
def test_add_product_to_cart(main_page, product_page):
    main_page.open()
    main_page.search_product('розетка')
    main_page.select_random_product()
    product_page.add_to_cart()
    product_page.check_added_to_cart()


@allure.tag('Web')
@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.feature('Remove product from cart')
@allure.story('Shopping Cart')
def test_delete_product_from_cart(main_page, product_page, cart_page):
    main_page.open()
    main_page.search_product('крепеж')
    main_page.select_random_product()
    product_page.add_to_cart()
    main_page.open_cart()
    cart_page.delete_product_from_cart()
    cart_page.is_cart_empty()


@allure.tag('Web')
@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.feature('Open Delivery page')
@allure.story('Services')
def test_open_delivery_page(main_page,services_page, delivery_page):
    main_page.open()
    main_page.open_services()
    services_page.open_delivery_page()
    delivery_page.check_delivery_page_title()


@allure.tag('Web')
@allure.severity(Severity.MINOR)
@allure.label('owner', 'Maksim-Fillife')
@allure.feature('Verify footer section titles')
@allure.story('Site Navigation')
def test_footer_contains_company_info(main_page):
    expected = {
        "О компании",
        "Покупателям",
        "Сервисы",
        "Лояльность",
        "Контакты",
        "Обратная связь"
    }

    main_page.open()
    actual = main_page.get_footer_section_titles()

    assert expected == actual, (
        f"Ожидались разделы: {expected}\n"
        f"Фактические разделы: {actual}\n"
        f"Разница: {expected.symmetric_difference(actual)}"
    )




































