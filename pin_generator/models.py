from dataclasses import dataclass
from pathlib import Path


@dataclass
class ImageAsset:
    local_path: Path
    file_stem: str


@dataclass
class SkuImageAsset(ImageAsset):
    sku_id: str
    sku_name: str


@dataclass
class PinRecord:
    title: str
    media_url: str
    pinterest_board: str
    thumbnail: str
    description: str
    link: str
    publish_date: str
    keywords: str
