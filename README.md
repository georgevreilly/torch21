# torch21

Torch 2.1 and Bazel experiments.

## Torch 2.1 doesn't work with Bazel

Torch 2.1 works fine if you install it and its CUDA dependencies
into a single `site-packages` (e.g., in a virtualenv).
It doesn't work with Bazel,
as it installs each dependency into its own directory tree,
which is added to `PYTHONPATH`.

Running the test from a virtualenv works on Linux:

```sh
$ python3 -m venv /pay/tmp/venv-torch21
$ /pay/tmp/venv-torch21/bin/pip install -r third_party/requirements.txt
$ /pay/tmp/venv-torch21/bin/python -m calculator.calc_test && echo yes || echo no
sys.path=['/pay/src/torch21', '/pay/src/torch21/bazel-torch21/external/python_3_8_x86_64-unknown-linux-gnu/lib/python38.zip', '/pay/src/torch21/bazel-torch21/external/python_3_8_x86_64-unknown-linux-gnu/lib/python3.8', '/pay/src/torch21/bazel-torch21/external/python_3_8_x86_64-unknown-linux-gnu/lib/python3.8/lib-dynload', '/pay/tmp/venv-torch21/lib/python3.8/site-packages']
/pay/tmp/venv-torch21/lib/python3.8/site-packages/torch/nn/modules/transformer.py:20: UserWarning: Failed to initialize NumPy: numpy.core.multiarray failed to import (Triggered internally at ../torch/csrc/utils/tensor_numpy.cpp:84.)
  device: torch.device = torch.device(torch._C._get_default_device()),  # torch.device('cpu'),
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
yes
```

(The `UserWarning` about `NumPy` is harmless and can be ignored.)

The test does `import torch`,
which causes a number of CUDA libraries to be loaded.

If you run this same test via [Bazel](https://bazel.build/), it fails.

First, install the [Bazelisk wrapper](https://github.com/bazelbuild/bazelisk/releases)
as `bazel` somewhere on your `$PATH`.
The first time that Bazelisk runs in this directory,
it will install Bazel 6.3.2 (from `.bazelversion`)
in a cache.

Then run the test:

```sh
$ bazel test //...
Starting local Bazel server and connecting to it...
INFO: Analyzed 3 targets (66 packages loaded, 15423 targets configured).
INFO: Found 2 targets and 1 test target...
FAIL: //calculator:calc_test (see /pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/execroot/__main__/bazel-out/k8-fastbuild/testlogs/calculator/calc_test/test.log)
INFO: From Testing //calculator:calc_test:
==================== Test output for //calculator:calc_test:
sys.path=['/pay/src/torch21/calculator',
    '/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/sandbox/linux-sandbox/1/execroot/__main__/bazel-out/k8-fastbuild/bin/calculator/calc_test.runfiles',
    '/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/sandbox/linux-sandbox/1/execroot/__main__/bazel-out/k8-fastbuild/bin/calculator/calc_test.runfiles/python_deps_filelock/site-packages',
    '/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/sandbox/linux-sandbox/1/execroot/__main__/bazel-out/k8-fastbuild/bin/calculator/calc_test.runfiles/python_deps_fsspec/site-packages',
... [40 directories omitted] ...
    '/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/sandbox/linux-sandbox/1/execroot/__main__/bazel-out/k8-fastbuild/bin/calculator/calc_test.runfiles/python_deps_sympy',
    '/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/sandbox/linux-sandbox/1/execroot/__main__/bazel-out/k8-fastbuild/bin/calculator/calc_test.runfiles/python_deps_torch',
    '/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/sandbox/linux-sandbox/1/execroot/__main__/bazel-out/k8-fastbuild/bin/calculator/calc_test.runfiles/python_deps_triton',
    '/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/sandbox/linux-sandbox/1/execroot/__main__/bazel-out/k8-fastbuild/bin/calculator/calc_test.runfiles/python_deps_typing_extensions',
    '/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/execroot/__main__/external/python_3_8_x86_64-unknown-linux-gnu/lib/python38.zip',
    '/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/execroot/__main__/external/python_3_8_x86_64-unknown-linux-gnu/lib/python3.8',
    '/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/execroot/__main__/external/python_3_8_x86_64-unknown-linux-gnu/lib/python3.8/lib-dynload',
    '/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/execroot/__main__/external/python_3_8_x86_64-unknown-linux-gnu/lib/python3.8/site-packages']
Traceback (most recent call last):
  File "/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/sandbox/linux-sandbox/1/execroot/__main__/bazel-out/k8-fastbuild/bin/calculator/calc_test.runfiles/python_deps_torch/site-packages/torch/__init__.py", line 174, in _load_global_deps
    ctypes.CDLL(lib_path, mode=ctypes.RTLD_GLOBAL)
  File "/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/execroot/__main__/external/python_3_8_x86_64-unknown-linux-gnu/lib/python3.8/ctypes/__init__.py", line 373, in __init__
    self._handle = _dlopen(self._name, mode)
OSError: libcufft.so.11: cannot open shared object file: No such file or directory

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/sandbox/linux-sandbox/1/execroot/__main__/bazel-out/k8-fastbuild/bin/calculator/calc_test.runfiles/__main__/calculator/calc_test.py", line 10, in <module>
    import torch  # type: ignore
  File "/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/sandbox/linux-sandbox/1/execroot/__main__/bazel-out/k8-fastbuild/bin/calculator/calc_test.runfiles/python_deps_torch/site-packages/torch/__init__.py", line 234, in <module>
    _load_global_deps()
  File "/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/sandbox/linux-sandbox/1/execroot/__main__/bazel-out/k8-fastbuild/bin/calculator/calc_test.runfiles/python_deps_torch/site-packages/torch/__init__.py", line 195, in _load_global_deps
    _preload_cuda_deps(lib_folder, lib_name)
  File "/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/sandbox/linux-sandbox/1/execroot/__main__/bazel-out/k8-fastbuild/bin/calculator/calc_test.runfiles/python_deps_torch/site-packages/torch/__init__.py", line 161, in _preload_cuda_deps
    ctypes.CDLL(lib_path)
  File "/pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/execroot/__main__/external/python_3_8_x86_64-unknown-linux-gnu/lib/python3.8/ctypes/__init__.py", line 373, in __init__
    self._handle = _dlopen(self._name, mode)
OSError: libnvJitLink.so.12: cannot open shared object file: No such file or directory
================================================================================
INFO: Elapsed time: 131.313s, Critical Path: 6.78s
INFO: 5 processes: 3 internal, 2 linux-sandbox.
INFO: Build completed, 1 test FAILED, 5 total actions
//calculator:calc_test                                                   FAILED in 0.9s
  /pay/home/georgevreilly/.cache/bazel/_bazel_georgevreilly/b060158845e808ff2a9c2fcf0dcfee37/execroot/__main__/bazel-out/k8-fastbuild/testlogs/calculator/calc_test/test.log

Executed 1 out of 1 test: 1 fails locally.
```

Note the enormous `sys.path`.
Bazel generates a separate directory for each package,
which is added to `PYTHONPATH`.

When all of the NVidia Cuda Python packages live in *one shared* `site-packages`,
it doesn't matter which order they get loaded in.
They are able to find the other `lib*.so`
libraries in the `nvidia` namespace.

## The patch

The [patch](patches/torch-2.1.0/001-cuda-libs-preload.patch) simply
reorders the preloading of `lib*.so` files slightly,
so that they are topologically sorted.
(This order was worked out by hand.)

The patch can be applied by running [wheel_patcher](scripts/wheel_patcher.py):

```sh
$ ./scripts/wheel_patcher.py --wheel /tmp/pypi/torch-2.1.0-cp38-cp38-manylinux1_x86_64.whl \
    --suffix stripe.5 --dest-dir /tmp/pypi --patch-dir ./patches/torch-2.1.0
```

This creates `torch-2.1.0+stripe.5-cp38-cp38-manylinux1_x86_64.whl`

When the patched wheel is used with Bazel, the test runs successfully.

## Using the patched wheel with rules_python

Unfortunately, I know of no easy way to convince
[rules_python](https://rules-python.readthedocs.io/)
to install a wheel from the local file system.

I was able to accomplish this by using [pip2pi](https://pypi.org/project/pip2pi/)
to create a package index on my filesystem,
then adding a custom `--index-url`
to the beginning of `third_party/requirements.txt`.

1. `pip install pip2pi` in some virtualenv
2. There's a [bug in pip2pi](https://github.com/wolever/pip2pi/issues/88#issuecomment-1886993187)
   that needs to be patched;
   without it, the `triton` package will be mishandled.
    * Apply the [5-dash patch](https://github.com/wolever/pip2pi/pull/89) by hand.
      Change the `4` at L152 to `5` in
      `$VIRTUAL_ENV/lib/python3.8/site-packages/libpip2pi/commands.py`
3. Run `pip2pi /tmp/pypi -r third_party/requirements.txt`
   to create a local package index from all the requirements.
4. Run `wheel_patcher --dest-dir /tmp/pypi --suffix stripe.5 ...`
   to create a patched Torch wheel in `/tmp/pypi`.
5. Run `dir2pi /tmp/pypi` to rebuild the local package index,
   so that the patched wheel can be located.
6. Add `--index-url=/tmp/pypi/simple`
   to the beginning of `third_party/requirements.txt`,
   then change the `torch` requirement to `torch==2.1.0+stripe.5`.
7. `bazel clean --expunge`
8. `bazel test //...` should now succeed,
   as it uses the patched Torch wheel from the local package index.
9. `ls -l $(bazel info output_base)/external/python_deps_torch`
   should show the patched wheel

## Issues

I have reported the following issues:

pytorch:

* [CUDA deps cannot be preloaded under Bazel](https://github.com/pytorch/pytorch/issues/117350).

rules_python:

* [pip_install_dependencies doesn't work with private package index repositories => Error downloading from files.pythonhosted.org](https://github.com/bazelbuild/rules_python/issues/1676) .
* [Make it easier to load wheels from the local file system](https://github.com/bazelbuild/rules_python/issues/1689).
