import os
import re


class Filesystem:
    """This class implements the subset of filesystem functionality needed for
    the BuildstatsCache to work correctly. It will be replaced by a stub for
    unit testing."""

    def directories(self, root):
        with os.scandir(root) as it:
            return [entry.name for entry in it
                    if entry.is_dir()]

    def path_exists(self, path):
        return os.path.exists(path)

    def open(self, path):
        with open(path, 'r') as file:
            return file.readlines()


class BuildstatsCache:
    """This class provides access to the time build step took for packages'
    buildstats located in the filesystem."""

    def __init__(self, search_directories, filesystem=Filesystem()):
        """Construct a cache using a list of search directories."""

        self.filesystem = filesystem
        self.package_directories = self._cache_directories(search_directories)

    def _cache_directories(self, search_directories):
        package_directories = {}

        for search_directory in search_directories:
            for directory in self.filesystem.directories(search_directory):
                if directory not in package_directories:
                    package_directories[directory] = []

                package_directories[directory].append(
                    os.path.join(search_directory, directory)
                )

        return package_directories

    def load_elapsed_time(self, package_step_id):
        """Return the elapsed time of a package step id of the format
        'package_name.step_name', for example 'gcc-runtime.do_compile'."""

        package_name, step_name = _split_package_step_id(package_step_id)
        package_stats_file = self._find_stats_file(package_name, step_name)

        if not package_stats_file:
            return 0

        return self._load_elapsed_time_from_file(package_stats_file)

    def _find_stats_file(self, package_name, step_name):
        directories = [path
                       for dir_name, paths in self.package_directories.items()
                       for path in paths
                       if _package_matches(package_name, dir_name)]

        if len(directories) == 0:
            return None

        for directory in reversed(directories):
            filename = os.path.join(directory, step_name)
            if self.filesystem.path_exists(filename):
                return filename

        return None

    def _load_elapsed_time_from_file(self, filename):
        for line in self.filesystem.open(filename):
            match = re.match(r'Elapsed time: ([0-9]+\.[0-9]+) seconds', line)
            if match:
                return float(match.group(1))

        raise RuntimeError(
            "Could not find 'Elapsed time' in '{}'".format(filename))


def _split_package_step_id(package_step_id):
    dot_pos = package_step_id.rfind(".")
    return package_step_id[:dot_pos], package_step_id[dot_pos + 1:]


def _package_matches(package_name, dir_name):
    dash_pos = dir_name.rfind('-', 0, -1)
    while dash_pos > 0:
        if dir_name[:dash_pos] == package_name:
            return True
        dash_pos = dir_name.rfind('-', 0, dash_pos)
