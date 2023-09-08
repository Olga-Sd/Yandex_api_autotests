import sender_stand_request
import data

def get_user_body(first_name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.user_body.copy()
    # изменение значения в поле firstName
    current_body["firstName"] = first_name
    # возвращается новый словарь с нужным значением firstName
    return current_body
def positive_assert(Name):
    user_body = get_user_body(Name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""
    users_table_response = sender_stand_request.get_users_table()
    # Строка, которая должна быть в ответе запроса на получение данных из таблицы users
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть, и он единственный
    assert users_table_response.text.count(str_user) == 1

def negative_assert(name):
    user_body = get_user_body(name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] =="Имя пользователя введено некорректно. Имя может содержать \
только русские или латинские буквы, длина должна быть не менее 2 и не более 15 символов"

def negative_assert_no_name(body):
    user_body = body
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == "Не все необходимые параметры были переданы"

def negative_assert_wrong_data(name):
    user_body = get_user_body(name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400

def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Аа")

def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("АААААбббббввввв")

def test_create_user_1_letter_in_first_name_get_negative_response():
    negative_assert("А")

def test_create_user_16_letter_in_first_name_get_negative_response():
    negative_assert("Ааааабббббсссссд")

def test_create_user_englisn_letter_in_first_name_get_success_response():
    positive_assert("Maria")

def test_create_user_russian_letters_in_first_name_get_success_response():
    positive_assert("Мария")

def test_create_user_is_space_in_first_name_get_negative_response():
    negative_assert("Человек и Ко")

def test_create_user_special_simbols_in_first_name_get_negative_response():
    negative_assert("\"@$%")

def test_create_user_number_in_first_name_get_negative_response():
    negative_assert("Маша5")

def test_create_user_no_first_name_get_negative_response():
    body_no_name = {
    "phone": "+79995553322",
    "address": "г. Москва, ул. Пушкина, д. 10"
}
    negative_assert_no_name(body_no_name)

def test_create_user_empty_first_name_get_negative_response():
    body_empty_name = get_user_body("")
    negative_assert_no_name(body_empty_name)

def test_create_user_wrong_data_type_first_name_get_negative_response():
    negative_assert_wrong_data(12)
