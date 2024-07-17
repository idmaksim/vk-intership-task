from pydantic import BaseModel, Field
from typing import Any, List, Optional

class ApplicationSchemaConfigurationSpecification(BaseModel):
    jvmConfig: Optional[List[str]] = Field()


class ApplicationSchemaConfiguration(BaseModel):
    specification: Optional[ApplicationSchemaConfigurationSpecification] = Field()
    exposedPorts: Optional[List[dict]] = Field()
    sharedNamespace: Optional[int] = Field()


class ApplicationSchemaLog(BaseModel):
    level: Optional[str] = Field()


class ApplicationSchemaSettingsSettingaaa(BaseModel):
    ...


class ApplicationSchemaSettingsSettingaab(BaseModel):
    ...


class ApplicationSchemaSettings(BaseModel):
    settingAaa: Optional[ApplicationSchemaSettingsSettingaaa] = Field()
    settingAab: Optional[ApplicationSchemaSettingsSettingaab] = Field()


class ApplicationSchema(BaseModel):
    kind: Optional[str] = Field()
    name: Optional[str] = Field()
    version: Optional[str] = Field()
    description: Optional[str] = Field()
    configuration: Optional[ApplicationSchemaConfiguration] = Field()
    log: Optional[ApplicationSchemaLog] = Field()
    environmentVariables: Optional[List[str]] = Field()
    settings: Optional[ApplicationSchemaSettings] = Field()


from fastapi import FastAPI

app = FastAPI()


@app.post("/users")
async def create_user(user: ApplicationSchema) -> Any:
    return user
