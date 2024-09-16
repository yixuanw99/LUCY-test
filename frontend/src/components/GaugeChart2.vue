<template>
  <svg :width="width" :height="height" :viewBox="`0 0 ${width} ${height}`">
    <!-- 標題文本 -->
    <text :x="width / 2" y="30" text-anchor="middle" font-size="7">
      Based on the methylation value of your sample, your DNAge is {{ bioAge }} and your Chronological Age is {{ chroAge }}.
    </text>

    <!-- DNAge® logo -->
    <g transform="translate(20, 50)">
      <!-- <path d="M0,8 L4,0 L8,8 M4,0 L4,16" stroke="#4CAF50" stroke-width="2" fill="none" /> -->
      <text x="12" y="12" font-size="14" font-weight="bold">LUCY®</text>
    </g>

    <!-- DNAge 圓圈 -->
    <circle :cx="width / 2" cy="100" r="40" fill="#4CAF50" />
    <text :x="width / 2" y="108" text-anchor="middle" fill="white" font-size="24" font-weight="bold">
      {{ bioAge }}
    </text>

    <!-- 年齡刻度 -->
    <line x1="50" :y1="height - 80" :x2="width - 50" :y2="height - 80" stroke="#E0E0E0" stroke-width="4" />
    <rect :x="bioAgePosition" :y="height - 84" width="8" height="8" fill="#4CAF50" />
    <rect :x="chroAgePosition" :y="height - 84" width="8" height="8" fill="#9E9E9E" />

    <!-- 刻度標籤 -->
    <text x="50" :y="height - 60" text-anchor="middle" font-size="12">0</text>
    <text :x="width - 50" :y="height - 60" text-anchor="middle" font-size="12">100</text>

    <!-- Calendar Age -->
    <g :transform="`translate(${chroAgePosition}, ${height - 40})`">
      <circle cx="4" cy="0" r="15" fill="#9E9E9E" />
      <text x="4" y="4" text-anchor="middle" fill="white" font-size="12">{{ chroAge }}</text>
      <text x="4" y="30" text-anchor="middle" font-size="12">Calendar Age</text>
    </g>
  </svg>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'GaugeChart',
  props: {
    bioAge: {
      type: Number,
      required: true
    },
    chroAge: {
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
  setup (props) {
    const scalePosition = computed(() => (age) => {
      return 50 + (age / 100) * (props.width - 100)
    })

    const bioAgePosition = computed(() => scalePosition.value(props.bioAge))
    const chroAgePosition = computed(() => scalePosition.value(props.chroAge))

    return {
      bioAgePosition,
      chroAgePosition
    }
  }
}
</script>
