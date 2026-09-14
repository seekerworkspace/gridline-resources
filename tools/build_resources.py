#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
PACKAGES = ROOT / "packages"
MANIFEST = ROOT / "resources.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_zip(version: int) -> Path:
    PACKAGES.mkdir(parents=True, exist_ok=True)
    out = PACKAGES / f"gridline_resources_v{version}.zip"
    if out.exists():
        out.unlink()

    files = [p for p in CONTENT.rglob("*") if p.is_file()]
    if not files:
        raise SystemExit("ERRO: a pasta content/ está vazia.")

    with ZipFile(out, "w", compression=ZIP_DEFLATED, compresslevel=9) as zf:
        for path in files:
            relative = path.relative_to(CONTENT)
            zf.write(path, relative.as_posix())
    return out


def main():
    parser = argparse.ArgumentParser(description="Gera o pacote obrigatório do GRIDLINE e atualiza resources.json")
    parser.add_argument("--version", type=int, required=True, help="Versão inteira dos recursos, ex.: 1")
    parser.add_argument("--base-url", required=True, help="Ex.: https://seuusuario.github.io/gridline-resources")
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    package_path = build_zip(args.version)
    size = package_path.stat().st_size
    digest = sha256_file(package_path)

    manifest = {
        "schema": 1,
        "game": "GRIDLINE",
        "required": True,
        "version": args.version,
        "package": {
            "file": package_path.name,
            "url": f"{base_url}/packages/{package_path.name}",
            "size": size,
            "sha256": digest,
        },
    }

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    mib = size / (1024 * 1024)
    print(f"Pacote: {package_path}")
    print(f"Tamanho: {mib:.2f} MiB ({size} bytes)")
    print(f"SHA-256: {digest}")
    print(f"Manifesto: {MANIFEST}")
    print()
    if size > 100 * 1024 * 1024:
        print("ERRO: o arquivo passou de 100 MiB. O GitHub bloqueia arquivos acima desse limite.")
        raise SystemExit(2)
    elif size > 25 * 1024 * 1024:
        print("AVISO: acima de 25 MiB o upload pelo navegador do GitHub não funciona; use Git/GitHub Desktop.")
    print("Pronto para commit/push no repositório do GitHub Pages.")


if __name__ == "__main__":
    main()
  
