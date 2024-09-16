<template>
  <svg :width="width" :height="height" :viewBox="`0 0 ${width} ${height}`">
    <!-- 標題文本 -->
    <!-- <text :x="width / 2" y="30" text-anchor="middle" font-size="7">Based on the methylation value of your sample, your DNAge is {{ bioAge }} and your Chronological Age is {{ chroAge }}.</text> -->

    <!-- LUCY® logo -->
    <g transform="translate(40, 50)">
      <!-- <path d="M0,8 L4,0 L8,8 M4,0 L4,16" stroke="#4CAF50" stroke-width="2" fill="none" /> -->
      <text :x="0" y="0" font-size="24" font-family="Nova Mono" font-weight="bold">LUCY®</text>
    </g>

    <!-- 刻度標籤 -->
    <text :x="50" :y="height - 100" text-anchor="middle" font-size="12">0</text>
    <text :x="width - 50" :y="height - 100" text-anchor="middle" font-size="12">100</text>

    <!-- 年齡刻度 -->
    <line :x1="50" :y1="height - 120" :x2="width - 50" :y2="height - 120" stroke="#E0E0E0" stroke-width="4" />

    <!-- Bio Age -->
    <g :transform="`translate(${bioAgePosition}, ${height - 80})`">
      <path :d="bioAgePin" :transform="`translate(${-26}, ${-130})`" fill="#4CAF50" />
      <rect :x="0" :y="-44" width="8" height="8" fill="#4CAF50" />
      <circle :cx="4" cy="-100" r="22" fill="#4CAF50" />
      <text :x="4" y="-92" text-anchor="middle" fill="white" font-size="22" font-weight="bold">{{ bioAge }}</text>
      <text :x="0" y="-140" text-anchor="middle" font-size="12" font-weight="bold">Biological Age</text>
    </g>

    <!-- Calendar Age -->
    <g :transform="`translate(${chroAgePosition}, ${height - 80})`">
      <path :d="chroAgePin" :transform="`translate(${-15}, ${20}) scale(1, -1)`" fill="#9E9E9E" />
      <rect :x="0" :y="-44" width="8" height="8" fill="#9E9E9E" />
      <circle :cx="3" cy="1" r="12" fill="#9E9E9E" />
      <text :x="3" y="6" text-anchor="middle" fill="white" font-size="16">{{ chroAge }}</text>
      <text :x="0" y="35" text-anchor="middle" font-size="12" font-weight="bold">Calendar Age</text>
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
      default: 500
    },
    height: {
      type: Number,
      default: 300
    },
    bioAgePinScale: {
      type: Number,
      default: 1
    },
    chroAgePinScale: {
      type: Number,
      default: 0.6
    }
  },
  setup (props) {
    const scalePosition = computed(() => (age) => {
      return 50 + (age / 100) * (props.width - 100)
    })

    const bioAgePosition = computed(() => scalePosition.value(props.bioAge))
    const chroAgePosition = computed(() => scalePosition.value(props.chroAge))

    const createPin = (scale) => `
      M${30 * scale},0 
      C${13.4 * scale},0 0,${13.4 * scale} 0,${30 * scale} 
      C0,${51.6 * scale} ${30 * scale},${75 * scale} ${30 * scale},${75 * scale} 
      C${30 * scale},${75 * scale} ${60 * scale},${51.6 * scale} ${60 * scale},${30 * scale} 
      C${60 * scale},${13.4 * scale} ${46.6 * scale},0 ${30 * scale},0 
      Z
    `

    const bioAgePin = computed(() => createPin(props.bioAgePinScale))
    const chroAgePin = computed(() => createPin(props.chroAgePinScale))

    return {
      bioAgePosition,
      chroAgePosition,
      bioAgePin,
      chroAgePin
    }
  }
}
</script>
