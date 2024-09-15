<template>
    <div class="dna-age-gauge">
      <h2>Based on the methylation value of your sample, your DNAge is {{ dnaAge }}.</h2>
      <div class="dna-logo">
        <img src="path-to-your-dna-icon.svg" alt="DNA icon" class="dna-icon">
        <span class="dna-text">DNAge®</span>
      </div>
      <div class="age-circle">
        <span class="age-number">{{ dnaAge }}</span>
      </div>
      <div class="chart-container">
        <bar-chart :chart-data="chartData" :options="chartOptions" />
      </div>
      <div class="scale-labels">
        <span>0</span>
        <div class="chro-age">
          <div class="chro-age-circle">{{ calendarAge }}</div>
          <span>Chronological Age</span>
        </div>
        <span>100</span>
      </div>
    </div>
</template>

<script>
import { Bar } from 'vue-chartjs'

export default {
  name: 'GaugeChart',
  components: {
    BarChart: Bar
  },
  props: {
    dnaAge: {
      type: Number,
      required: true
    },
    calendarAge: {
      type: Number,
      required: true
    }
  },
  data () {
    return {
      chartData: {
        labels: ['Age'],
        datasets: [
          {
            data: [this.dnaAge],
            backgroundColor: '#4CAF50',
            borderColor: '#4CAF50',
            borderWidth: 1,
            borderRadius: 5,
            barThickness: 10
          },
          {
            data: [this.calendarAge],
            backgroundColor: '#9E9E9E',
            borderColor: '#9E9E9E',
            borderWidth: 1,
            borderRadius: 5,
            barThickness: 10
          }
        ]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [{
            display: true,
            ticks: {
              beginAtZero: true,
              max: 100,
              stepSize: 50
            },
            gridLines: {
              display: false
            }
          }],
          yAxes: [{
            display: false
          }]
        },
        legend: {
          display: false
        },
        tooltips: {
          enabled: false
        }
      }
    }
  }
}
</script>

  <style scoped>
  .dna-age-gauge {
    font-family: Arial, sans-serif;
    max-width: 500px;
    margin: 0 auto;
    text-align: center;
  }

  .dna-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 20px 0;
  }

  .dna-icon {
    width: 24px;
    height: 24px;
    margin-right: 8px;
  }

  .dna-text {
    font-weight: bold;
  }

  .age-circle {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 4px solid #4CAF50;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 20px auto;
  }

  .age-number {
    font-size: 48px;
    font-weight: bold;
  }

  .chart-container {
    height: 60px;
    margin-bottom: 10px;
  }

  .scale-labels {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .chro-age {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .chro-age-circle {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: #9E9E9E;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 14px;
    margin-bottom: 5px;
  }
</style>
