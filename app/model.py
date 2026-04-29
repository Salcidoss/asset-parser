from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DataAsset:
    id: str
    name: str
    type: str
    classification: str
    retention: Optional[str] = None
    confidence: float = 1.0


@dataclass
class ComponentAsset:
    id: str
    name: str
    type: str
    criticality: str
    dependencies: List[str] = field(default_factory=list)
    confidence: float = 1.0


@dataclass
class CredentialAsset:
    id: str
    name: str
    type: str
    privilege_level: str
    rotation_policy: Optional[str] = None
    confidence: float = 1.0


@dataclass
class Flow:
    origen: str
    destino: str
    tipo: str


@dataclass
class Inventory:
    componentes: List[ComponentAsset] = field(default_factory=list)
    actores: List[str] = field(default_factory=list)
    entidades: List[str] = field(default_factory=list)
    flujos: List[Flow] = field(default_factory=list)
    data_assets: List[DataAsset] = field(default_factory=list)
    component_assets: List[ComponentAsset] = field(default_factory=list)
    credential_assets: List[CredentialAsset] = field(default_factory=list)
    faltantes_inconsistencias: List[str] = field(default_factory=list)
    resumen_markdown: Optional[str] = None
    diagrama: Optional[str] = None


@dataclass
class PipelineResult:
    componentes: List[str]
    actores: List[str]
    entidades: List[str]
    flujos: List[dict]
    dataAssets: List[dict]
    componentAssets: List[dict]
    credentialAssets: List[dict]
    faltantes_inconsistencias: List[str]
    resumen_markdown: str
    diagrama: str
