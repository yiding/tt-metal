"""Generate python stubs using nanobind stubgen.

This script generates stubs for the `_ttnn` native module (functionally
identical to invoking stubgen with --recursive) and dynamically added members of
ttnn base module.

Operations from the native module (and other composite operations defined in
python) are dynamically added to the base module using module-level code, so
they are not visible to pyright. They are also wrapped in a FastOperation /
Operation object, which makes nanobind stubgen unable to get the underlying type
of the operation.

This script extracts the dynamic members from the module and gives the unwrapped
(original) operations to nanobind stubgen.
"""
from nanobind.stubgen import StubGen
from ttnn.decorators import FastOperation, Operation
from pathlib import Path

import argparse
import ttnn
import ttnn._ttnn

def gen_ttnn_dynamic_stub(output_dir: Path):
    stubgen = StubGen(ttnn)
    stubgen.stack.append(ttnn)
    for name, child in ttnn.__dict__.items():
        # Pass through the unwrapped function to stubgen so it can emit a useful type.
        if isinstance(child, (FastOperation, Operation)):
            stubgen.put(child.function, name=name, parent=ttnn)
    with open(output_dir / "_dynamic.pyi", "w") as f:
        # Need this initial import as stubgen doesn't emit it.
        f.write("import ttnn._ttnn as _ttnn\n")
        f.write(stubgen.get())


def gen_ttnn_native_stub(output_dir: Path):
    output_file = output_dir / "_ttnn" / "__init__.pyi"
    stubgen = StubGen(
        ttnn._ttnn,
        recursive=True,
        output_file=output_file,
    )
    stubgen.put(ttnn._ttnn)
    with open(output_file, "w") as f:
        f.write(stubgen.get())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "output_dir",
        type=Path,
        help="Output directory for the base module.")
    args = parser.parse_args()
    gen_ttnn_dynamic_stub(args.output_dir)
    gen_ttnn_native_stub(args.output_dir)


if __name__ == "__main__":
    main()
