import shlex
import subprocess
from typing import Dict

import numpy as np
import pandas as pd

from backend.hardware_query import HardwareQuery

flags = ["timestamp", "driver_version", "count", "name" or "gpu_name",
         "serial" or "gpu_serial", "uuid" or "gpu_uuid",
         "pci.bus_id" or "gpu_bus_id", "pci.domain", "pci.bus", "pci.device",
         "pci.device_id", "pci.sub_device_id", "pcie.link.gen.current",
         "pcie.link.gen.max", "pcie.link.width.current", "pcie.link.width.max",
         "index", "display_mode", "display_active", "persistence_mode",
         "accounting.mode", "accounting.buffer_size", "driver_model.current",
         "driver_model.pending", "vbios_version",
         "inforom.img" or "inforom.image", "inforom.oem", "inforom.ecc",
         "inforom.pwr" or "inforom.power",
         "gom.current" or "gpu_operation_mode.current",
         "gom.pending" or "gpu_operation_mode.pending", "fan.speed", "pstate",
         "clocks_throttle_reasons.supported", "clocks_throttle_reasons.active",
         "clocks_throttle_reasons.gpu_idle",
         "clocks_throttle_reasons.applications_clocks_setting",
         "clocks_throttle_reasons.sw_power_cap",
         "clocks_throttle_reasons.hw_slowdown",
         "clocks_throttle_reasons.hw_thermal_slowdown",
         "clocks_throttle_reasons.hw_power_brake_slowdown",
         "clocks_throttle_reasons.sw_thermal_slowdown",
         "clocks_throttle_reasons.sync_boost", "memory.total", "memory.used",
         "memory.free", "compute_mode", "utilization.gpu",
         "utilization.memory", "encoder.stats.sessionCount",
         "encoder.stats.averageFps", "encoder.stats.averageLatency",
         "ecc.mode.current", "ecc.mode.pending",
         "ecc.errors.corrected.volatile.device_memory",
         "ecc.errors.corrected.volatile.register_file",
         "ecc.errors.corrected.volatile.l1_cache",
         "ecc.errors.corrected.volatile.l2_cache",
         "ecc.errors.corrected.volatile.texture_memory",
         "ecc.errors.corrected.volatile.total",
         "ecc.errors.corrected.aggregate.device_memory",
         "ecc.errors.corrected.aggregate.register_file",
         "ecc.errors.corrected.aggregate.l1_cache",
         "ecc.errors.corrected.aggregate.l2_cache",
         "ecc.errors.corrected.aggregate.texture_memory",
         "ecc.errors.corrected.aggregate.total",
         "ecc.errors.uncorrected.volatile.device_memory",
         "ecc.errors.uncorrected.volatile.register_file",
         "ecc.errors.uncorrected.volatile.l1_cache",
         "ecc.errors.uncorrected.volatile.l2_cache",
         "ecc.errors.uncorrected.volatile.texture_memory",
         "ecc.errors.uncorrected.volatile.total",
         "ecc.errors.uncorrected.aggregate.device_memory",
         "ecc.errors.uncorrected.aggregate.register_file",
         "ecc.errors.uncorrected.aggregate.l1_cache",
         "ecc.errors.uncorrected.aggregate.l2_cache",
         "ecc.errors.uncorrected.aggregate.texture_memory",
         "ecc.errors.uncorrected.aggregate.total",
         "retired_pages.single_bit_ecc.count" or "retired_pages.sbe",
         "retired_pages.double_bit.count" or "retired_pages.dbe",
         "retired_pages.pending", "temperature.gpu", "temperature.memory",
         "power.management", "power.draw", "power.limit",
         "enforced.power.limit", "power.default_limit", "power.min_limit",
         "power.max_limit", "clocks.current.graphics" or "clocks.gr",
         "clocks.current.sm" or "clocks.sm",
         "clocks.current.memory" or "clocks.mem",
         "clocks.current.video" or "clocks.video",
         "clocks.applications.graphics" or "clocks.applications.gr",
         "clocks.applications.memory" or "clocks.applications.mem",
         "clocks.default_applications.graphics",
         "clocks.default_applications.memory",
         "clocks.max.graphics" or "clocks.max.gr",
         "clocks.max.sm" or "clocks.max.sm",
         "clocks.max.memory" or "clocks.max.mem"]
joined_flags = ','.join(flags)


def has_gpu():
    """
    Checks whether a GPU is accessible.
    :return:
    """
    try:
        process = subprocess.Popen(shlex.split(
            "nvidia-smi --format=csv,nounits --query-gpu=timestamp"),
            stdout=subprocess.PIPE)
        output, error = process.communicate()
        return not error
    except Exception:
        return False


class GPUQuery(HardwareQuery):
    """Query for the GPU.
    """

    def get_bash_command(self):
        """inherited
        """
        return "nvidia-smi --format=csv,nounits --query-gpu=" + joined_flags

    def get_custom_index(self) -> list:
        """Gets the index for the resulting dataframe.
        """
        return ['name', 'count']

    def parse_query_result(self, result) -> Dict[str, pd.DataFrame]:
        """inherited
        """
        lines = result.splitlines()
        lines = np.array([np.array(line.split(', ')) for line in lines])
        lines = lines.transpose()
        data = {line[0]: [line[1]] for line in lines}
        data['timestamp'] = self.timestamp
        df = pd.DataFrame(data=data)

        return {'gpu': df}


if __name__ == "__main__":
    GPUQuery().query()
