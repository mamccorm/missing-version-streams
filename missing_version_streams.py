import os
import re
import sys
import argparse


def find_top_level_files_with_numbers(root_dir):
    """
    Find top-level files with numbers in their names.

    Args:
        root_dir (str): The root directory to scan.

    Returns:
        list: Sorted list of matched filenames.
    """
    pattern = re.compile(r'-\d+')
    matched_files = []
    for file in os.listdir(root_dir):
        file_path = os.path.join(root_dir, file)
        if os.path.isfile(file_path) and pattern.search(file):
            matched_files.append(file)
    matched_files.sort()
    return matched_files


def find_top_level_files_without_numbers(root_dir):
    """
    Find top-level files without numbers in their names.

    Args:
        root_dir (str): The root directory to scan.

    Returns:
        list: Sorted list of matched filenames.
    """
    pattern = re.compile(r'-\d+')
    matched_files = []
    for file in os.listdir(root_dir):
        file_path = os.path.join(root_dir, file)
        if os.path.isfile(file_path) and not pattern.search(file):
            matched_files.append(file)
    matched_files.sort()
    return matched_files


def find_version_stream_files(root_dir):
    """
    Find version stream files in the specified directory.

    Args:
        root_dir (str): The root directory to scan.

    Returns:
        set: Set of matched filenames without extensions.
    """
    matched_files = []
    for file in os.listdir(root_dir):
        file_path = os.path.join(root_dir, file)
        if os.path.isfile(file_path) and file.endswith('.yaml'):
            file = file.rsplit('.', 1)[0]
            matched_files.append(file)
    return set(matched_files)


def find_endoflife_files(root_dir):
    """
    Find end-of-life files in the specified directory.

    Args:
        root_dir (str): The root directory to scan.

    Returns:
        set: Set of matched filenames without extensions.
    """
    matched_files = []
    for file in os.listdir(root_dir):
        file_path = os.path.join(root_dir, file)
        if os.path.isfile(file_path) and file.endswith('.md'):
            file = file.rsplit('.', 1)[0]
            matched_files.append(file)
    return set(matched_files)


def main(package_repo, version_streams_repo, endoflife_repo):
    """
    Main function to process the repositories and generate reports.

    Args:
        package_repo (str): Path to the package repository.
        version_streams_repo (str): Path to the version streams 
                                    repository.
        endoflife_repo (str): Path to the end-of-life repository.
    """
    package_files_with_numbers = find_top_level_files_with_numbers(
        package_repo)
    package_files_without_numbers = find_top_level_files_without_numbers(
        package_repo)
    version_stream_files = find_version_stream_files(
        version_streams_repo)
    endoflife_files = find_endoflife_files(endoflife_repo)

    matched_files = [
        file for file in package_files_with_numbers
        if file.split('-')[0] in version_stream_files
    ]
    unmatched_files = [
        file for file in package_files_with_numbers
        if file.split('-')[0] not in version_stream_files
    ]
    endoflife_matches_unmatched = [
        file for file in unmatched_files
        if file.split('-')[0] in endoflife_files
    ]
    endoflife_matches_no_version = [
        file for file in package_files_without_numbers
        if file.split('.')[0] in endoflife_files
    ]

    total_packages_with_numbers = len(package_files_with_numbers)
    total_packages_without_numbers = len(package_files_without_numbers)
    total_with_streams = len(matched_files)
    total_without_streams = len(unmatched_files)
    total_endoflife_matches_unmatched = len(endoflife_matches_unmatched)
    total_endoflife_matches_no_version = len(endoflife_matches_no_version)
    total_endoflife_matches = (
        total_endoflife_matches_unmatched + total_endoflife_matches_no_version
    )

    print("\nSummary:")
    print(f"  Wolfi packages with version numbers in their name, but "
          f"missing a version stream: {total_without_streams}")
    print(f"  Wolfi packages found on endoflife.date, but missing a "
          f"version stream: {total_endoflife_matches}")
    print("\nSee the individual files for details:")

    files_written = []

    with open('wolfi-versioned-but-missing-version-stream.txt', 'w') as f:
        for file in unmatched_files:
            f.write(f"{file}\n")
        files_written.append('wolfi-versioned-but-missing-version-stream.txt')

    with open('endoflife-versioned-but-missing-in-wolfi.txt', 'w') as f:
        all_endoflife_matches = sorted(
            endoflife_matches_unmatched + endoflife_matches_no_version
        )
        filtered_endoflife_matches = [
            file for file in all_endoflife_matches
            if file.split('-')[0] not in version_stream_files
        ]
        for file in filtered_endoflife_matches:
            f.write(f"{file}\n")
        files_written.append('endoflife-versioned-but-missing-in-wolfi.txt')

    for file in files_written:
        print(f"  - {file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find and match package files with version streams and "
                    "end-of-life information")
    parser.add_argument('--package-repo', required=True,
                        help='Path to the package repository')
    parser.add_argument('--version-streams-repo', required=True,
                        help='Path to the version streams repository')
    parser.add_argument('--endoflife-repo', required=True,
                        help='Path to the end-of-life repository')

    args = parser.parse_args()

    if not os.path.isdir(args.package_repo):
        print(f"Error: {args.package_repo} is not a valid directory")
        sys.exit(1)

    if not os.path.isdir(args.version_streams_repo):
        print(f"Error: {args.version_streams_repo} is not a valid directory")
        sys.exit(1)

    if not os.path.isdir(args.endoflife_repo):
        print(f"Error: {args.endoflife_repo} is not a valid directory")
        sys.exit(1)

    main(args.package_repo, args.version_streams_repo, args.endoflife_repo)
