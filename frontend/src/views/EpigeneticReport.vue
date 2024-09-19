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
          <a href="https://lucyhealth.com.tw/" target="_blank" rel="noopener noreferrer">
            <img class="logo" src="@/assets/logo.png" alt="LUCY logo">
            <b class = "logo-text">LUCY</b>
          </a>
        </div>
      </div>
    </header>

    <main :style="{ paddingTop: `90px` }">
      <div class="user-info">
        <h2>Information</h2>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">姓名：</span>
            <span class="info-value">{{ info.name }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">樣本編號：</span>
            <span class="info-value">{{ info.sampleId }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">採檢日期：</span>
            <span class="info-value">{{ info.collectionDate }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">報告日期：</span>
            <span class="info-value">{{ info.reportDate }}</span>
          </div>
        </div>
      </div>
      <div v-if="reportData">
        <!-- 生物年齡 section -->
        <section id="biological-age" class="section">
          <div class="section-title">
            <h2>生物年齡</h2>
            <div class="section-actions">
              <button class="share-button" @click="shareSection('biological-age')" :disabled="isGeneratingImage">
                <img alt="share_button" src="@/assets/share_button.png" width="20">
              </button>
              <button class="download-button" @click="downloadSectionImage('biological-age')"
                      :disabled="isGeneratingImage">
                {{ isGeneratingImage ? '生成圖片中...' : '下載圖片' }}
              </button>
            </div>
          </div>
          <hr width="100%" size="3" color="#80c2ec" style="margin-top: 0px;">
          <div class="section-content">
            <div class="section-text">
              <p>表觀遺傳時鐘（Epigenetic Clock）是一種根據DNA甲基化水平來預測生物年齡的工具。DNA甲基化是影響基因表達的化學修飾，隨著年齡增長會發生變化。表觀遺傳時鐘通過測量特定DNA位點的甲基化程度來估算個體的生物年齡，這種方法可用於評估健康狀況、老化速度，甚至預測疾病風險。</p>
              <p v-html="bioAgeComment"></p>
            </div>
            <div class="section-figure">
              <GaugeChart :bio-age="formattedBioAge" :chro-age="formattedChroAge" :width="450"/>
            </div>
          </div>
        </section>

        <!-- 老化速度 section -->
        <section id="aging-speed" class="section">
          <div class="section-title">
            <h2>老化速度</h2>
            <div class="section-actions">
              <a class="cta" :href="'https://www.facebook.com/sharer.php?u=' + agingSpeedFigUrl">
                <img alt="share_button" src="@/assets/share_button.png" width="20">
              </a>
              <button class="download-button" @click="downloadSectionImage('aging-speed')"
                      :disabled="isGeneratingImage">
                {{ isGeneratingImage ? '生成圖片中...' : '下載圖片' }}
              </button>
            </div>
          </div>
          <hr width="100%" size="3" color="#80c2ec" style="margin-top: 0px;">
          <div class="section-content">
            <div class="section-text">
              <p>老化速度是一種測量個體老化速度的指標，基於紐西蘭Dunedin縱向研究的數據發展而來。它利用DNA甲基化的變化來評估身體系統的衰老速率。老化速度能夠顯示”當下”跟同齡人相比老的快還是慢。這個指標幫助研究者和受測者瞭解老化進程，提供個性化的健康幹預建議。</p>
              <p>老化速度反映的是老化當前動態變化，類似於加速器。即使 一個人Horvath 顯示生物年齡比實際年齡輕，也可能 DunedinPACE 顯示老化速率加快。</p>
              <p v-html="paceComment"></p>
            </div>
            <div class="section-figure">
              <AgingSpeedPlot :pace-value="formattedPaceValue" :pace-pr="pacePrInverse" :width="450" />
            </div>
          </div>
        </section>

        <!-- 老化疾病風險評估 section -->
        <section id="disease-risks" class="section">
          <div class="section-title">
            <h2>老化疾病風險評估</h2>
            <div class="section-actions">
              <a class="cta" :href="'https://www.facebook.com/sharer.php?u=' + diseaseRisksFigUrl">
                <img alt="share_button" src="@/assets/share_button.png" width="20">
              </a>
              <button class="download-button" @click="downloadSectionImage('disease-risks')"
                      :disabled="isGeneratingImage">
                {{ isGeneratingImage ? '生成圖片中...' : '下載圖片' }}
              </button>
            </div>
          </div>
          <hr width="100%" size="3" color="#80c2ec" style="margin-top: 0px;">
          <div class="section-content">
            <div class="section-figure">
              <div class="table-and-description">
                <disease-risks-table :disease-risks="diseaseRisks"></disease-risks-table>
                <p>placeholder還不確定這邊的文案放甚麼</p>
              </div>
              <disease-risks-plot :disease-risks="diseaseRisks"></disease-risks-plot>
            </div>
          </div>
        </section>
        <button>Share<i class="fas fa-share-alt"></i></button>
      </div>
    </main>

    <footer>
      <p>&copy; {{ new Date().getFullYear() }} LUCY. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import html2canvas from 'html2canvas'
import GaugeChart from '@/components/GaugeChart.vue'
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

    const bioAgeComment = computed(() => {
      const ageDifference = bioAge.value - chroAge.value
      const baseMessage = `根據你的表觀遺傳訊息，你的生物年齡為<strong>${formattedBioAge.value}</strong>歲`

      if (Math.abs(ageDifference) < 2) {
        return `${baseMessage}。你的身體狀況與同齡人相比處於平均水平，這是一個良好的跡象。為了進一步優化健康狀況，你可以專注於一些小的改變，例如增加高強度的運動訓練，或者更加規律地進行壓力管理，這將有助於進一步提升你的健康指數。`
      } else {
        const ageComparisonMessage = `，比你的實際年齡${formattedChroAge.value}歲要${ageDifference < 0 ? '年輕' : '老'}了<strong>${diffAge.value}</strong>歲。`

        if (ageDifference < 0) {
          return `${baseMessage}${ageComparisonMessage}恭喜你！代表跟同年齡的相比，統計上你有更長的餘命。這意味著你擁有健康的生活方式，讓你的生理機能維持在更年輕的水平。繼續保持這種積極的健康習慣，這將有助於進一步延緩老化速度，增強身體韌性和抵抗疾病的能力。保持這種正向的生活方式，例如規律運動、健康飲食、良好的睡眠和壓力管理，將能進一步鞏固你的健康優勢，延長壽命。`
        } else {
          return `${baseMessage}${ageComparisonMessage}這可能表明你的身體正在承受更多的壓力或生活方式需要進行一定的調整，這將影響到你的整體健康。不要擔心，這是一個改善健康的好機會！你可以從一些關鍵生活領域開始進行調整，例如減少壓力、增加有氧運動、改善飲食結構，以及更加規律的睡眠習慣。這些變化將有助於降低你的生物年齡，讓你在未來的健康評估中獲得更積極的結果。`
        }
      }
    })

    const paceComment = computed(() => {
      const pace = formattedPaceValue.value
      let comment = `你的老化速度為<strong>${pace}</strong>，比<strong>${pacePrInverse.value}%</strong>同齡的人老得慢。代表平均一個人老1.0年，你的身體老了<strong>${pace}</strong>年。數值越低，代表老化速度越慢。<br><br>`

      if (pace >= 0.97 && pace <= 1.03) {
        comment += '你的老化速度處於<strong>正常範圍</strong>。這意味著你的老化速度與年齡增長的速度基本一致。'
      } else if (pace > 1.03 && pace < 1.2) {
        comment += '你的老化速度<strong>略快於正常</strong>。這表示你的衰老速度稍微加快，可能需要關注一些生活方式的調整。'
      } else if (pace >= 1.2) {
        comment += '你的老化速度<strong>明顯加快</strong>。這表示衰老速度加快，生理功能退化的風險增加。建議你積極採取措施改善生活方式，以減緩老化速度。'
      } else if (pace < 0.97 && pace > 0.8) {
        comment += '你的老化速度<strong>略慢於正常</strong>。這是一個好現象，表明你的生活方式可能對健康有積極影響。'
      } else if (pace <= 0.8) {
        comment += '你的老化速度<strong>明顯減緩</strong>。這表明你的衰老速度比正常人慢，潛在的健康風險降低。繼續保持良好的生活習慣，有助於維持這種優勢。'
      }

      return comment
    })

    const pacePrInverse = computed(() => {
      return 100 - pacePr.value
    })

    const isGeneratingImage = ref(false)
    const shareMessage = ref('')

    const generateSectionImage = async (sectionId) => {
      isGeneratingImage.value = true
      try {
        const element = document.getElementById(sectionId)
        if (!element) {
          console.error(`Element with id ${sectionId} not found`)
          return null
        }

        const canvas = await html2canvas(element)
        return canvas
      } catch (error) {
        console.error('Error generating image:', error)
        return null
      } finally {
        isGeneratingImage.value = false
      }
    }

    const downloadSectionImage = async (sectionId) => {
      const canvas = await generateSectionImage(sectionId)
      if (!canvas) return

      canvas.toBlob((blob) => {
        const url = URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `${sectionId}-report.png`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        URL.revokeObjectURL(url)
      }, 'image/png')
    }

    const shareSection = async (sectionId) => {
      const canvas = await generateSectionImage(sectionId)
      if (!canvas) return

      canvas.toBlob(async (blob) => {
        const file = new File([blob], `${sectionId}-report.png`, { type: 'image/png' })

        if (navigator.share) {
          try {
            await navigator.share({
              files: [file],
              title: '樂稀表觀檢測報告',
              text: `查看我的${sectionId}報告結果！`
            })
            console.log('Successfully shared')
            shareMessage.value = '分享成功！'
          } catch (error) {
            console.error('Error sharing:', error)
            shareMessage.value = '分享失敗，請稍後再試。'
          }
        } else {
          console.log('Web Share API not supported')
          shareMessage.value = '瀏覽器不支援一鍵分享功能，已下載圖檔'
          await downloadSectionImage(sectionId)
        }
      }, 'image/png')
    }

    // onMounted(() => {
    //   // 從 localStorage 獲取報告數據
    //   const storedReportData = localStorage.getItem('reportData')
    //   if (storedReportData) {
    //     reportData.value = JSON.parse(storedReportData)
    //     updateReportData()
    //   }
    // })

    const route = useRoute()
    const reportIndex = parseInt(route.params.id || '0', 10)

    onMounted(async () => {
      if (process.env.NODE_ENV === 'production') {
        const response = await fetch(process.env.BASE_URL + 'mockdata/mock-data.json')
        const mockData = await response.json()
        reportData.value = mockData.reports[reportIndex] // 使用傳遞的索引
      } else {
        // 在開發環境中從localStorage獲取報告數據
        const storedReportData = localStorage.getItem('reportData')
        if (storedReportData) {
          reportData.value = JSON.parse(storedReportData)
        }
      }
      updateReportData()
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
      bioAgeComment,
      pacePrInverse,
      paceComment,
      isGeneratingImage,
      downloadSectionImage,
      shareSection,
      shareMessage
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
  width:100%;
  position: fixed;
}

.header-title {
  display: flex;
  color: white;
  justify-content: space-between;
  align-items: center;
  padding: 10px 5% 5px;
  position: fixed;
  width: -webkit-fill-available;
  background-color: #3498db;
}

.header-title h1 {
  font-size: 30px;
  font-family: 'Noto Sans TC', sans-serif;
  color: #ffffff;
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
  color: #ffffff;
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

.logo-container a {
  display: flex;
  align-items: center;
  cursor: pointer;
  text-decoration: none;
}

.logo {
  width: 60px;
  height: 60px;
}

.logo-text {
  font-size: 40px;
  font-family: 'Nova Mono', sans-serif;
  color: #ffffff;
}

.user-info {
  background-color: #f1f8ff;
  border-radius: 10px;
  margin: 0 5% -70px;
  padding: 10px 15px;
}

.user-info h2 {
  font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
  margin: 0 0 10px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}

.info-item {
  display: flex;
}

.info-label {
  font-weight: bold;
  color: #3498db;
  font-family: 'Noto Sans TC', sans-serif;
}

.info-value {
  font-family: 'Noto Sans TC', 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
}

main {
  flex: 1;
}

.section {
  margin-bottom: -90px;
  padding: 90px 5% 0;
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title h2 {
  font-family: 'Noto Sans TC', sans-serif;
  color: #3498db;
  margin: 0;
}

.section-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: 'Noto Sans TC', sans-serif;
  color: #262626;
}

.table-and-description {
  flex: 1;
}

.section-figure {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  width: 100%;
  flex-wrap: wrap;
  justify-content: space-around;
}

footer {
  text-align: center;
  margin-top: 80px;
  color: #7f8c8d;
  font-size: 0.9em;
}

.section-actions {
  display: flex;
  gap: 10px;  /* 在按鈕之間添加一些間距 */
  align-items: center;
}

.cta, .download-button {
  padding: 1.5% 0 0.5%;
  color: #303030;
  text-decoration: none;
  border-radius: 5px;
  cursor: pointer;
}

.cta:hover, .download-button:hover {
  background: #a9deff;
}

.download-button {
  padding-bottom: 5px;
  background: none;
  border: none;
  font-size: 15px;
  font-family: 'Noto Sans TC', sans-serif;
}

.share-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
}

.share-button:hover {
  background: #a9deff;
  border-radius: 5px;
}

@media (max-width: 768px) {
  .section-content {
    flex-direction: column;
    align-items: stretch;
  }

  .section-figure {
    width: 100%;
  }

  /* Adjust the GaugeChart, AgingSpeedPlot, and other components to be responsive */
  .section-figure :deep(svg) {
    width: 100% !important;
    height: auto !important;
  }
}

/* 保留其他原有的樣式... */
</style>
