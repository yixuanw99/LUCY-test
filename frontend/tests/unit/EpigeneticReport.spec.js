// frontend/tests/unit/EpigeneticReport.spec.js
import { shallowMount } from '@vue/test-utils'
import EpigeneticReport from '@/views/EpigeneticReport.vue'

describe('EpigeneticReport.vue', () => {
  it('renders properly', () => {
    const wrapper = shallowMount(EpigeneticReport)
    expect(wrapper.text()).toMatch('Epigenetic Report')
  })

  // Add more tests as needed
})