workspace(name = "workspace_monitor")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# Python 
http_archive(
    name = "rules_python",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.0.2/rules_python-0.0.2.tar.gz",
    strip_prefix = "rules_python-0.0.2",
    sha256 = "b5668cde8bb6e3515057ef465a35ad712214962f0b3a314e551204266c7be90c",
)

load("@rules_python//python:defs.bzl", "py_binary")