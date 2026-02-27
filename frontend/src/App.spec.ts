import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import App from './App.vue'

describe('App.vue', () => {
  it('debe renderizar el título correctamente', () => {
    const wrapper = mount(App)
    expect(wrapper.text()).toContain('Vercel & Render')
  })
})
