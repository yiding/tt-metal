// SPDX-FileCopyrightText: © 2025 Tenstorrent AI ULC
//
// SPDX-License-Identifier: Apache-2.0

#include "moreh_arange_nanobind.hpp"

#include <optional>

#include <nanobind/nanobind.h>
#include <nanobind/stl/optional.h>

#include "moreh_arange.hpp"
#include "ttnn-nanobind/decorators.hpp"

namespace ttnn::operations::moreh::moreh_arange {
void bind_moreh_arange_operation(nb::module_& mod) {
    bind_registered_operation(
        mod,
        ttnn::moreh_arange,
        "Moreh Arange Operation",
        ttnn::nanobind_arguments_t{
            nb::arg("start"),
            nb::arg("end"),
            nb::arg("step"),
            nb::arg("device"),
            nb::kw_only(),
            nb::arg("output") = nb::none(),
            nb::arg("untilize_out") = false,
            nb::arg("dtype") = DataType::BFLOAT16,
            nb::arg("memory_config") = ttnn::DRAM_MEMORY_CONFIG,
        });
}
}  // namespace ttnn::operations::moreh::moreh_arange
