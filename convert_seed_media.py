
from pathlib import Path
from PIL import Image, ImageOps

# Lokasi folder sumber dan hasil
BASE_DIR = Path(__file__).resolve().parent

SOURCE_DIR = BASE_DIR / "core" / "seed_media"
OUTPUT_DIR = BASE_DIR / "core" / "seed_media_webp"

# Pengaturan optimasi
WEBP_QUALITY = 82
MAX_SIZE = (1600, 1600)

# Format gambar yang akan diproses
SUPPORTED_FORMATS = {
    ".jpg",
    ".jpeg",
    ".png",
}


def convert_to_webp(
    source_dir=SOURCE_DIR,
    output_dir=OUTPUT_DIR,
    quality=WEBP_QUALITY,
    max_size=MAX_SIZE,
):
    """
    Mengonversi seluruh gambar dalam folder sumber
    menjadi WebP tanpa mengubah file aslinya.
    """

    source_dir = Path(source_dir)
    output_dir = Path(output_dir)

    if not source_dir.exists():
        print(f"Folder sumber tidak ditemukan: {source_dir}")
        return

    total = 0
    success = 0
    failed = 0

    for image_path in source_dir.rglob("*"):

        if not image_path.is_file():
            continue

        if image_path.suffix.lower() not in SUPPORTED_FORMATS:
            continue

        total += 1

        try:
            # Mempertahankan struktur subfolder
            relative_path = image_path.relative_to(source_dir)

            # Mengubah ekstensi menjadi .webp
            output_path = (
                output_dir / relative_path
            ).with_suffix(".webp")

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with Image.open(image_path) as image:

                # Memperbaiki orientasi berdasarkan metadata EXIF
                image = ImageOps.exif_transpose(image)

                # Mengubah mode warna agar kompatibel dengan WebP
                if image.mode not in ("RGB", "RGBA"):
                    image = image.convert("RGBA" if "transparency" in image.info else "RGB")

                # Membatasi resolusi tanpa mengubah rasio aspek
                image.thumbnail(
                    max_size,
                    Image.Resampling.LANCZOS,
                )

                # Menyimpan hasil WebP
                image.save(
                    output_path,
                    format="WEBP",
                    quality=quality,
                    method=6,
                )

            original_size = image_path.stat().st_size
            optimized_size = output_path.stat().st_size

            reduction = (
                (1 - optimized_size / original_size) * 100
                if original_size > 0 else 0
            )

            success += 1

            print(
                f"[BERHASIL] {relative_path} | "
                f"{original_size / 1024:.1f} KB -> "
                f"{optimized_size / 1024:.1f} KB | "
                f"Hemat {reduction:.1f}%"
            )

        except Exception as error:
            failed += 1
            print(f"[GAGAL] {image_path}: {error}")

    print("\n========== RINGKASAN ==========")
    print(f"Total gambar ditemukan : {total}")
    print(f"Berhasil dikonversi    : {success}")
    print(f"Gagal                  : {failed}")
    print(f"Folder hasil           : {output_dir}")


if __name__ == "__main__":
    convert_to_webp()
