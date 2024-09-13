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
                <!-- TODO unavailable link-->
                <a class="cta" :href="'https://www.facebook.com/sharer.php?u=' + agingSpeed_fig_url">
                    <img alt="share_button" src="@/assets/share_button.png" width="20">
                </a>
            </div>
            <hr width="100%" size="3" color="#80c2ec" style="margin-top: 0px;">
            <div class="section-content">
                <div class="section-text">
                    <p>你的老化速度為{{ paceValue }}，比{{ pacePr }}％同齡的人老得慢。</p>
                    <P>代表平均一個人老1.0年，你的身體老了{{paceValue}}年。數值越低，代表老化速度越慢。</p>
                </div>
                <div class="section-figure">
                    <AgingSpeedPlot :pace-value="paceValue" :pace-pr="pacePr" />
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">
                <h2>老化疾病風險評估</h2>
                <!-- TODO unavailable link-->
                <a class="cta" :href="'https://www.facebook.com/sharer.php?u=' + diseaseRisks_fig_url">
                    <img alt="share_button" src="@/assets/share_button.png" width="20">
                </a>
            </div>
            <hr width="100%" size="3" color="#80c2ec" style="margin-top: 0px;">
            <div class="section-content">
                <!-- <div class="section-text">
                    <ul>
                        <li v-for="risk in diseaseRisks" :key="risk.name">
                            {{ risk.name }}: {{ risk.description }}
                        </li>
                    </ul>
                </div> -->
                <div class="section-figure">
                    <disease-risks-table :disease-risks="diseaseRisks"></disease-risks-table>
                    <disease-risks-plot :disease-risks="diseaseRisks"></disease-risks-plot>
                </div>
            </div>
        </div>

        <button @click="updateAges">隨機產生數據</button>
    </div>
</template>

<script>
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
    data() {
        return {
            bioAge: 70.96,
            chroAge: 58.54,
            paceValue: 0.82,
            pacePr: 65,
            info: {
                name: '吳亦烜',
                sampleId: 'A7S1',
                collectionDate: '2024/06/31',
                reportDate: '2024/09/01'
            },
            epigeneticClock: {
                diffAge: 0,
                olderYounger: '',
                olderYoungerComment: ''
            },
            agingSpeed: {
                // deprecated
                pacePositive: '',
            },
            diseaseRisks: 
            [
                { acmHorvathRisk: 8, cvdHorvathRisk: 4, dmHorvathRisk: 6, adHorvathRisk: 5, cancerHorvathRisk: 12 },
                { acmPaceRisk: 4, cvdPaceRisk: 2, dmPaceRisk: 1, adPaceRisk: 3, cancerPaceRisk: 6 }
            ]
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
        pacePositive() {
            return this.paceValue < 1 ? '慢' : '快';
        }
    },
    methods: {
        updateAges() {
            // Randomly generate new ages
            this.bioAge = Math.round((Math.random() * (74 - 45) + 45) * 100) / 100;
            this.chroAge = Math.round((Math.random() * (74 - 45) + 45) * 100) / 100;
            this.paceValue = Math.round((Math.random() * (1.4 - 0.6) + 0.6) * 100) / 100;
            this.pacePr = Math.round((Math.random() * (74 - 45) + 45) * 100) / 100;

            // Update diseaseRisks with new random values
            const horvathRisks = {
                acmHorvathRisk: Math.floor(Math.random() * 12),
                cvdHorvathRisk: Math.floor(Math.random() * 12),
                dmHorvathRisk: Math.floor(Math.random() * 12),
                adHorvathRisk: Math.floor(Math.random() * 12),
                cancerHorvathRisk: Math.floor(Math.random() * 12)
            };

            const paceRisks = {
                acmPaceRisk: Math.floor(Math.random() * (horvathRisks.acmHorvathRisk + 1)),
                cvdPaceRisk: Math.floor(Math.random() * (horvathRisks.cvdHorvathRisk + 1)),
                dmPaceRisk: Math.floor(Math.random() * (horvathRisks.dmHorvathRisk + 1)),
                adPaceRisk: Math.floor(Math.random() * (horvathRisks.adHorvathRisk + 1)),
                cancerPaceRisk: Math.floor(Math.random() * (horvathRisks.cancerHorvathRisk + 1))
            };

            this.diseaseRisks = [horvathRisks, paceRisks];
        }
    }
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style>