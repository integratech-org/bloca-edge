from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PhaseEnum(StrEnum):
    heating = "heating"
    compression = "compression"
    cooling = "cooling"


class Telemetry(BaseModel):
    model_config = ConfigDict(extra="ignore")
    seq: int = Field(ge=0)
    phase: PhaseEnum
    phase_elapsed_s: int = Field(ge=0)
    temp_c: float
    power_w: float
    pressure_mpa: float
    height_mm: float


class TelemetryMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")

    type: Literal["telemetry"] = "telemetry"
    payload: Telemetry
