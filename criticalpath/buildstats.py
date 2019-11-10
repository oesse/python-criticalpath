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
                package_name = _directory_to_package(directory)
                if package_name not in package_directories:
                    package_directories[package_name] = []

                package_directories[package_name].append(
                    os.path.join(search_directory, directory)
                )

        return package_directories

    def load_elapsed_time(self, package_step_id):
        """Return the elapsed time of a package step id of the format
        'package_name.step_name', for example 'gcc-runtime.do_compile'."""

        package_name, step_name = _split_package_step_id(package_step_id)
        package_stats_file = self._find_stats_file(package_name, step_name)
        return (self._load_elapsed_time_from_file(package_stats_file)
                if package_stats_file else 0)

    def _find_stats_file(self, package_name, step_name):
        if package_name not in self.package_directories:
            return None

        search_directories = self.package_directories[package_name]
        for directory in search_directories:
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


def _directory_to_package(directory):
    match = re.match(r'(.*)-([0-9]|git).*', directory)
    return match.group(1)


def _split_package_step_id(package_step_id):
    dot_pos = package_step_id.rfind(".")
    return package_step_id[:dot_pos], package_step_id[dot_pos + 1:]
