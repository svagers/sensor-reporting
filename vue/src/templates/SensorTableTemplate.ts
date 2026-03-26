import type { Column } from '@/types/column'
import PlainHeaderCell from '@/components/ui/cells/PlainHeaderCell.vue'
import MetricHeaderCell from '@/components/app/cells/MetricHeaderCell.vue'
import MetricCell from '@/components/app/cells/MetricCell.vue'
import SensorCell from '@/components/app/cells/SensorCell.vue'
import { structure } from '@/stores/structure'
import type { TableTemplate } from '@/types/tableTemplate'
import type { Sensor } from '@/types/sensor'
import { nameSearchFilter } from '@/filters/nameSearchFilter'
import { sensorTypeFilter } from '@/filters/sensorTypeFilter'

export const SensorTableTemplate: TableTemplate<Sensor> = {
  getFilters() {
    return {
      nameSearch: nameSearchFilter,
      sensorType: sensorTypeFilter,
    }
  },

  getColumns(): Column[] {
    const columns: Column[] = []

    columns.push({
      columnKey: 'name',
      label: 'Sensor',
      disableable: false,
      sortKey: (row) => row.name,
      headerComponent: PlainHeaderCell,
      headerProps: {
        label: 'Sensor',
        columnKey: 'name',
      },
      cellComponent: SensorCell,
    })

    if (structure.value?.metrics) {
      structure.value.metrics.forEach((metric) => {
        columns.push({
          columnKey: `metric_${metric.id}`,
          label: metric.name,
          disableable: true,
          sortKey: (row) => row[`metric_${metric.id}`]?.value ?? null,
          headerComponent: MetricHeaderCell,
          headerProps: {
            metric,
          },
          cellComponent: MetricCell,
          cellProps: {
            metricKey: `metric_${metric.id}`,
          },
        })
      })
    }

    return columns
  },
}
