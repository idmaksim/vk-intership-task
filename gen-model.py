import sys
import json
from typing import Any, Dict

def generate_pydantic_model_from_json(data: Dict[str, Any], class_name: str) -> str:
    class_definitions = []

    def parse_dict(name: str, dictionary: Dict[str, Any]) -> str:
        fields = []
        nested_models = []

        def get_type(value):
            if isinstance(value, str):
                return "str"
            elif isinstance(value, bool):
                return "bool"
            elif isinstance(value, int):
                return "int"
            elif isinstance(value, float):
                return "float"
            elif isinstance(value, dict):
                nested_class_name = f"{name}{key.capitalize()}"
                nested_model = parse_dict(nested_class_name, value)
                nested_models.append(nested_model)
                return nested_class_name
            elif isinstance(value, list):
                if value:
                    first_item_type = get_type(value[0])
                    return f"List[{first_item_type}]"
                else:
                    return "List[Any]"
            else:
                return "Any"

        for key, value in dictionary.items():
            field_type = get_type(value)
            fields.append(f'{key}: {field_type}')

        if fields:
            fields_str = "\n\t".join(fields)
        else:
            fields_str = '...'

        class_definition = f"class {name}(BaseModel):\n\t{fields_str}\n"
        class_definitions.append(class_definition)

        return name

    kind_name = data['kind'].capitalize()
    class_name = f"{kind_name}Schema"

    parse_dict(class_name, data)

    return "\n\n".join(class_definitions)

def write_model_to_file(model: str, file_path: str):
    with open(file_path, 'w') as file:
        file.write("from pydantic import BaseModel\n")
        file.write("from typing import Any, Dict, List, Optional\n\n")
        file.write(model)

def main(json_data_path: str, output_file_path: str):
    with open(json_data_path, 'r') as file:
        data = json.load(file)

    if "kind" not in data:
        raise ValueError("JSON data must contain a 'kind' field.")

    model = generate_pydantic_model_from_json(data, class_name=data['kind'])
    write_model_to_file(model, output_file_path)
    print(f"Pydantic model has been written to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python gen-model.py <json_data_path> <output_file_path>")
    else:
        json_data_path = sys.argv[1]
        output_file_path = sys.argv[2]
        main(json_data_path, output_file_path)
