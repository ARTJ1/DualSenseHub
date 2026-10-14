"""Community setups: checks a shared setup issue, and publishes it once the maintainer labels it 'approved'.

  python community.py check     -> comments what the code contains (or why it can't be read)
  python community.py publish   -> writes community/setups/<n>-<slug>.dshub, updates community/index.json

Issue text is untrusted: it is only read from the event file, never passed through a shell.
"""
import base64, datetime, json, os, pathlib, re, subprocess, sys, tempfile, zlib

PREFIX = "DSHUB1:"
MAX_JSON = 256 * 1024
ROOT = pathlib.Path("community")

event = json.loads(pathlib.Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8-sig"))
issue = event["issue"]
number = issue["number"]
body = issue.get("body") or ""


def section(title):
    """Text under '### Title' in an issue form body."""
    m = re.search(r"^###\s+" + re.escape(title) + r"\s*\n(.*?)(?=^###\s|\Z)", body, re.S | re.M)
    if not m:
        return ""
    text = m.group(1).strip()
    return "" if text == "_No response_" else text


def decode():
    m = re.search(re.escape(PREFIX) + r"([A-Za-z0-9_\-\s]+)", body)
    if not m:
        raise ValueError("No setup code found (it starts with DSHUB1:).")
    payload = re.sub(r"\s", "", m.group(1))
    payload += "=" * (-len(payload) % 4)
    try:
        raw = base64.urlsafe_b64decode(payload)
        d = zlib.decompressobj(-15)
        data = d.decompress(raw, MAX_JSON + 1)
        if len(data) > MAX_JSON or d.unconsumed_tail:
            raise ValueError("The setup is too large.")
        bundle = json.loads(data.decode("utf-8"))
    except (ValueError, zlib.error, UnicodeDecodeError) as e:
        raise ValueError(f"The code is damaged or incomplete ({e.__class__.__name__}).")
    if not isinstance(bundle, dict) or bundle.get("format") != "dshub-setup" or bundle.get("version") != 1:
        raise ValueError("This is not a DualSense Hub setup code.")
    return bundle


def clip(value, n):
    value = value if isinstance(value, str) else ""
    value = "".join(c for c in value if c == "\n" or c.isprintable()).strip()
    return value[:n]


def covers(bundle):
    games = [g for g in (bundle.get("games") or {}) if re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", g)]
    if bundle.get("eldenRing"):
        games.append("eldenring")
    if bundle.get("effects"):
        games.append("effects")
    if bundle.get("profiles"):
        games.append("profiles")
    return games


def gh(*args, body_text=None):
    if body_text is not None:
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".md", encoding="utf-8") as f:
            f.write(body_text)
        args = (*args, "--body-file", f.name)
    subprocess.run(["gh", *args], check=True)


def comment(text):
    gh("issue", "comment", str(number), body_text=text)


def check():
    try:
        bundle = decode()
    except ValueError as e:
        comment(f"Couldn't read this setup: {e}\n\nCopy the code again from the app (Community ??? Share your setup ??? Copy code) and edit the issue.")
        return
    games = covers(bundle)
    if not games:
        comment("The code reads fine, but the setup is empty.")
        return
    comment("Setup code reads fine. It covers: " + ", ".join(f"`{g}`" for g in games)
            + ".\n\nIt goes into the gallery once a maintainer adds the `approved` label.")


def publish():
    bundle = decode()
    games = covers(bundle)
    if not games:
        raise SystemExit("empty setup")
    name = clip(section("Name") or bundle.get("name"), 60) or f"Setup #{number}"
    description = clip(section("Description") or bundle.get("description"), 500)
    author = clip(bundle.get("author"), 40) or issue["user"]["login"]
    bundle.update(name=name, description=description, author=author)

    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:40] or "setup"
    file = f"setups/{number}-{slug}.dshub"
    (ROOT / "setups").mkdir(parents=True, exist_ok=True)
    (ROOT / file).write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index_path = ROOT / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8-sig")) if index_path.exists() else {"version": 1, "items": []}
    items = [i for i in index.get("items", []) if i.get("issue") != number]  # re-approving replaces
    items.append({
        "id": f"{number}-{slug}", "name": name, "author": author, "description": description,
        "games": games, "file": file, "added": datetime.date.today().isoformat(), "issue": number,
    })
    index["items"] = items
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(file)


if __name__ == "__main__":
    {"check": check, "publish": publish}[sys.argv[1]]()
