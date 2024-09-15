<template>
  <div class="chart-container">
    <svg :viewBox="`0 0 ${size} ${size}`">
      <!-- 背景多边形 -->
      <polygon :points="backgroundPoints" fill="none" stroke="#ccc" />

      <!-- 中心点 -->
      <circle :cx="center" :cy="center" r="2" fill="black" />

      <!-- 数据多边形 - 基础风险 -->
      <polygon :points="horvathRiskPoints" fill="rgba(75, 192, 192, 0.2)" stroke="rgba(75, 192, 192, 1)" />

      <!-- 数据多边形 - 当前风险 -->
      <polygon :points="paceRiskPoints" fill="rgba(54, 162, 235, 0.2)" stroke="rgba(54, 162, 235, 1)" />

      <!-- 轴标签 -->
      <g v-for="(label, index) in labels" :key="index">
        <text
          :x="getLabelCoordinates(index).x"
          :y="getLabelCoordinates(index).y"
          text-anchor="middle"
          dominant-baseline="middle"
          font-size="12"
          fill="#333"
        >
          {{ label }}
        </text>
        <!-- 添加轴线 -->
        <line
          :x1="center"
          :y1="center"
          :x2="getCoordinates(100, index).x"
          :y2="getCoordinates(100, index).y"
          stroke="#ccc"
          stroke-dasharray="4"
        />
      </g>

      <!-- 图例 -->
      <g transform="translate(0, 10)">
        <rect width="20" height="20" fill="rgba(75, 192, 192, 0.2)" stroke="rgba(75, 192, 192, 1)" />
        <text x="25" y="15" font-size="10" fill="#333">基础风险(horvath)(%)</text>

        <rect y="25" width="20" height="20" fill="rgba(54, 162, 235, 0.2)" stroke="rgba(54, 162, 235, 1)" />
        <text x="25" y="40" font-size="10" fill="#333">当前风险(pace)(%)</text>
      </g>
    </svg>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'DiseaseRisksPlot',
  props: {
    diseaseRisks: {
      type: Array,
      required: true
    }
  },
  setup (props) {
    const size = ref(400)
    const maxValue = ref(100)
    const labels = ref(['全因死亡率', '心血管疾病', '糖尿病风险', '失智风险', '癌症风险'])

    const center = computed(() => size.value / 2)
    const radius = computed(() => size.value * 0.35)

    const getCoordinates = (value, index) => {
      const angle = (index * 360 / labels.value.length - 90) * (Math.PI / 180)
      const distance = radius.value * (value / maxValue.value)
      const x = center.value + Math.cos(angle) * distance
      const y = center.value + Math.sin(angle) * distance
      return { x, y }
    }

    const calculatePoints = (values) => {
      if (Array.isArray(values)) {
        return values.map((value, index) => {
          const point = getCoordinates(value, index)
          return `${point.x},${point.y}`
        }).join(' ')
      } else {
        return labels.value.map((_, index) => {
          const point = getCoordinates(values, index)
          return `${point.x},${point.y}`
        }).join(' ')
      }
    }

    const backgroundPoints = computed(() => calculatePoints(maxValue.value))

    const horvathRiskPoints = computed(() => {
      const values = [
        props.diseaseRisks[0].acmHorvathRisk,
        props.diseaseRisks[0].cvdHorvathRisk,
        props.diseaseRisks[0].dmHorvathRisk,
        props.diseaseRisks[0].adHorvathRisk,
        props.diseaseRisks[0].cancerHorvathRisk
      ]
      return calculatePoints(values)
    })

    const paceRiskPoints = computed(() => {
      const values = [
        props.diseaseRisks[1].acmPaceRisk,
        props.diseaseRisks[1].cvdPaceRisk,
        props.diseaseRisks[1].dmPaceRisk,
        props.diseaseRisks[1].adPaceRisk,
        props.diseaseRisks[1].cancerPaceRisk
      ]
      return calculatePoints(values)
    })

    const getLabelCoordinates = (index) => {
      const angle = (index * 360 / labels.value.length - 90) * (Math.PI / 180)
      const x = center.value + Math.cos(angle) * (radius.value + 30)
      const y = center.value + Math.sin(angle) * (radius.value + 30)
      return { x, y }
    }

    return {
      size,
      center,
      radius,
      labels,
      backgroundPoints,
      horvathRiskPoints,
      paceRiskPoints,
      getCoordinates,
      getLabelCoordinates
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
