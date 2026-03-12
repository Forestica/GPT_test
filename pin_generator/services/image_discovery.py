from pathlib import Path

from pin_generator.models import ImageAsset

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def discover_images(images_dir: Path) -> list[ImageAsset]:
    assets: list[ImageAsset] = []
    if not images_dir.exists():
        return assets

    for path in sorted(images_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            assets.append(ImageAsset(local_path=path, file_stem=path.stem))
    return assets


def make_public_media_url(local_path: Path, media_base_url: str) -> str:
    """
    Pinterest CSV expects a public URL.
    We map local filename to a future uploaded URL:
    https://your-domain.com/pins/my_file.png
    """
    return f"{media_base_url.rstrip('/')}/{local_path.name}"
