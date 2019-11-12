from criticalpath import BuildstatsCache


def test_load_elapsed_time():
    stub_filesystem = StubFilesystem({
        "somedir": ["gcc-runtime-8.3.0-r0"]
    }, {
        "somedir/gcc-runtime-8.3.0-r0/do_compile": """Event: TaskStarted
Started: 1572226085.36
Elapsed time: 1.23 seconds
Ended: 1572226615.15
"""
    })

    buildstats_cache = BuildstatsCache(["somedir"], stub_filesystem)
    time = buildstats_cache.load_elapsed_time("gcc-runtime.do_compile")
    assert time == 1.23


def test_load_elapsed_time_for_git_package():
    stub_filesystem = StubFilesystem({
        "somedir": ["linux-yocto-git-r0"]
    }, {
        "somedir/linux-yocto-git-r0/do_compile": """Event: TaskStarted
Started: 1572226085.36
Elapsed time: 1.23 seconds
Ended: 1572226615.15
"""
    })

    buildstats_cache = BuildstatsCache(["somedir"], stub_filesystem)
    time = buildstats_cache.load_elapsed_time("linux-yocto.do_compile")
    assert time == 1.23


def test_load_elapsed_time_for_multiple_search_directories():
    stub_filesystem = StubFilesystem({
        "somedir": ["gcc-runtime-8.3.0-r0"],
        "anotherdir": ["gcc-runtime-8.3.0-r0"]
    }, {
        "anotherdir/gcc-runtime-8.3.0-r0/do_compile": """Event: TaskStarted
Started: 1572226085.36
Elapsed time: 1.23 seconds
Ended: 1572226615.15
"""
    })

    buildstats_cache = BuildstatsCache(["somedir", "anotherdir"],
                                       stub_filesystem)
    time = buildstats_cache.load_elapsed_time("gcc-runtime.do_compile")
    assert time == 1.23


def test_load_elapsed_time_for_missing_directory():
    stub_filesystem = StubFilesystem({
        "somedir": []
    }, {})

    buildstats_cache = BuildstatsCache(["somedir"], stub_filesystem)
    time = buildstats_cache.load_elapsed_time("gcc-runtime.do_compile")
    assert time == 0


def test_load_elapsed_time_for_missing_statsfile():
    stub_filesystem = StubFilesystem({
        "somedir": ["gcc-runtime-8.3.0-r0"]
    }, {})

    buildstats_cache = BuildstatsCache(["somedir"], stub_filesystem)
    time = buildstats_cache.load_elapsed_time("gcc-runtime.do_compile")
    assert time == 0


def test_load_elapsed_time_for_edk_package():
    stub_filesystem = StubFilesystem({
        "somedir": ["ovmf-edk2-stable201905-r0"]
    }, {
        "somedir/ovmf-edk2-stable201905-r0/do_compile": """Event: TaskStarted
Started: 1572226085.36
Elapsed time: 585.36 seconds
Ended: 1572226615.15
"""
    })

    buildstats_cache = BuildstatsCache(["somedir"], stub_filesystem)
    time = buildstats_cache.load_elapsed_time("ovmf.do_compile")
    assert time == 585.36


class StubFilesystem:
    def __init__(self, dir_map, file_map):
        self.dir_map = dir_map
        self.file_map = file_map

    def directories(self, root):
        return self.dir_map[root]

    def path_exists(self, path):
        return path in self.file_map

    def open(self, path):
        return self.file_map[path].splitlines()
