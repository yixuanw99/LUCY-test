<template>
  <div class="lucy-report">
    <header>
      <div class="header-title">
        <h1>樂稀表觀檢測報告</h1>
        <nav class="report-nav">
          <a href="#biological-age">生物年齡</a>
          <a href="#aging-speed">老化速度</a>
          <a href="#disease-risks">老化疾病風險評估</a>
        </nav>
        <div class="logo-container">
          <img class="logo" src="@/assets/logo.png" alt="LUCY logo">
          <b class = "logo-text">LUCY</b>
        </div>
      </div>
      <div class="header-info">
        <p>姓名：{{ info.name }}</p>
        <p>樣本編號：{{ info.sampleId }}</p>
        <p>採檢日期：{{ info.collectionDate }}</p>
        <p>報告日期：{{ info.reportDate }}</p>
      </div>
    </header>

    <main>
      <div v-if="reportData">
        <!-- 生物年齡 section -->
        <section id="biological-age" class="section">
          <div class="section-title">
            <h2>生物年齡</h2>
            <a class="cta" :href="'https://www.facebook.com/sharer.php?u=' + epigeneticClockFigUrl">
              <img alt="share_button" src="@/assets/share_button.png" width="20">
            </a>
          </div>
          <hr width="100%" size="3" color="#80c2ec" style="margin-top: 0px;">
          <div class="section-content">
            <div class="section-text">
              <p>表觀遺傳時鐘是一種根據DNA甲基化水平來預測生物年齡的工具。根據你的表觀基因，你的生物年齡為{{formattedBioAge}}歲，比你的實際年齡{{olderYounger}}{{diffAge}}歲。</p>
              <p>{{ olderYoungerComment }}</p>
            </div>
            <div class="section-figure">
              <GaugeChart :bio-age="formattedBioAge" :chro-age="formattedChroAge" :width="700"/>
            </div>
          </div>
        </section>

        <!-- 老化速度 section -->
        <section id="aging-speed" class="section">
          <div class="section-title">
            <h2>老化速度</h2>
            <a class="cta" :href="'https://www.facebook.com/sharer.php?u=' + agingSpeedFigUrl">
              <img alt="share_button" src="@/assets/share_button.png" width="20">
            </a>
          </div>
          <hr width="100%" size="3" color="#80c2ec" style="margin-top: 0px;">
          <div class="section-content">
            <div class="section-text">
              <p>你的老化速度為{{ formattedPaceValue }}，比{{ pacePrInverse }}％同齡的人老得慢。</p>
              <p>代表平均一個人老1.0年，你的身體老了{{ formattedPaceValue }}年。數值越低，代表老化速度越慢。</p>
            </div>
            <div class="section-figure">
              <AgingSpeedPlot :pace-value="formattedPaceValue" :pace-pr="pacePrInverse" />
            </div>
          </div>
        </section>

        <!-- 老化疾病風險評估 section -->
        <section id="disease-risks" class="section">
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
        </section>
      </div>
    </main>

    <footer>
      <p>&copy; {{ new Date().getFullYear() }} LUCY 樂稀生醫. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import GaugeChart from '@/components/GaugeChart2.vue'
import AgingSpeedPlot from '@/components/AgingSpeedPlot.vue'
import DiseaseRisksTable from '@/components/DiseaseRisksTable.vue'
import DiseaseRisksPlot from '@/components/DiseaseRisksPlot.vue'

export default {
  name: 'EpigeneticReport',
  components: {
    GaugeChart,
    AgingSpeedPlot,
    DiseaseRisksTable,
    DiseaseRisksPlot
  },
  setup () {
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

    const formattedBioAge = computed(() => parseFloat(bioAge.value.toFixed(2)))
    const formattedChroAge = computed(() => parseFloat(chroAge.value.toFixed(1)))
    const formattedPaceValue = computed(() => parseFloat(paceValue.value.toFixed(2)))

    // const deltaAge = computed(() => bioAge.value - chroAge.value) 暫時沒用到 TODO整理一些computed
    const deltaPace = computed(() => paceValue.value - 1)

    const diseaseRisks = computed(() => [
      {
        acmPaceRisk: Number((200 * deltaPace.value).toFixed(2)), // acm = all cause mortality
        cvdPaceRisk: Number((195 * deltaPace.value).toFixed(2)), // cvd = cardiovascular disease
        dmPaceRisk: Number((155 * deltaPace.value).toFixed(2)), // dm = diabetes mellitus
        adPaceRisk: Number((200 * deltaPace.value).toFixed(2)), // ad = Alzheimer's disease
        cancerPaceRisk: Number((250 * deltaPace.value).toFixed(2)) // cancer
      },
      {
        acmPaceRiskReduced01: Number((200 * (deltaPace.value - 0.05)).toFixed(2)),
        cvdPaceRiskReduced01: Number((195 * (deltaPace.value - 0.05)).toFixed(2)),
        dmPaceRiskReduced01: Number((155 * (deltaPace.value - 0.05)).toFixed(2)),
        adPaceRiskReduced01: Number((200 * (deltaPace.value - 0.05)).toFixed(2)),
        cancerPaceRiskReduced01: Number((250 * (deltaPace.value - 0.05)).toFixed(2))
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

    onMounted(() => {
      // 從 localStorage 獲取報告數據
      const storedReportData = localStorage.getItem('reportData')
      if (storedReportData) {
        reportData.value = JSON.parse(storedReportData)
        updateReportData()
      }
    })

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
      reportData,
      info,
      bioAge,
      chroAge,
      paceValue,
      formattedBioAge,
      formattedChroAge,
      formattedPaceValue,
      pacePr,
      diseaseRisks,
      epigeneticClockFigUrl,
      agingSpeedFigUrl,
      diseaseRisksFigUrl,
      diffAge,
      olderYounger,
      olderYoungerComment,
      pacePrInverse
    }
  }
}
</script>

<style scoped>
.lucy-report {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

header {
  background-color: #7bc9f6;
  width:100%;
}

.header-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 5%;
  position: fixed;
  width: -webkit-fill-available;
  background-color: #7bc9f6;
}

.header-title h1 {
  font-size: 30px;
  font-family: 'Noto Sans TC', sans-serif;
  color: #303036;
  margin: 0;
  flex: 2;
}

.report-nav {
  display: flex;
  gap: 20px;
  flex: 1;
  justify-content: center;
}

.report-nav a {
  color: #303036;
  text-decoration: none;
  font-weight: bold;
}

.report-nav a:hover {
  text-decoration: underline;
}

.logo-container {
  display: flex;
  align-items: center;
  flex: 1;
  justify-content: flex-end;
}

.logo {
  width: 60px;
  height: 60px;
}

.logo-text {
  font-size: 40px;
  font-family: 'Noto Sans TC', sans-serif;
  color: #303036;
  padding-bottom: 5px;
}

.header-info {
  background-color: #f5f5f5;
  border-radius: 30px;
  display: flex;
  gap: 10%;
  margin: 80px 5% 20px;
  justify-content: space-around;
}

main {
  flex: 1;
  padding-top: 0px;
}

.section {
  margin-bottom: 40px;
  padding: 70px 5% 0;
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-figure {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  margin-top: 20px;
  flex-wrap: wrap;
  justify-content: space-around;
}

footer {
  background-color: #f0f0f0;
  padding: 10px;
  text-align: center;
}

.cta {
  padding: 0.5% 1%;
  border: 1px outset;
  color: #303030;
  text-decoration: none;
  border-radius: 5px;
  margin: 0;
}

.cta:hover {
  background: #80c2ec;
}

/* 保留其他原有的樣式... */
</style>
