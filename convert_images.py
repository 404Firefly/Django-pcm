
from pathlib import Path
from PIL import Image

# Lokasi folder gambar static
IMAGE_DIR = Path("core/static/images")

# Gambar yang akan dikonversi
FILES = [
    "logo.png",
]

QUALITY = 82

for filename in FILES:
    source = IMAGE_DIR / filename
    destination = source.with_suffix(".webp")

    if not source.exists():
        print(f"[TIDAK DITEMUKAN] {source}")
        continue

    with Image.open(source) as image:
        image.save(
            destination,
            "WEBP",
            quality=QUALITY,
            method=6
        )

    original_size = source.stat().st_size / 1024
    new_size = destination.stat().st_size / 1024

    print(f"\nFile: {filename}")
    print(f"Ukuran awal : {original_size:.2f} KB")
    print(f"Ukuran baru : {new_size:.2f} KB")
    print(f"Penghematan : {100 - (new_size / original_size * 100):.1f}%")

print("\nKonversi selesai!")
