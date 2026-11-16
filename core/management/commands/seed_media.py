
from pathlib import Path

from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = "Upload seluruh file core/seed_media ke Supabase Storage."

    def handle(self, *args, **options):
        source_dir = Path(settings.BASE_DIR) / "core" / "seed_media"

        if not source_dir.exists():
            raise CommandError(
                f"Folder sumber tidak ditemukan: {source_dir}"
            )

        files = sorted(
            path for path in source_dir.rglob("*")
            if path.is_file()
        )

        if not files:
            self.stdout.write(
                self.style.WARNING("Tidak ada file untuk diunggah.")
            )
            return

        uploaded = 0
        skipped = 0
        failed = 0
        total_size = 0

        for path in files:
            relative_path = path.relative_to(source_dir).as_posix()
            file_size = path.stat().st_size

            try:
                if default_storage.exists(relative_path):
                    self.stdout.write(
                        f"[LEWATI] {relative_path} sudah tersedia."
                    )
                    skipped += 1
                    continue

                with path.open("rb") as file:
                    default_storage.save(relative_path, File(file))

                self.stdout.write(
                    self.style.SUCCESS(
                        f"[UPLOAD] {relative_path} "
                        f"({file_size / 1024:.2f} KB)"
                    )
                )

                uploaded += 1
                total_size += file_size

            except Exception as error:
                self.stdout.write(
                    self.style.ERROR(
                        f"[GAGAL] {relative_path}: {error}"
                    )
                )
                failed += 1

        self.stdout.write("")
        self.stdout.write("=" * 45)
        self.stdout.write(
            self.style.SUCCESS(f"Berhasil diunggah : {uploaded}")
        )
        self.stdout.write(f"Dilewati           : {skipped}")
        self.stdout.write(
            self.style.ERROR(f"Gagal              : {failed}")
        )
        self.stdout.write(
            f"Total ukuran upload: {total_size / (1024 * 1024):.2f} MB"
        )
        self.stdout.write("=" * 45)
