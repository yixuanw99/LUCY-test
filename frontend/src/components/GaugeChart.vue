<template>
  <canvas ref='gauge' width='400' height='400'></canvas>
</template>

<script>
export default {
  name: 'GaugeChart',
  props: {
    bioAge: Number,
    chroAge: Number
  },
  mounted () {
    this.drawGauge()
  },
  watch: {
    bioAge: 'drawGauge',
    chroAge: 'drawGauge'
  },
  methods: {
    drawGauge () {
      const canvas = this.$refs.gauge
      const ctx = canvas.getContext('2d')
      ctx.clearRect(0, 0, canvas.width, canvas.height) // Clear previous drawings

      // Dynamically set min and max values
      const minValue = Math.round(this.chroAge - 20)
      const maxValue = Math.round(this.chroAge + 20)

      // Center of the canvas
      const centerX = (canvas.width / 2)
      const centerY = (canvas.height / 2)
      const radius = 150

      // Angles for the gauge
      // const startAngle = 200 * Math.PI / 180
      // const endAngle = -20 * Math.PI / 180
      const startAngle = 0.8 * Math.PI
      const endAngle = 2.2 * Math.PI

      // Draw the grey background arc
      ctx.beginPath()
      ctx.arc(centerX, centerY + 25, radius, startAngle, endAngle)
      ctx.lineWidth = 20
      ctx.strokeStyle = 'lightgrey'
      ctx.stroke()

      // Calculate where the needle should point
      let valueFrac
      if (this.bioAge > this.chroAge) {
        valueFrac = 0.5 + 0.5 * ((this.bioAge - this.chroAge) / (maxValue - this.chroAge))
      } else if (this.bioAge === this.chroAge) {
        valueFrac = 0.5
      } else {
        valueFrac = 0.5 - 0.5 * ((this.chroAge - this.bioAge) / (this.chroAge - minValue))
      }

      const needleAngle = startAngle + valueFrac * (endAngle - startAngle)

      // Create gradient color for the arc (green to white to red)
      const gradient = ctx.createLinearGradient(0, 0, canvas.width, 0)
      gradient.addColorStop(0, '#66ff66')
      gradient.addColorStop(0.5, '#ffffff')
      gradient.addColorStop(1, '#ff0000')

      // Draw the colored arc depending on the needle's position
      ctx.beginPath()
      if (valueFrac <= 0.5) {
        ctx.arc(centerX, centerY + 25, radius, 1.5 * Math.PI, needleAngle, true)
        ctx.lineWidth = 13
        ctx.strokeStyle = gradient
      } else {
        ctx.arc(centerX, centerY + 25, radius, 1.5 * Math.PI, needleAngle)
        ctx.lineWidth = 13
        ctx.strokeStyle = gradient
      }
      ctx.stroke()

      // Draw the needle
      const needleLength = 120
      const needleWidth = 4
      const needleX = centerX + needleLength * Math.cos(needleAngle)
      const needleY = centerY + 25 + needleLength * Math.sin(needleAngle)

      ctx.beginPath()
      ctx.moveTo(centerX, centerY + 25)
      ctx.lineTo(needleX, needleY)
      ctx.lineWidth = needleWidth
      ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)'
      ctx.stroke()

      // Draw the labels
      ctx.font = '20px Arial'
      ctx.fillStyle = 'black'
      ctx.textAlign = 'center'

      ctx.fillText('細胞年齡: ' + this.bioAge, centerX, centerY - radius - 20) // Biological age at top
      ctx.fillText('實際年齡: ' + this.chroAge, centerX, centerY + radius + 40) // Chronological age at bottom
      ctx.fillText(minValue, centerX - radius / 2 - 25, centerY + radius / 2 + 25) // Min value on left
      ctx.fillText(maxValue, centerX + radius / 2 + 25, centerY + radius / 2 + 25) // Max value on right

      // Draw the 'Younger' and 'Older' text
      ctx.fillText('Younger', centerX - radius + 50, centerY + 35)
      ctx.fillText('Older', centerX + radius - 40, centerY + 35)
    }
  }
}
</script>

<style scoped>
  canvas {
    display: block;
    margin: 0;
    background-color: white
  }
</style>
