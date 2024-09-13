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
            <div class="section">
                <div class="section-title">
                    <h2>生物年齡</h2>
                    <a class="cta" :href="'https://www.facebook.com/sharer.php?u=' + epigeneticClock_fig_url">
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

            <div class="section">
                <div class="section-title">
                    <h2>老化速度</h2>
                    <a class="cta" :href="'https://www.facebook.com/sharer.php?u=' + agingSpeed_fig_url">
                        <img alt="share_button" src="@/assets/share_button.png" width="20">
                    </a>
                </div>
                <hr width="100%" size="3" color="#80c2ec" style="margin-top: 0px;">
                <div class="section-content">
                    <div class="section-text">
                        <p>你的老化速度為{{ paceValue }}，比{{ pacePrInverse }}％同齡的人老得慢。</p>
                        <P>代表平均一個人老1.0年，你的身體老了{{paceValue}}年。數值越低，代表老化速度越慢。</p>
                    </div>
                    <div class="section-figure">
                        <AgingSpeedPlot :pace-value="paceValue" :pace-pr="pacePrInverse" />
                    </div>
                </div>
            </div>

            <div class="section">
                <div class="section-title">
                    <h2>老化疾病風險評估</h2>
                    <a class="cta" :href="'https://www.facebook.com/sharer.php?u=' + diseaseRisks_fig_url">
                        <img alt="share_button" src="@/assets/share_button.png" width="20">
                    </a>
                </div>
                <hr width="100%" size="3" color="#80c2ec" style="margin-top: 0px;">
                <div class="section-content">
                    <div class="section-figure">
                        <disease-risks-table :disease-risks="diseaseRisks"></disease-risks-table>
                        <disease-risks-plot :disease-risks="diseaseRisks"></disease-risks-plot>
                        <disease-risks-plot2 title="全因死亡率風險" :horvath-risk="diseaseRisks[0].acmHorvathRisk" :pace-risk="diseaseRisks[1].acmPaceRisk" />
                        <disease-risks-plot2 title="心血管疾病風險" :horvath-risk="diseaseRisks[0].cvdHorvathRisk" :pace-risk="diseaseRisks[1].cvdPaceRisk" />
                        <disease-risks-plot2 title="糖尿病風險" :horvath-risk="diseaseRisks[0].dmHorvathRisk" :pace-risk="diseaseRisks[1].dmPaceRisk" />
                        <disease-risks-plot2 title="失智風險" :horvath-risk="diseaseRisks[0].adHorvathRisk" :pace-risk="diseaseRisks[1].adPaceRisk" />
                        <disease-risks-plot2 title="癌症風險" :horvath-risk="diseaseRisks[0].cancerHorvathRisk" :pace-risk="diseaseRisks[1].cancerPaceRisk" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import GaugeChart from '@/components/GaugeChart.vue'
import AgingSpeedPlot from '@/components/AgingSpeedPlot.vue'
import DiseaseRisksTable from '@/components/DiseaseRisksTable.vue'
import DiseaseRisksPlot from '@/components/DiseaseRisksPlot.vue'
import DiseaseRisksPlot2 from '@/components/DiseaseRisksPlot2.vue'
import axios from 'axios'

export default {
    name: 'EpigeneticReport',
    components: {
        GaugeChart,
        AgingSpeedPlot,
        DiseaseRisksTable,
        DiseaseRisksPlot,
        DiseaseRisksPlot2
    },
    data() {
        return {
            inputSampleId: '',
            reportData: null,
            info: {
                name: '',
                sampleId: '',
                collectionDate: '',
                reportDate: ''
            },
            bioAge: 0,
            chroAge: 0,
            paceValue: 0,
            pacePr: 0,
            diseaseRisks: [
                { acmHorvathRisk: 0, cvdHorvathRisk: 0, dmHorvathRisk: 0, adHorvathRisk: 0, cancerHorvathRisk: 0 },
                { acmPaceRisk: 0, cvdPaceRisk: 0, dmPaceRisk: 0, adPaceRisk: 0, cancerPaceRisk: 0 }
            ],
            epigeneticClock_fig_url: '',
            agingSpeed_fig_url: '',
            diseaseRisks_fig_url: ''
        }
    },
    computed: {
        diffAge() {
            return Math.abs(Math.round((this.bioAge - this.chroAge) * 100) / 100);
        },
        olderYounger() {
            return this.bioAge > this.chroAge ? '老' : '年輕';
        },
        olderYoungerComment() {
            return this.bioAge < this.chroAge ? '恭喜你！代表跟同年齡的相比，統計上你有更長的餘命。' : '糟糕了！與同齡人相比起來統計上有較短的餘命。';
        },
        pacePrInverse() {
            return 100 - this.pacePr;
        }
    },
    methods: {
        async fetchReport() {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/report/${this.inputSampleId}`);
                this.reportData = response.data;
                this.updateReportData();
            } catch (error) {
                console.error('Error fetching report:', error);
                // 在這裡處理錯誤，例如顯示錯誤消息給用戶
            }
        },
        updateReportData() {
            if (this.reportData) {
                this.info.name = this.reportData.user_id;
                this.info.sampleId = this.reportData.sample_id;
                this.info.collectionDate = this.reportData.collection_date;
                this.info.reportDate = this.reportData.report_date;
                this.bioAge = this.reportData.bio_age;
                this.chroAge = this.reportData.chro_age;
                this.paceValue = this.reportData.pace_value;
                this.pacePr = this.reportData.pace_pr;
                this.diseaseRisks = [
                    {
                        acmHorvathRisk: this.reportData.acm_horvath_risk,
                        cvdHorvathRisk: this.reportData.cvd_horvath_risk,
                        dmHorvathRisk: this.reportData.dm_horvath_risk,
                        adHorvathRisk: this.reportData.ad_horvath_risk,
                        cancerHorvathRisk: this.reportData.cancer_horvath_risk
                    },
                    {
                        acmPaceRisk: this.reportData.acm_pace_risk,
                        cvdPaceRisk: this.reportData.cvd_pace_risk,
                        dmPaceRisk: this.reportData.dm_pace_risk,
                        adPaceRisk: this.reportData.ad_pace_risk,
                        cancerPaceRisk: this.reportData.cancer_pace_risk
                    }
                ];
            }
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