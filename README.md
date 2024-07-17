# VK-intership-task
## A small note
В задании указано, что нужно валидировать в соответствии с [json-schema](https://json-schema.org),
но в примере указан yaml файл с другими полями. Эта утилита работает с файлами, которые были
в примере задания. Названия полей совпадают, но файл типа json. [Далее](#generating-pydantic-schema-from-json) это будет наглядно показано
## Feautures
- Pydantic schema generating from JSON
- CRUD generating from pydantic schema

## Generating Pydantic schema from JSON
### Sample JSON
```json
{
  "kind": "application",
  "name": "hello-world",
  "version": "v0.1.0",
  "description": "My application",
  "configuration": {
    "specification": {
      "jvmConfig": [
        "-Dcom.sun.a=a",
        "-Dcom.sun.b=b",
        "-Dcom.sun.c=c"
      ]
    },
    "exposedPorts": [
      {
        "name": "my-port",
        "port": 8000,
        "protocol": "TCP"
      }
    ],
    "sharedNamespace": true
  },
  "log": {
    "level": "INFO"
  },
  "environmentVariables": [
    "VAR1=VALUE1",
    "VAR2=VALUE2"
  ],
  "settings": {
    "settingAaa": {},
    "settingAab": {}
  }
}
```

### Sample pydantic output
```python
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class ApplicationSchemaConfigurationSpecification(BaseModel):
	jvmConfig: List[str]


class ApplicationSchemaConfigurationExposedports(BaseModel):
	name: str
	port: int
	protocol: str


class ApplicationSchemaConfiguration(BaseModel):
	specification: ApplicationSchemaConfigurationSpecification
	exposedPorts: List[ApplicationSchemaConfigurationExposedports]
	sharedNamespace: bool


class ApplicationSchemaLog(BaseModel):
	level: str


class ApplicationSchemaSettingsSettingaaa(BaseModel):
	...


class ApplicationSchemaSettingsSettingaab(BaseModel):
	...


class ApplicationSchemaSettings(BaseModel):
	settingAaa: ApplicationSchemaSettingsSettingaaa
	settingAab: ApplicationSchemaSettingsSettingaab


class ApplicationSchema(BaseModel):
	kind: str
	name: str
	version: str
	description: str
	configuration: ApplicationSchemaConfiguration
	log: ApplicationSchemaLog
	environmentVariables: List[str]
	settings: ApplicationSchemaSettings

```

### Command line
```shell
python gen-model.py path/to/your/json/sample.json path/to/your/output/output.py
```