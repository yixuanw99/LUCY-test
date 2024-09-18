<template>
  <svg :width="width" :height="height" :viewBox="`0 0 ${width} ${height}`">
    <!-- 標題文本 -->
    <text :x="width / 2" y="40" text-anchor="middle" font-size="14" font-family="Lucida Console">Based on the methylation pattern of your saliva,</text>
    <text :x="width / 2" y="60" text-anchor="middle" font-size="14" font-family="Lucida Console">your Biological Age is <tspan font-weight="bold">{{ bioAge }}</tspan>.</text>

    <!-- LUCY® logo -->
    <!-- <g :transform="`translate(${width * 0.08}, ${height * 0.167})`"><text :x="0" :y="0" :font-size="width * 0.048" font-family="Nova Mono" font-weight="bold">LUCY®</text></g> -->

    <!-- 刻度標籤 -->
    <text :x="width * 0.1" :y="height * 0.667" text-anchor="middle" :font-size="width * 0.024" font-family="Lucida Console">0</text>
    <text :x="width * 0.9" :y="height * 0.667" text-anchor="middle" :font-size="width * 0.024" font-family="Lucida Console">100</text>

    <!-- 年齡刻度 -->
    <line :x1="width * 0.1" :y1="height * 0.6" :x2="width * 0.9" :y2="height * 0.6" stroke="#E0E0E0" :stroke-width="width * 0.008" />

    <!-- Bio Age -->
    <g :transform="`translate(${bioAgePosition}, ${height * 0.733})`">
      <path :d="bioAgePin" :transform="`translate(${-width * 0.052}, ${-height * 0.433}) scale(1)`" fill="#4CAF50" />
      <rect :x="0" :y="-height * 0.147" :width="width * 0.008" :height="height * 0.027" fill="#4CAF50" />
      <circle :cx="width * 0.008" :cy="-height * 0.333" :r="width * 0.044" fill="#4CAF50" />
      <text :x="width * 0.008" :y="-height * 0.335" text-anchor="middle" fill="white" :font-size="width * 0.034" font-weight="bold" font-family="Lucida Console">{{ bioAge }}</text>
      <text :x="0" :y="-height * 0.467" text-anchor="middle" :font-size="width * 0.024" font-family="Lucida Console" font-weight="bold">Biological Age</text>
    </g>

    <!-- Calendar Age -->
    <g :transform="`translate(${chroAgePosition}, ${height * 0.733})`">
      <path :d="chroAgePin" :transform="`translate(${-width * 0.03}, ${height * 0.067}) scale(1, -1)`" fill="#9E9E9E" />
      <rect :x="0" :y="-height * 0.147" :width="width * 0.008" :height="height * 0.027" fill="#9E9E9E" />
      <circle :cx="width * 0.006" :cy="height * 0.003" :r="width * 0.024" fill="#9E9E9E" />
      <text :x="width * 0.006" :y="height * 0.02" text-anchor="middle" fill="white" :font-size="width * 0.032" font-family="Lucida Console">{{ chroAge }}</text>
      <text :x="0" :y="height * 0.117" text-anchor="middle" :font-size="width * 0.024" font-family="Lucida Console" font-weight="bold">Calendar Age</text>
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
    }
  },
  setup (props) {
    const height = computed(() => props.width * 0.75) // 保持 4:3 的寬高比

    const scalePosition = computed(() => (age) => {
      return props.width * 0.1 + (age / 100) * (props.width * 0.8)
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

    const bioAgePin = computed(() => createPin(props.width / 500))
    const chroAgePin = computed(() => createPin(props.width / 500 * 0.6))

    return {
      height,
      bioAgePosition,
      chroAgePosition,
      bioAgePin,
      chroAgePin
    }
  }
}
</script>
