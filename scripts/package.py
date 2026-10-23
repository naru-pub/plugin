#!/usr/bin/env python3
"""Build Claude and ChatGPT packages from the same versioned source."""
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "plugin.json").read_text())
claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
assert manifest["name"] == claude["name"] == "naru"
assert manifest["version"] == claude["version"]
assert (ROOT / "skills/naru/SKILL.md").read_text().startswith("---\nname: naru\n")
assert (ROOT / "assets/icon.png").read_bytes() == (ROOT / ".claude-plugin/icon.png").read_bytes()
review = manifest["extensions"]["com.openai"]["review"]
assert len(review["test_cases"]["positive"]) == 5
assert len(review["test_cases"]["negative"]) == 3
shared = [ROOT / "LICENSE", ROOT / "README.md"]
shared += [p for directory in ("skills", "assets") for p in (ROOT / directory).rglob("*") if p.is_file()]
platforms = {
    "claude": [ROOT / ".mcp.json", ROOT / ".claude-plugin/plugin.json", ROOT / ".claude-plugin/icon.png"],
    "chatgpt": [ROOT / "plugin.json", ROOT / "mcp.json"],
}
(ROOT / "dist").mkdir(exist_ok=True)
for platform, files in platforms.items():
    target = ROOT / "dist" / f"naru-{platform}-{manifest['version']}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(shared + files):
            assert not path.is_symlink()
            archive.write(path, Path("naru") / path.relative_to(ROOT))
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        assert "naru/skills/naru/SKILL.md" in names
        assert "naru/skills/naru/references/data-sdk.md" in names
        assert not any(name.endswith(".app.json") for name in names)
        for name in names:
            if name.endswith(".json"):
                json.loads(archive.read(name))
    print(target)
