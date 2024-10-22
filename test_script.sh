echo 'start tests'
function run_test(){
  python manage.py test "$1"
}

path_array=$(find . -regex '.*\(test_[a-zA-Z]\w*.py\)')
for path in $path_array
do
  slash='/'
  point='.'
  prefix=$point
  suffix='.py'
  path_without_point=$(echo "$path" | sed -e "s/^$prefix//")
  path_without_first_slash=${path_without_point/$slash/}
  path_without_slash=${path_without_first_slash//$slash/$point}
  path_without_suffix=$(echo "$path_without_slash" | sed "s/$suffix//g")
  run_test $path_without_suffix
done

read -p "Press Enter to exit"