#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil
from conans import ConanFile, CMake, tools


class ConanSqlite3Installer(ConanFile):
    name = "sqlite3_installer"
    version = "3.29.0"
    description = "Self-contained, serverless, in-process SQL database engine."
    url = "http://github.com/bincrafters/conan-sqlite3"
    homepage = "https://www.sqlite.org"
    author = "Bincrafters <bincrafters@gmail.com>"
    topics = ("conan", "sqlite", "database", "sql", "serverless")
    license = "Public Domain"
    generators = "cmake"
    settings = "os_build", "arch_build", "compiler", "arch"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "threadsafe": [0, 1, 2],
               "enable_column_metadata": [True, False],
               "enable_explain_comments": [True, False],
               "enable_fts3": [True, False],
               "enable_fts4": [True, False],
               "enable_fts5": [True, False],
               "enable_json1": [True, False],
               "enable_rtree": [True, False],
               "omit_load_extension": [True, False]
               }
    default_options = {"shared": False,
                       "fPIC": True,
                       "threadsafe": 1,
                       "enable_column_metadata": False,
                       "enable_explain_comments": False,
                       "enable_fts3": False,
                       "enable_fts4": False,
                       "enable_fts5": False,
                       "enable_json1": False,
                       "enable_rtree": False,
                       "omit_load_extension": False
                       }
    _source_subfolder = "source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        url = self.conan_data["sources"][self.version]["url"]
        archive_name = os.path.basename(url)
        archive_name = os.path.splitext(archive_name)[0]
        os.rename(archive_name, self._source_subfolder)

    def config_options(self):
        if self.settings.os_build == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["THREADSAFE"] = self.options.threadsafe
        cmake.definitions["ENABLE_COLUMN_METADATA"] = self.options.enable_column_metadata
        cmake.definitions["ENABLE_EXPLAIN_COMMENTS"] = self.options.enable_explain_comments
        cmake.definitions["ENABLE_FTS3"] = self.options.enable_fts3
        cmake.definitions["ENABLE_FTS4"] = self.options.enable_fts4
        cmake.definitions["ENABLE_FTS5"] = self.options.enable_fts5
        cmake.definitions["ENABLE_JSON1"] = self.options.enable_json1
        cmake.definitions["ENABLE_RTREE"] = self.options.enable_rtree
        cmake.definitions["OMIT_LOAD_EXTENSION"] = self.options.omit_load_extension
        cmake.definitions["HAVE_FDATASYNC"] = True
        cmake.definitions["HAVE_GMTIME_R"] = True
        cmake.definitions["HAVE_LOCALTIME_R"] = True
        cmake.definitions["HAVE_POSIX_FALLOCATE"] = True
        cmake.definitions["HAVE_STRERROR_R"] = True
        cmake.definitions["HAVE_USLEEP"] = True
        if self.settings.os_build == "Windows":
            cmake.definitions["HAVE_LOCALTIME_R"] = False
            cmake.definitions["HAVE_POSIX_FALLOCATE"] = False
        if tools.is_apple_os(self.settings.os_build):
            cmake.definitions["HAVE_POSIX_FALLOCATE"] = False
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        header = tools.load(os.path.join(self._source_subfolder, "sqlite3.h"))
        license_content = header[3:header.find("***", 1)]
        tools.save("LICENSE", license_content)

        self.copy("LICENSE", dst="licenses")

        cmake = self._configure_cmake()
        cmake.install()

        shutil.rmtree(os.path.join(self.package_folder, "include"))

    def package_id(self):
        self.info.include_build_settings()
        if self.settings.os_build == "Windows":
            del self.info.settings.arch_build # same build is used for x86 and x86_64
        del self.info.settings.arch
        del self.info.settings.compiler
        del self.info.settings.compiler

    def package_info(self):
        if self.package_folder is not None:
            self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
            self.env_info.CMAKE_ROOT = self.package_folder
        else:
            self.output.warn("No package folder have been created.")
