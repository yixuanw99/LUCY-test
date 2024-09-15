<template>
  <div class="overflow-x-auto">
    <table class="min-w-full bg-white border border-gray-300">
      <thead>
        <tr class="bg-gray-100">
          <th class="py-2 px-4 border-b text-left">疾病風險</th>
          <th class="py-2 px-4 border-b text-left">基礎風險(horvath)(%)</th>
          <th class="py-2 px-4 border-b text-left">當前風險(pace)(%)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="risk in risks" :key="risk.name" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b">{{ risk.name }}</td>
          <td class="py-2 px-4 border-b">{{ risk.relative }}</td>
          <td class="py-2 px-4 border-b">{{ risk.absolute }}</td>
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
      { name: '全因死亡率', relative: props.diseaseRisks[0].acmHorvathRisk, absolute: props.diseaseRisks[1].acmPaceRisk },
      { name: '心血管疾病', relative: props.diseaseRisks[0].cvdHorvathRisk, absolute: props.diseaseRisks[1].cvdPaceRisk },
      { name: '糖尿病風險', relative: props.diseaseRisks[0].dmHorvathRisk, absolute: props.diseaseRisks[1].dmPaceRisk },
      { name: '失智風險', relative: props.diseaseRisks[0].adHorvathRisk, absolute: props.diseaseRisks[1].adPaceRisk },
      { name: '癌症風險', relative: props.diseaseRisks[0].cancerHorvathRisk, absolute: props.diseaseRisks[1].cancerPaceRisk }
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
  text-align: left;
}
thead {
  background-color: #f8fafc;
}
</style>
