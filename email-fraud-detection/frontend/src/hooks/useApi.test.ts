import { beforeEach, describe, expect, it, vi } from 'vitest'
import { useApi } from './useApi'

describe('useApi', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn())
    vi.stubGlobal('localStorage', {
      getItem: vi.fn(() => 'token'),
      setItem: vi.fn(),
      removeItem: vi.fn(),
    })
  })

  it('calls login endpoint and returns token', async () => {
    const fakeResponse = { access_token: 'abc', token_type: 'bearer', expires_at: '2026-01-01T00:00:00Z' }
    global.fetch = vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve(fakeResponse) })) as any
    const api = useApi()

    const result = await api.login('user@example.com', 'password')

    expect(result).toEqual(fakeResponse)
    expect(global.fetch).toHaveBeenCalled()
  })
})
