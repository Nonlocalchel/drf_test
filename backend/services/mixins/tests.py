import json


class ManipulateExpectedDataMixin:
    expected_data_path = ''

    def get_expected_data(self) -> list:
        path = self.expected_data_path
        with open(path) as expected_data_file:
            expected_data = json.loads(expected_data_file.read())
            return expected_data

    def write_data_to_json_file(self, new_data) -> None:
        path = self.expected_data_path
        with open(path, 'w') as expected_data_file:
            expected_data_file.write(json.dumps(new_data))


