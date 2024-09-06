<template>
    <svg :width="400" :height="400" viewBox="0 0 400 400">
      <defs>
        <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style="stop-color:#66ff66;stop-opacity:1" />
          <stop offset="50%" style="stop-color:#ffffff;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#ff0000;stop-opacity:1" />
        </linearGradient>
      </defs>
  
      <!-- 灰色背景弧 -->
      <path :d="backgroundArc" fill="none" stroke="lightgrey" stroke-width="20" />
  
      <!-- 彩色弧 -->
      <path :d="coloredArc" fill="none" stroke="url(#gaugeGradient)" stroke-width="13" />
  
      <!-- 指針 -->
      <line :x1="centerX" :y1="centerY + 25" :x2="needleX" :y2="needleY" stroke="rgba(0, 0, 0, 0.3)" stroke-width="4" />
  
      <!-- 標籤 -->
      <text :x="centerX" :y="centerY - radius - 20" text-anchor="middle" font-size="20">細胞年齡: {{ bioAge }}</text>
      <text :x="centerX" :y="centerY + radius + 40" text-anchor="middle" font-size="20">實際年齡: {{ chroAge }}</text>
      <text :x="centerX - radius / 2 - 25" :y="centerY + radius / 2 + 25" text-anchor="middle" font-size="20">{{ minValue }}</text>
      <text :x="centerX + radius / 2 + 25" :y="centerY + radius / 2 + 25" text-anchor="middle" font-size="20">{{ maxValue }}</text>
      <text :x="centerX - radius + 50" :y="centerY + 35" text-anchor="middle" font-size="20">Younger</text>
      <text :x="centerX + radius - 40" :y="centerY + 35" text-anchor="middle" font-size="20">Older</text>
    </svg>
  </template>
  
  <script>
  export default {
    name: 'GaugeChart',
    props: {
      bioAge: Number,
      chroAge: Number
    },
    data() {
      return {
        centerX: 200,
        centerY: 200,
        radius: 150,
        startAngle: 0.8 * Math.PI,
        endAngle: 2.2 * Math.PI
      }
    },
    computed: {
      minValue() {
        return Math.round(this.chroAge - 20);
      },
      maxValue() {
        return Math.round(this.chroAge + 20);
      },
      valueFrac() {
        const range = this.maxValue - this.minValue;
        return (this.bioAge - this.minValue) / range;
      },
      needleAngle() {
        return this.startAngle + this.valueFrac * (this.endAngle - this.startAngle);
      },
      needleX() {
        return this.centerX + 120 * Math.cos(this.needleAngle);
      },
      needleY() {
        return this.centerY + 25 + 120 * Math.sin(this.needleAngle);
      },
      backgroundArc() {
        return this.describeArc(this.centerX, this.centerY + 25, this.radius, this.startAngle, this.endAngle);
      },
      coloredArc() {
        const midAngle = (this.startAngle + this.endAngle) / 2;
        let coloredEndAngle;
        
        if (this.valueFrac <= 0.5) {
            coloredEndAngle = midAngle + (this.valueFrac * 2 - 1) * (midAngle - this.startAngle);
        } else {
            coloredEndAngle = this.needleAngle;
        }
        
        return this.describeArc(this.centerX, this.centerY + 25, this.radius, midAngle, coloredEndAngle, this.valueFrac > 0.5);
      }
    },
    methods: {
      polarToCartesian(centerX, centerY, radius, angleInRadians) {
        return {
          x: centerX + (radius * Math.cos(angleInRadians)),
          y: centerY + (radius * Math.sin(angleInRadians))
        };
      },
      describeArc(x, y, radius, startAngle, endAngle, clockwise = false) {
        const start = this.polarToCartesian(x, y, radius, endAngle);
        const end = this.polarToCartesian(x, y, radius, startAngle);
        const largeArcFlag = Math.abs(endAngle - startAngle) <= Math.PI ? "0" : "1";
        const sweepFlag = clockwise ? "1" : "0";
  
        return [
          "M", start.x, start.y,
          "A", radius, radius, 0, largeArcFlag, sweepFlag, end.x, end.y
        ].join(" ");
      }
    }
  }
  </script>
  
  <style scoped>
  svg {
    display: block;
    margin: 0;
    background-color: white;
  }
  </style>