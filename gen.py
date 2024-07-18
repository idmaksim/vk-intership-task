import os
import sys
import json

from gen_crud import gen_crud
from gen_schema import generate_pydantic_model_from_json, write_model_to_file
from gen_db import gen_db
from gen_abstract_repo import gen_abstract_repo
from gen_service import gen_service


def main(json_data_path: str, output_file_path: str, action: str):
    with open(json_data_path, 'r') as file:
        data = json.load(file)

    if "kind" not in data:
        raise ValueError("JSON data must contain a 'kind' field.")
    kind = data['kind']
    output_dir_path = '/'.join(output_file_path.split('/')[:-1]) 
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    match action:
        case 'model':
            model = generate_pydantic_model_from_json(data, class_name=kind)
            write_model_to_file(model, output_file_path)
            print(f"Pydantic model has been written to {output_file_path}")
        case 'crud':
            gen_db(output_dir_path, kind)
            gen_abstract_repo(output_dir_path)
            gen_service(output_dir_path, kind)
            gen_crud(data, output_file_path)

        case _:
            print('Choose the right action: model, crud')



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage for schemas: python gen.py model <json_data_path> <output_file_path>")
        print("Usage for CRUD: python gen.py model <json_data_path> <output_file_path>")
    else:
        action = sys.argv[1]
        json_data_path = sys.argv[2]
        output_file_path = sys.argv[3]
        main(json_data_path, output_file_path, action)
