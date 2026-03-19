import os
import argparse


def extract_first_heading(filepath: str) -> str:
    """
    Reads a markdown file and returns the first heading (# ...).
    Falls back to the file name if no heading is found.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):  # First-level heading
                    return line[2:].strip()
                # optionally also allow ## or ###:
                # if line.startswith("#"):
                #    return line.lstrip("#").strip()
    except Exception:
        pass

    # fallback: filename without extension
    return os.path.splitext(os.path.basename(filepath))[0]


def list_markdown_files(root_dir: str, root_md_name: str = None) -> str:
    """
    Recursively walks through root_dir, collects all .md files except
    the root-level markdown file, and returns them as a Markdown list.
    """
#    md_files = []
    tree: dict[str, list[tuple[str, str, str]]] = {}      # dir → [(filename, title, rel_path), …]

    for dirpath, _, filenames in os.walk(root_dir):
        rel_dir = os.path.relpath(dirpath, root_dir)
        if rel_dir == ".":
            rel_dir = ""                                 # make root '' instead of '.'
        for filename in filenames:
            if filename.endswith(".md"):
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, root_dir)

                # Skip root-level markdown file
                if (not root_md_name and dirpath == root_dir) or (root_md_name and dirpath == root_dir and filename == root_md_name):
                    continue
                heading = extract_first_heading(full_path)
                tree.setdefault(rel_dir, []).append((filename, heading, rel_path))
#                md_files.append((heading, rel_path))


    lines: list[str] = []

    for rel_dir in tree:
        # ``depth`` = how many indents a *non‑index* file should have.
        #   root files → depth 0
        #   files inside a sub‑folder → depth = number of path components
        depth = 0 if rel_dir == "" else rel_dir.count(os.sep) + 1

        # sort files so that `index.md` (case‑insensitive) comes first,
        # everything else alphabetically afterwards
        files = sorted(
            tree[rel_dir],
            key=lambda item: (0 if item[0].lower() == "index.md" else 1, item[0].lower())
        )

        for fname, title, rel_path in files:
            is_index = fname.lower() in ("index.md", "readme.md")
            single_file_in_dir = (len(files) == 1)

            if is_index or single_file_in_dir:
                # Index files are shown at the *current* level
                indent = "  " * (depth - 1)   # one level less than the normal files
            else:
                # All other files are one level deeper than the directory level
                indent = "  " * depth

            lines.append(f"{indent}- [{title}]({rel_path})")

    return "\n".join(lines)

#    markdown_list = "\n".join(
#        f"- [{title}]({path})"
#        for title, path in md_files
#    )

#    return markdown_list


def main():
    parser = argparse.ArgumentParser(description="List markdown files recursively.")
    parser.add_argument("root_directory", help="Directory to scan")
    parser.add_argument("--ignore", help="Root-level markdown file to ignore", default=None)

    args = parser.parse_args()

    output = list_markdown_files(args.root_directory,  args.ignore)
    print(output)


if __name__ == "__main__":
    main()
