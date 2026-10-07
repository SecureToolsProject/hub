"""Regression coverage for canonical Hub destinations and release availability."""
import contextlib
import importlib.util
import io
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("url_map", ROOT / "scripts/validate-h3-url-map.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "public", self.root / "public")
        shutil.copytree(ROOT / "docs/migrations", self.root / "docs/migrations")
        self.original = validator.MAP_PATH, validator.PUBLIC_ROOT, validator.REDIRECTS_PATH
        validator.MAP_PATH = self.root / "docs/migrations/h3-url-map.csv"
        validator.PUBLIC_ROOT = self.root / "public"
        validator.REDIRECTS_PATH = validator.PUBLIC_ROOT / "_redirects"
    def tearDown(self):
        validator.MAP_PATH, validator.PUBLIC_ROOT, validator.REDIRECTS_PATH = self.original
        self.temp.cleanup()
    def result(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return validator.main()
    def change(self, path, old, new):
        p = self.root / path
        text = p.read_text(encoding="utf-8")
        self.assertIn(old, text)
        p.write_text(text.replace(old, new), encoding="utf-8")
    def test_current_contract_passes(self):
        self.assertEqual(self.result(), 0)
    def test_stale_csv_target_rejected(self):
        self.change("docs/migrations/h3-url-map.csv", "https://tools.securetools.app/pdf/merge/", "https://tools.securetools.app/tools/pdf/merge/")
        self.assertEqual(self.result(), 1)
    def test_stale_redirect_target_rejected(self):
        self.change("public/_redirects", "https://tools.securetools.app/pdf/split/", "https://tools.securetools.app/tools/pdf/split/")
        self.assertEqual(self.result(), 1)
    def test_legacy_published_link_rejected(self):
        self.change("public/products/web-utilities/index.html", "https://tools.securetools.app/image/resize/", "https://tools.securetools.app/tools/image/resize/")
        self.assertEqual(self.result(), 1)
    def test_pdf_ocr_discovery_required(self):
        self.change("public/products/web-utilities/index.html", "https://tools.securetools.app/pdf/to-text/", "https://tools.securetools.app/pdf/")
        self.assertEqual(self.result(), 1)
    def test_document_scanner_not_published(self):
        self.change("public/products/web-utilities/index.html", "https://tools.securetools.app/image/to-text/", "https://tools.securetools.app/scan/")
        self.assertEqual(self.result(), 1)
    def test_apex_redirect_loop_rejected(self):
        self.change("public/_redirects", "https://tools.securetools.app/pdf/merge/", "https://securetools.app/tools/pdf/merge/")
        self.assertEqual(self.result(), 1)
    def test_image_to_pdf_alias_must_target_final_tool(self):
        self.change("public/_redirects", "/tools/image-to-pdf/ https://tools.securetools.app/pdf/images-to-pdf/", "/tools/image-to-pdf/ https://tools.securetools.app/image-to-pdf/")
        self.assertEqual(self.result(), 1)
    def test_extra_speculative_legacy_route_rejected(self):
        self.change("docs/migrations/h3-url-map.csv", "/tools/pdf/merge/", "/tools/pdf/to-text/")
        self.assertEqual(self.result(), 1)

if __name__ == "__main__":
    unittest.main()
