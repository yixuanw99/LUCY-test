<template>
  <div class="chart-container">
    <Radar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { defineComponent } from 'vue'
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
    const chartData = {
      labels: ['全因死亡率', '心血管疾病', '糖尿病風險', '失智風險', '癌症風險'],
      datasets: [
        {
          label: '基礎風險(horvath)(%)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          pointBackgroundColor: 'rgba(75, 192, 192, 1)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(75, 192, 192, 1)',
          data: [
            props.diseaseRisks[0].acmHorvathRisk,
            props.diseaseRisks[0].cvdHorvathRisk,
            props.diseaseRisks[0].dmHorvathRisk,
            props.diseaseRisks[0].adHorvathRisk,
            props.diseaseRisks[0].cancerHorvathRisk
          ]
        },
        {
          label: '當前風險(pace)(%)',
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          pointBackgroundColor: 'rgba(54, 162, 235, 1)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(54, 162, 235, 1)',
          data: [
            props.diseaseRisks[1].acmPaceRisk,
            props.diseaseRisks[1].cvdPaceRisk,
            props.diseaseRisks[1].dmPaceRisk,
            props.diseaseRisks[1].adPaceRisk,
            props.diseaseRisks[1].cancerPaceRisk
          ]
        }
      ]
    }

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
