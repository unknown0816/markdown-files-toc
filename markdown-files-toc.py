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


def list_markdown_files(root_dir: str) -> str:
    """
    Recursively walks through root_dir, collects all .md files except
    the root-level markdown file, and returns them as a Markdown list.
    """
    md_files = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".md"):
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, root_dir)

                # Skip root-level markdown file
                if dirpath == root_dir:
                    continue
                heading = extract_first_heading(full_path)
                md_files.append((heading, rel_path))


    markdown_list = "\n".join(
        f"- [{title}]({path})"
        for title, path in md_files
    )

    return markdown_list


def main():
    parser = argparse.ArgumentParser(description="List markdown files recursively.")
    parser.add_argument("root_directory", help="Directory to scan")

    args = parser.parse_args()

    output = list_markdown_files(args.root_directory)
    print(output)


if __name__ == "__main__":
    main()
