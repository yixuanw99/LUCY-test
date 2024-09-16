<template>
  <div class="overflow-x-auto">
    <table class="min-w-full bg-white border border-gray-300">
      <thead>
        <tr class="bg-gray-100">
          <th class="py-2 px-4 border-b">疾病風險</th>
          <th class="py-2 px-4 border-b column-name">當前DunedinPACE風險</th>
          <th class="py-2 px-4 border-b column-name">若DunedinPACE減少0.05時風險</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="risk in risks" :key="risk.name" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b row-name">{{ risk.name }}</td>
          <td class="py-2 px-4 border-b content">{{ risk.current }} %</td>
          <td class="py-2 px-4 border-b content">{{ risk.reduced01 }} %</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'DiseaseRisksTable',
  props: {
    diseaseRisks: {
      type: Array,
      required: true
    }
  },
  setup (props) {
    const risks = computed(() => [
      { name: '全因死亡率', current: props.diseaseRisks[0].acmPaceRisk, reduced01: props.diseaseRisks[1].acmPaceRiskReduced01 },
      { name: '心血管疾病', current: props.diseaseRisks[0].cvdPaceRisk, reduced01: props.diseaseRisks[1].cvdPaceRiskReduced01 },
      { name: '糖尿病風險', current: props.diseaseRisks[0].dmPaceRisk, reduced01: props.diseaseRisks[1].dmPaceRiskReduced01 },
      { name: '失智風險', current: props.diseaseRisks[0].adPaceRisk, reduced01: props.diseaseRisks[1].adPaceRiskReduced01 },
      { name: '癌症風險', current: props.diseaseRisks[0].cancerPaceRisk, reduced01: props.diseaseRisks[1].cancerPaceRiskReduced01 }
    ])

    return { risks }
  }
}
</script>

<style scoped>
.overflow-x-auto {
  overflow-x: auto;
}
table {
  border-collapse: collapse;
  width: 100%;
}
th, td {
  border: 1px solid #e2e8f0;
  padding: 0.5rem 1rem;
}
.column-name {
  text-align: center;
  font-weight: bold;
  background-color: #f8fafc;
}
.row-name {
  text-align: left;
  font-weight: bold;
}
.content {
  text-align: center;
}
thead {
  background-color: #f8fafc;
}
</style>
