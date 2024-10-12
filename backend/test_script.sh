echo 'start tests'
function run_test(){
  python manage.py test "$1"
}
path_array=(
  tasks.tests.test_logic #логика
  users.tests.test_logic
  tasks.tests.test_serializers #сериализаторы
  users.tests.test_serializers
  users.tests.test_api.test_anonimus_user #тесты апи анонимов
  tasks.tests.tests_api.test_anonimus
  tasks.tests.tests_api.test_customer #тесты апи пользователей заказчик
  users.tests.test_api.test_simple_user
  tasks.tests.tests_api.test_worker #тесты апи пользователей работник
  users.tests.test_api.test_super_customer #тесты апи пользователей заказчик с привелегиями
  users.tests.test_api.test_super_worker #тесты апи пользователей работник с привелегиями
  tasks.tests.tests_api.test_super_worker
)
for path in ${path_array[*]}
do
    run_test "$path"
done
read -p "Press Enter to exit"
