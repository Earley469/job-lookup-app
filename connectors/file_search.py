import os
from pathlib import Path


def _label_for_path(base_path: str) -> str:
    return Path(base_path).name or base_path


def search_network_folders(query, base_paths, max_depth=6, max_matches_per_path=50):
    """Search configured network folders for files/subfolders whose name contains query.

    Walks each base path up to max_depth levels deep, matching directory and file
    names against the query (case-insensitive substring match). Returns normalized
    result dicts in the same shape as the database records, plus a list of any
    base paths that could not be reached (e.g. an unmapped network drive).
    """
    query_lower = query.lower()
    results = []
    unavailable_paths = []

    for base_path in base_paths:
        base = Path(base_path)
        if not base.exists():
            unavailable_paths.append(base_path)
            continue

        label = _label_for_path(base_path)
        matches_found = 0
        base_depth = len(base.parts)

        for root, dirs, files in os.walk(base_path, onerror=lambda err: None):
            if matches_found >= max_matches_per_path:
                break

            depth = len(Path(root).parts) - base_depth
            if depth >= max_depth:
                dirs[:] = []
                continue

            for name in list(dirs) + files:
                if matches_found >= max_matches_per_path:
                    break
                if query_lower not in name.lower():
                    continue

                full_path = os.path.join(root, name)
                try:
                    relative = os.path.relpath(full_path, base_path)
                except ValueError:
                    relative = full_path

                results.append({
                    "source": label,
                    "record_type": "folder" if name in dirs else "file",
                    "job_number": None,
                    "serial_number": None,
                    "summary": relative,
                    "status": None,
                    "details": None,
                    "source_url": full_path,
                })
                matches_found += 1

    return results, unavailable_paths
