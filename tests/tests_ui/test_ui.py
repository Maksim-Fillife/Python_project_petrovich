from allure_commons.types import Severity
import allure
import pytest


@allure.tag('Web')
@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.story('Авторизация')
@allure.feature('Успешный вход пользователя')
@allure.title('Успешная авторизация пользователя с корректными данными')
@pytest.mark.ui
def test_login_success(main_page, login_page):
    main_page.open()
    main_page.open_login_modal()
    login_page.fill_email()
    login_page.fill_password()
    login_page.submit_authorization()
    assert login_page.is_profile_popup_displayed(), "Профиль не отобразился"


@allure.tag('Web')
@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.story('Авторизация')
@allure.feature('Вход с неверным паролем')
@allure.title('Попытка входа с некорректным паролем')
@pytest.mark.ui
def test_login_with_wrong_password(main_page, login_page):
    main_page.open()
    main_page.open_login_modal()
    login_page.fill_email()
    login_page.fill_invalid_password()
    login_page.submit_authorization()
    with allure.step("Проверить сообщение об ошибке при неверном пароле"):
        error_message = login_page.get_error_password_message()
        assert error_message ==  "Неверный пароль", \
            f"Ожидалось 'Неверный пароль', получено: '{error_message}'"



@allure.tag('Web')
@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.story('Авторизация')
@allure.feature('Выход из аккаунта')
@allure.title('Выход пользователя из аккаунта')
@pytest.mark.ui
def test_logout(main_page, login_page):
    main_page.open()
    main_page.open_login_modal()
    login_page.fill_email()
    login_page.fill_password()
    login_page.submit_authorization()
    login_page.open_profile_popup()
    login_page.click_logout()
    with allure.step("Проверить отображение элемента авторизации после выхода из аккаунта"):
        login_prompt = login_page.get_login_prompt_text()
        assert login_prompt == "Войдите, чтобы продолжить", \
            f"Ожидалось 'Войдите, чтобы продолжить', получено: '{login_prompt}'"


@allure.tag('Web')
@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.story('Поиск товаров')
@allure.feature('Поиск по ключевому слову')
@allure.title('Поиск товара по ключевому слову {keyword}')
@pytest.mark.ui
def test_search_product_by_keyword(main_page, product_page):
    main_page.open()
    keyword='перфоратор'
    main_page.search_product(keyword)
    with allure.step(f"Проверить, что результат поиска содержит ключевое слово '{keyword}'"):
        search_result = main_page.get_search_result_text(keyword)
        assert keyword.lower() in search_result.lower(), \
            f"Ожидаемый ключ '{keyword}' не найден в результате: '{search_result}'"


@allure.tag('Web')
@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.story('Каталог товаров')
@allure.feature('Открытие карточки товара')
@allure.title('Открытие случайной карточки товара и проверка названия')
@pytest.mark.ui
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
@allure.story('Избранное')
@allure.feature('Добавление товара в избранное')
@allure.title('Добавление товара в список избранного')
@pytest.mark.ui
def test_add_product_to_favorites(main_page, product_page):
    main_page.open()
    main_page.search_product('Водоснабжение')
    main_page.select_random_product()
    main_page.get_title_cards()
    product_page.add_to_favourite()
    with allure.step("Проверить, что появилось сообщение 'Добавлено в избранное'"):
        message = product_page.get_favorite_added_message()
        assert message == 'Добавлено в избранное'


@allure.tag('Web')
@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.story('Корзина')
@allure.feature('Добавление товара в корзину')
@allure.title('Добавление товара в корзину покупок')
@pytest.mark.ui
def test_add_product_to_cart(main_page, product_page):
    main_page.open()
    main_page.search_product('розетка')
    main_page.select_random_product()
    product_page.add_to_cart()
    with allure.step("Проверить, что кнопка изменила текст на 'В корзине'"):
        button_text = product_page.get_add_to_cart_button_text()
        assert button_text == "В корзине", \
            f"Ожидался текст кнопки 'В корзине', получено: '{button_text}'"


@allure.tag('Web')
@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.story('Корзина')
@allure.feature('Удаление товара из корзины')
@allure.title('Удаления товара из корзины и очистка содержимого')
@pytest.mark.ui
def test_delete_product_from_cart(main_page, product_page, cart_page):
    main_page.open()
    main_page.search_product('крепеж')
    main_page.select_random_product()
    product_page.add_to_cart()
    main_page.open_cart()
    cart_page.delete_product_from_cart()
    with allure.step("Проверить, что появилось сообщение 'Корзина пуста'"):
        assert cart_page.is_cart_empty(), "Сообщение 'Корзина пуста.' не отобразилось"


@allure.tag('Web')
@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Maksim-Fillife')
@allure.story('Сервисы')
@allure.feature('Открытие страницы доставки')
@allure.title('Переход на страницу "Доставка и подъём"')
@pytest.mark.ui
def test_open_delivery_page(main_page,services_page, delivery_page):
    main_page.open()
    main_page.open_services()
    services_page.open_delivery_page()
    with allure.step("Проверить, что заголовок страницы содержит 'Доставка и подъем'"):
        title_text = delivery_page.get_delivery_page_title()
        assert "Доставка и подъем" in title_text, \
            f"Ожидалось, что заголовок содержит 'Доставка и подъем', но получено: '{title_text}'"


@allure.tag('Web')
@allure.severity(Severity.MINOR)
@allure.label('owner', 'Maksim-Fillife')
@allure.story('Навигация по сайту')
@allure.feature('Проверка разделов футера')
@allure.title('Проверка наличия разделов в футере сайта')
@pytest.mark.ui
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




































