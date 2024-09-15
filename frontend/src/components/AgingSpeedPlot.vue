<template>
  <svg :width="width" :height="height" viewBox="0 0 400 300">
    <!-- 背景和坐標軸 -->
    <rect x="0" y="0" :width="width" :height="height" fill="#ffffff" />
    <line x1="50" :y1="height - 50" x2="350" :y2="height - 50" stroke="black" />

    <!-- 正態分佈曲線 -->
    <path :d="normalDistributionPath" fill="#777777" stroke="none" />

    <!-- X軸刻度 -->
    <g v-for="tick in xAxisTicks" :key="tick">
      <line :x1="xScale(tick)" :y1="height - 50" :x2="xScale(tick)" :y2="height - 45" stroke="black" />
      <text :x="xScale(tick)" :y="height - 25" text-anchor="middle">{{ tick }}</text>
    </g>

    <!-- 標記線和文字 -->
    <line :x1="xScale(paceValue)" y1="90" :x2="xScale(paceValue)" :y2="height - 50" stroke="black" stroke-dasharray="5,5" />
    <text :x="xScale(paceValue)" y="70" text-anchor="middle" font-weight="bold">{{ paceValue }}</text>
    <text :x="180" :y="40" font-size="14" fill="black">
      你比{{ pacePr }}%同齡的人老得慢
    </text>

    <!-- X軸標籤 -->
    <text x="200" :y="height - 5" text-anchor="middle">你的老化速度</text>
  </svg>
</template>

<script>
export default {
  name: 'AgingSpeedPlot',
  props: {
    paceValue: {
      type: Number,
      required: true
    },
    pacePr: {
      type: Number,
      required: true
    },
    width: {
      type: Number,
      default: 400
    },
    height: {
      type: Number,
      default: 300
    }
  },
  methods: {
    normalDistribution (x, mean = 1, stdDev = 0.3) {
      return Math.exp(-0.5 * Math.pow((x - mean) / stdDev, 2)) / (stdDev * Math.sqrt(2 * Math.PI))
    },
    generateNormalDistributionPath () {
      const points = []
      for (let x = 0; x <= 2; x += 0.05) {
        const y = this.normalDistribution(x)
        points.push([this.xScale(x), 250 - y * 40])
      }
      return 'M' + points.map(p => p.join(',')).join('L')
    }
  },
  computed: {
    normalDistributionPath () {
      return this.generateNormalDistributionPath()
    },
    xScale () {
      return x => 50 + (x / 2) * 300
    },
    xAxisTicks () {
      return [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
    }
  }
}
</script>
