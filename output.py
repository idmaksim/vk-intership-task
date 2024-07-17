from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class ApplicationSchemaConfigurationSpecification(BaseModel):
	jvmConfig: Optional[List[str]]


class ApplicationSchemaConfiguration(BaseModel):
	specification: Optional[ApplicationSchemaConfigurationSpecification]
	exposedPorts: Optional[List[dict]]
	sharedNamespace: Optional[int]


class ApplicationSchemaLog(BaseModel):
	level: Optional[str]


class ApplicationSchemaSettingsSettingaaa(BaseModel):
	...


class ApplicationSchemaSettingsSettingaab(BaseModel):
	...


class ApplicationSchemaSettings(BaseModel):
	settingAaa: Optional[ApplicationSchemaSettingsSettingaaa]
	settingAab: Optional[ApplicationSchemaSettingsSettingaab]


class ApplicationSchema(BaseModel):
	kind: str
	name: str
	version: str
	description: str
	configuration: ApplicationSchemaConfiguration
	log: ApplicationSchemaLog
	environmentVariables: List[str]
	settings: ApplicationSchemaSettings
