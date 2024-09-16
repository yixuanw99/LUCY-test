<template>
  <div class="chart-container">
    <h3>{{ title }}</h3>
    <canvas ref="chartRef"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, watch, onBeforeUnmount, nextTick } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'DiseaseRisksPlot2',
  props: {
    title: {
      type: String,
      required: true
    },
    horvathRisk: {
      type: Number,
      required: true
    },
    paceRisk: {
      type: Number,
      required: true
    }
  },
  setup (props) {
    const chart = ref(null)
    const chartRef = ref(null)

    const createChart = () => {
      if (!chartRef.value) {
        console.error('Chart canvas element not found')
        return
      }

      const ctx = chartRef.value.getContext('2d')
      if (!ctx) {
        console.error('Failed to get 2D context from canvas')
        return
      }

      const combinedRisk = props.horvathRisk + props.paceRisk

      chart.value = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Combined Risk', 'Horvath Clock', 'DunedinPACE'],
          datasets: [{
            label: 'Risk Multiplier (HR)',
            data: [combinedRisk, props.horvathRisk, props.paceRisk],
            backgroundColor: ['#800080', '#0000FF', '#008000'],
            borderColor: ['#800080', '#0000FF', '#008000'],
            borderWidth: 1
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: false
            },
            legend: {
              display: false
            }
          },
          scales: {
            x: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Risk Multiplier (HR)'
              },
              grid: {
                display: true
              }
            },
            y: {
              title: {
                display: false
              },
              grid: {
                display: false
              }
            }
          }
        }
      })
    }

    // may cause stack overflow
    const updateChart = () => {
      if (chart.value) {
        const combinedRisk = props.horvathRisk + props.paceRisk
        chart.value.data.datasets[0].data = [combinedRisk, props.horvathRisk, props.paceRisk]
        chart.value.update()
      } else {
        console.warn('Chart not initialized, creating new chart')
        createChart()
      }
    }

    onMounted(() => {
      nextTick(() => {
        createChart()
      })
    })

    watch(() => [props.horvathRisk, props.paceRisk], () => {
      nextTick(() => {
        updateChart()
      })
    })

    onBeforeUnmount(() => {
      if (chart.value) {
        chart.value.destroy()
      }
    })

    return {
      chartRef
    }
  }
}
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 200px;
  width: 100%;
  max-width: 400px;
  margin: 20px;
}
h3 {
  text-align: center;
  margin-bottom: 10px;
}
</style>
