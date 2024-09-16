<template>
  <div class="chart-container">
    <Radar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { defineComponent, computed } from 'vue'
import { Radar } from 'vue-chartjs'
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from 'chart.js'

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend)

export default defineComponent({
  name: 'DiseaseRisksPlot',
  components: { Radar },
  props: {
    diseaseRisks: {
      type: Array,
      required: true
    }
  },
  setup (props) {
    const chartData = computed(() => ({
      labels: ['全因死亡率', '心血管疾病', '糖尿病風險', '失智風險', '癌症風險'],
      datasets: [
        {
          label: '當前DunedinPACE風險(%)',
          backgroundColor: 'rgba(54, 162, 235, 0.05)',
          borderColor: 'rgba(54, 162, 235, 1)',
          pointBackgroundColor: 'rgba(54, 162, 235, 1)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(75, 192, 192, 1)',
          data: [
            props.diseaseRisks[0].acmPaceRisk,
            props.diseaseRisks[0].cvdPaceRisk,
            props.diseaseRisks[0].dmPaceRisk,
            props.diseaseRisks[0].adPaceRisk,
            props.diseaseRisks[0].cancerPaceRisk
          ]
        },
        {
          label: '若DunedinPACE減少0.05時風險(%)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          pointBackgroundColor: 'rgba(75, 192, 192, 1)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(54, 162, 235, 1)',
          data: [
            props.diseaseRisks[1].acmPaceRiskReduced01,
            props.diseaseRisks[1].cvdPaceRiskReduced01,
            props.diseaseRisks[1].dmPaceRiskReduced01,
            props.diseaseRisks[1].adPaceRiskReduced01,
            props.diseaseRisks[1].cancerPaceRiskReduced01
          ]
        }
      ]
    }))

    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          angleLines: {
            display: false
          },
          grid: {
            color: (context) => {
              if (context.tick.value === 0) {
                return 'rgba(0, 0, 0, 0.5)' // 0 刻度線的顏色
              }
              return 'rgba(0, 0, 0, 0.1)' // 其他刻度線的顏色
            },
            lineWidth: (context) => {
              if (context.tick.value === 0) {
                return 2 // 0 刻度線的寬度
              }
              return 1 // 其他刻度線的寬度
            }
          },
          ticks: {
            backdropColor: 'transparent',
            color: 'rgba(0, 0, 0, 0.7)' // 刻度標籤的顏色
          }
        }
      }
    }

    return { chartData, chartOptions }
  }
})
</script>

<style scoped>
.chart-container {
  width: 100%;
  max-width: 600px;
  height: 400px;
  margin: 0 auto;
}
</style>
