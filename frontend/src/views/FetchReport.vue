<template>
<div class="fetch-report">
    <h1>獲取樂稀表觀檢測報告</h1>
    <div class="input-section">
    <input v-model="inputSampleId" placeholder="輸入樣本ID" />
    <button @click="fetchReport">獲取報告</button>
    </div>
</div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'FetchReport',
  setup () {
    const inputSampleId = ref('')
    const router = useRouter()

    const fetchReport = async () => {
      if (process.env.NODE_ENV === 'production') {
        try {
          const response = await fetch(process.env.BASE_URL + 'mockdata/mock-data.json')
          const mockData = await response.json()
          const reportIndex = mockData.reports.findIndex(r => r.sample_id === inputSampleId.value)

          if (reportIndex !== -1) {
            localStorage.setItem('reportData', JSON.stringify(mockData.reports[reportIndex]))
            router.push({ name: 'ReportDisplay', params: { id: inputSampleId.value } })
          } else {
            alert('無法找到匹配的報告，請檢查樣本ID是否正確。')
          }
        } catch (error) {
          console.error('Error fetching mock report:', error)
          alert('無法獲取報告，請稍後再試。')
        }
      } else {
        try {
          // 在開發環境中，使用實際的API
          const response = await axios.get(`http://127.0.0.1:8000/report/${inputSampleId.value}`)
          // 假設我們將報告數據存儲在 localStorage 中
          localStorage.setItem('reportData', JSON.stringify(response.data))
          // 導航到報告顯示頁面
          router.push({ name: 'ReportDisplay', params: { id: inputSampleId.value } })
        } catch (error) {
          console.error('Error fetching report:', error)
          alert('無法獲取報告，請檢查樣本ID是否正確。')
        }
      }
    }

    return {
      inputSampleId,
      fetchReport
    }
  }
}
</script>

<style scoped>
.fetch-report {
display: flex;
flex-direction: column;
align-items: center;
padding: 20px;
}

.input-section {
margin: 20px 0;
display: flex;
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
</style>
