<template>
  <div class="chart-container">
    <h3>{{ title }}</h3>
    <canvas ref="chart"></canvas>
  </div>
</template>

<script>
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
  data () {
    return {
      chart: null
    }
  },
  mounted () {
    this.createChart()
  },
  methods: {
    createChart () {
      const ctx = this.$refs.chart.getContext('2d')
      const combinedRisk = this.horvathRisk + this.paceRisk

      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Combined Risk', 'Horvath Clock', 'DunedinPACE'],
          datasets: [{
            label: 'Risk Multiplier (HR)',
            data: [combinedRisk, this.horvathRisk, this.paceRisk],
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
    },
    updateChart () {
      if (this.chart) {
        const combinedRisk = this.horvathRisk + this.paceRisk
        this.chart.data.datasets[0].data = [combinedRisk, this.horvathRisk, this.paceRisk]
        this.chart.update()
      }
    }
  },
  watch: {
    horvathRisk () {
      this.updateChart()
    },
    paceRisk () {
      this.updateChart()
    }
  },
  beforeUnmount () {
    if (this.chart) {
      this.chart.destroy()
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
