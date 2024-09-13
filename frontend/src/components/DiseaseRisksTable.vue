<template>
    <div class="overflow-x-auto">
      <table class="min-w-full bg-white border border-gray-300">
        <thead>
          <tr class="bg-gray-100">
            <th class="py-2 px-4 border-b text-left">疾病風險</th>
            <th class="py-2 px-4 border-b text-left">與同齡相比的風險程度(%)</th>
            <th class="py-2 px-4 border-b text-left">生物年齡每年輕1年可降低風險(%)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(risk, index) in risks" :key="index" class="hover:bg-gray-50">
            <td class="py-2 px-4 border-b">{{ risk.name }}</td>
            <td class="py-2 px-4 border-b">{{ risk.relative }}</td>
            <td class="py-2 px-4 border-b">{{ risk.absolute }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DiseaseRisksTable',
    props: {
      diseaseRisks: {
        type: Array,
        required: true
      }
    },
    computed: {
      risks() {
        return [
          { name: '全因死亡率', relative: this.diseaseRisks[0].acmHorvathRisk, absolute: this.diseaseRisks[1].acmPaceRisk },
          { name: '心血管疾病', relative: this.diseaseRisks[0].cvdHorvathRisk, absolute: this.diseaseRisks[1].cvdPaceRisk },
          { name: '糖尿病風險', relative: this.diseaseRisks[0].dmHorvathRisk, absolute: this.diseaseRisks[1].dmPaceRisk },
          { name: '失智風險', relative: this.diseaseRisks[0].adHorvathRisk, absolute: this.diseaseRisks[1].adPaceRisk },
          { name: '癌症風險', relative: this.diseaseRisks[0].cancerHorvathRisk, absolute: this.diseaseRisks[1].cancerPaceRisk }
        ];
      }
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
  /* tr:hover {
  background-color: #f1f5f9;
  } */
  </style>