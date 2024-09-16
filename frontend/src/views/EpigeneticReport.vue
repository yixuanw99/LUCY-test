<template>
  <div class="container">
    <div class="header">
      <div class="header-title">
        <h1>樂稀表觀年齡報告</h1>
        <div class="logo-container">
          <img class="logo" src="@/assets/logo.png" alt="LUCY logo">
          <p class="logo-text"><b>LUCY</b></p>
        </div>
      </div>
      <div class="header-info">
        <p>姓名：{{ info.name }}</p>
        <p>採檢日期：{{ info.collectionDate }}</p>
        <p>樣本編號：{{ info.sampleId }}</p>
        <p>報告日期：{{ info.reportDate }}</p>
      </div>
    </div>

    <div class="input-section">
      <input v-model="inputSampleId" placeholder="輸入樣本ID" />
      <button @click="fetchReport">獲取報告</button>
    </div>

    <div v-if="reportData">
      <!-- 生物年齡 section -->
      <div class="section">
        <div class="section-title">
          <h2>生物年齡</h2>
          <a class="cta" :href="'https://www.facebook.com/sharer.php?u=' + epigeneticClockFigUrl">
            <img alt="share_button" src="@/assets/share_button.png" width="20">
          </a>
        </div>
        <hr width="100%" size="3" color="#80c2ec" style="margin-top: 0px;">
        <div class="section-content">
          <div class="section-text">
            <p>表觀遺傳時鐘是一種根據DNA甲基化水平來預測生物年齡的工具。根據你的表觀基因，你的生物年齡為{{bioAge}}歲，比你的實際年齡{{olderYounger}}{{diffAge}}歲。</p>
            <p>{{ olderYoungerComment }}</p>
          </div>
          <div class="section-figure">
            <GaugeChart :bio-age="bioAge" :chro-age="chroAge" />
          </div>
        </div>
      </div>

      <!-- 老化速度 section -->
      <div class="section">
        <div class="section-title">
          <h2>老化速度</h2>
          <a class="cta" :href="'https://www.facebook.com/sharer.php?u=' + agingSpeedFigUrl">
            <img alt="share_button" src="@/assets/share_button.png" width="20">
          </a>
        </div>
        <hr width="100%" size="3" color="#80c2ec" style="margin-top: 0px;">
        <div class="section-content">
          <div class="section-text">
            <p>你的老化速度為{{ paceValue }}，比{{ pacePrInverse }}％同齡的人老得慢。</p>
            <p>代表平均一個人老1.0年，你的身體老了{{paceValue}}年。數值越低，代表老化速度越慢。</p>
          </div>
          <div class="section-figure">
            <AgingSpeedPlot :pace-value="paceValue" :pace-pr="pacePrInverse" />
          </div>
        </div>
      </div>

      <!-- 老化疾病風險評估 section -->
      <div class="section">
        <div class="section-title">
          <h2>老化疾病風險評估</h2>
          <a class="cta" :href="'https://www.facebook.com/sharer.php?u=' + diseaseRisksFigUrl">
            <img alt="share_button" src="@/assets/share_button.png" width="20">
          </a>
        </div>
        <hr width="100%" size="3" color="#80c2ec" style="margin-top: 0px;">
        <div class="section-content">
          <div class="section-figure">
            <disease-risks-table :disease-risks="diseaseRisks"></disease-risks-table>
            <disease-risks-plot :disease-risks="diseaseRisks"></disease-risks-plot>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import GaugeChart from '@/components/GaugeChart.vue'
import AgingSpeedPlot from '@/components/AgingSpeedPlot.vue'
import DiseaseRisksTable from '@/components/DiseaseRisksTable.vue'
import DiseaseRisksPlot from '@/components/DiseaseRisksPlot.vue'
import axios from 'axios'

export default {
  name: 'EpigeneticReport',
  components: {
    GaugeChart,
    AgingSpeedPlot,
    DiseaseRisksTable,
    DiseaseRisksPlot
  },
  setup () {
    const inputSampleId = ref('')
    const reportData = ref(null)
    const info = reactive({
      name: '',
      sampleId: '',
      collectionDate: '',
      reportDate: ''
    })
    const bioAge = ref(0)
    const chroAge = ref(0)
    const paceValue = ref(0)
    const pacePr = ref(0)

    const deltaAge = computed(() => bioAge.value - chroAge.value)
    const deltaPace = computed(() => paceValue.value - 1)

    const diseaseRisks = computed(() => [
      {
        acmHorvathRisk: Number((4.6 * deltaAge.value).toFixed(2)), // acm = all cause mortality
        cvdHorvathRisk: Number((4.0 * deltaAge.value).toFixed(2)), // cvd = cardiovascular disease
        dmHorvathRisk: Number((8.0 * deltaAge.value).toFixed(2)), // dm = diabetes mellitus
        adHorvathRisk: Number((4.1 * deltaAge.value).toFixed(2)), // ad = Alzheimer's disease
        cancerHorvathRisk: Number((6.0 * deltaAge.value).toFixed(2)) // cancer
      },
      {
        acmPaceRisk: Number((500 * deltaPace.value).toFixed(2)),
        cvdPaceRisk: Number((195 * deltaPace.value).toFixed(2)),
        dmPaceRisk: Number((155 * deltaPace.value).toFixed(2)),
        adPaceRisk: Number((500 * deltaPace.value).toFixed(2)),
        cancerPaceRisk: Number((500 * deltaPace.value).toFixed(2))
      }
    ])

    const epigeneticClockFigUrl = ref('')
    const agingSpeedFigUrl = ref('')
    const diseaseRisksFigUrl = ref('')

    const diffAge = computed(() => {
      return Math.abs(Math.round((bioAge.value - chroAge.value) * 100) / 100)
    })

    const olderYounger = computed(() => {
      return bioAge.value > chroAge.value ? '老' : '年輕'
    })

    const olderYoungerComment = computed(() => {
      return bioAge.value < chroAge.value
        ? '恭喜你！代表跟同年齡的相比，統計上你有更長的餘命。'
        : '糟糕了！與同齡人相比起來統計上有較短的餘命。'
    })

    const pacePrInverse = computed(() => {
      return 100 - pacePr.value
    })

    const fetchReport = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/report/${inputSampleId.value}`)
        reportData.value = response.data
        updateReportData()
      } catch (error) {
        console.error('Error fetching report:', error)
        // 在這裡處理錯誤，例如顯示錯誤消息給用戶
      }
    }

    const updateReportData = () => {
      if (reportData.value) {
        info.name = reportData.value.user_id
        info.sampleId = reportData.value.sample_id
        info.collectionDate = reportData.value.collection_date
        info.reportDate = reportData.value.report_date
        bioAge.value = reportData.value.bio_age
        chroAge.value = reportData.value.chro_age
        paceValue.value = reportData.value.pace_value
        pacePr.value = reportData.value.pace_pr
      }
    }

    return {
      inputSampleId,
      reportData,
      info,
      bioAge,
      chroAge,
      paceValue,
      pacePr,
      diseaseRisks,
      epigeneticClockFigUrl,
      agingSpeedFigUrl,
      diseaseRisksFigUrl,
      diffAge,
      olderYounger,
      olderYoungerComment,
      pacePrInverse,
      fetchReport
    }
  }
}
</script>

<style scoped>
.input-section {
  margin: 20px 0;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.input-section input {
  padding: 5px 10px;
  font-size: 16px;
}

.input-section button {
  padding: 5px 15px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

.input-section button:hover {
  background-color: #45a049;
}

.section-figure {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

/* 其他現有的樣式... */
</style>
