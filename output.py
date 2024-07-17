from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class ApplicationSchemaConfigurationSpecification(BaseModel):
	jvmConfig: List[str]


class ApplicationSchemaConfiguration(BaseModel):
	specification: ApplicationSchemaConfigurationSpecification
	exposedPorts: List[dict]
	sharedNamespace: int


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
