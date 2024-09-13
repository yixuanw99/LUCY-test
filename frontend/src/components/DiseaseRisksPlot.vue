<template>
    <div class="chart-container">
      <svg :viewBox="`0 0 ${size} ${size}`">
        <!-- 背景多邊形 -->
        <polygon :points="backgroundPoints" fill="none" stroke="#ccc" />
                
        <!-- 數據多邊形 - 基礎風險 -->
        <polygon :points="horvathRiskPoints" fill="rgba(75, 192, 192, 0.2)" stroke="rgba(75, 192, 192, 1)" />
        
        <!-- 數據多邊形 - 當前風險 -->
        <polygon :points="paceRiskPoints" fill="rgba(54, 162, 235, 0.2)" stroke="rgba(54, 162, 235, 1)" />
        
        <!-- 軸標籤 -->
        <text
            v-for="(label, index) in labels"
            :key="index"
            :x="getLabelCoordinates(index).x"
            :y="getLabelCoordinates(index).y"
            text-anchor="middle"
            dominant-baseline="middle"
            font-size="12"
            fill="#333"
        >
            {{ label }}
        </text>
        <!-- 圖例 -->
        <g transform="translate(0, 10)">
            <rect width="20" height="20" fill="rgba(75, 192, 192, 0.2)" stroke="rgba(75, 192, 192, 1)" />
            <text x="25" y="15" font-size="10" fill="#333">與同齡相比的風險程度(%)</text>
            
            <rect y="25" width="20" height="20" fill="rgba(54, 162, 235, 0.2)" stroke="rgba(54, 162, 235, 1)" />
            <text x="25" y="40" font-size="10" fill="#333">生物年齡每年輕1年可降低風險(%)</text>
        </g>
      </svg>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DiseaseRisksPlot',
    props: {
      diseaseRisks: {
        type: Array,
        required: true
      }
    },
    data() {
      return {
        size: 400,
        maxValue: 15,
        labels: ['全因死亡率', '心血管疾病', '糖尿病風險', '失智風險', '癌症風險']
      }
    },
    computed: {
      center() {
        return this.size / 2
      },
      radius() {
        return this.size * 0.35  // 減小半徑以留出更多空間給標籤
      },
      backgroundPoints() {
        return this.calculatePoints(this.maxValue)
      },
      horvathRiskPoints() {
        const values = [
          this.diseaseRisks[0].acmHorvathRisk,
          this.diseaseRisks[0].cvdHorvathRisk,
          this.diseaseRisks[0].dmHorvathRisk,
          this.diseaseRisks[0].adHorvathRisk,
          this.diseaseRisks[0].cancerHorvathRisk
        ]
        return this.calculatePoints(values)
      },
      paceRiskPoints() {
        const values = [
          this.diseaseRisks[1].acmPaceRisk,
          this.diseaseRisks[1].cvdPaceRisk,
          this.diseaseRisks[1].dmPaceRisk,
          this.diseaseRisks[1].adPaceRisk,
          this.diseaseRisks[1].cancerPaceRisk
        ]
        return this.calculatePoints(values)
      }
    },
    methods: {
      calculatePoints(values) {
        if (Array.isArray(values)) {
          return values.map((value, index) => {
            const point = this.getCoordinates(value, index)
            return `${point.x},${point.y}`
          }).join(' ')
        } else {
          return this.labels.map((_, index) => {
            const point = this.getCoordinates(values, index)
            return `${point.x},${point.y}`
          }).join(' ')
        }
      },
      getCoordinates(value, index) {
        const angle = (index * 360 / this.labels.length - 90) * (Math.PI / 180)
        const x = this.center + Math.cos(angle) * (this.radius * value / this.maxValue)
        const y = this.center + Math.sin(angle) * (this.radius * value / this.maxValue)
        return { x, y }
      },
      getLabelCoordinates(index) {
        const angle = (index * 360 / this.labels.length - 90) * (Math.PI / 180)
        const x = this.center + Math.cos(angle) * (this.radius + 30) // Add some padding
        const y = this.center + Math.sin(angle) * (this.radius + 30)
        return { x, y }
      }
    }
  }
  </script>
  
  <style scoped>
  .chart-container {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
  }
  </style>