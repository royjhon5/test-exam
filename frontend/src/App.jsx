import { useEffect, useMemo, useState } from 'react'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'
const TENANTS = [
  { id: 'tenant-acme', label: 'Acme Corp' },
  { id: 'tenant-globex', label: 'Globex' },
]

function useAlerts(tenantId, page) {
  const [state, setState] = useState({ loading: true, error: '', data: null })

  useEffect(() => {
    let active = true
    setState((current) => ({ ...current, loading: true, error: '' }))

    fetch(`${API_BASE_URL}/api/alerts?page=${page}&page_size=50`, {
      headers: {
        'X-Tenant-Id': tenantId,
        'X-User-Role': 'analyst',
      },
    })
      .then(async (response) => {
        if (!response.ok) throw new Error(`Request failed with status ${response.status}`)
        return response.json()
      })
      .then((data) => {
        if (active) setState({ loading: false, error: '', data })
      })
      .catch((error) => {
        if (active) setState({ loading: false, error: error.message, data: null })
      })

    return () => {
      active = false
    }
  }, [tenantId, page])

  return state
}

function VirtualizedAlertList({ alerts, height = 420, rowHeight = 124 }) {
  const [scrollTop, setScrollTop] = useState(0)
  const totalHeight = alerts.length * rowHeight
  const startIndex = Math.max(0, Math.floor(scrollTop / rowHeight) - 2)
  const endIndex = Math.min(alerts.length, Math.ceil((scrollTop + height) / rowHeight) + 2)
  const visible = alerts.slice(startIndex, endIndex)

  return (
    <div className="virtual-list" style={{ height }} onScroll={(event) => setScrollTop(event.currentTarget.scrollTop)}>
      <div style={{ height: totalHeight, position: 'relative' }}>
        {visible.map((alert, index) => {
          const actualIndex = startIndex + index
          return (
            <article
              key={alert.id}
              className="alert-card"
              style={{ position: 'absolute', top: actualIndex * rowHeight, left: 0, right: 0, height: rowHeight - 12 }}
            >
              <div className="alert-header">
                <div>
                  <p className="eyebrow">{alert.source} · {alert.severity.toUpperCase()}</p>
                  <h3>{alert.title}</h3>
                </div>
                <span className={`badge badge-${alert.status}`}>{alert.status}</span>
              </div>
              <p>{alert.description}</p>
              <p className="summary">{alert.enrichment.summary}</p>
            </article>
          )
        })}
      </div>
    </div>
  )
}

export default function App() {
  const [tenantId, setTenantId] = useState(TENANTS[0].id)
  const [page, setPage] = useState(1)
  const { data, loading, error } = useAlerts(tenantId, page)

  const alerts = data?.items ?? []
  const metrics = useMemo(() => {
    return alerts.reduce(
      (accumulator, alert) => {
        accumulator.total += 1
        if (alert.enrichment.risk_score >= 80) accumulator.highRisk += 1
        return accumulator
      },
      { total: 0, highRisk: 0 },
    )
  }, [alerts])

  return (
    <main className="app-shell">
      <section className="hero">
        <div>
          <p className="eyebrow">Prototype dashboard</p>
          <h1>Multi-tenant Security Alerts</h1>
          <p>Tenant isolation is enforced via headers on the backend; enrichment is injected before payload delivery.</p>
        </div>
        <div className="controls">
          <label>
            Tenant
            <select value={tenantId} onChange={(event) => { setTenantId(event.target.value); setPage(1) }}>
              {TENANTS.map((tenant) => <option key={tenant.id} value={tenant.id}>{tenant.label}</option>)}
            </select>
          </label>
          <div className="pagination">
            <button onClick={() => setPage((value) => Math.max(1, value - 1))} disabled={page === 1}>Previous</button>
            <span>Page {data?.page ?? page} / {data?.total_pages ?? 1}</span>
            <button onClick={() => setPage((value) => value + 1)} disabled={Boolean(data && page >= data.total_pages)}>Next</button>
          </div>
        </div>
      </section>

      <section className="stats-grid">
        <article className="stat-card"><span>Total alerts</span><strong>{metrics.total}</strong></article>
        <article className="stat-card"><span>High risk</span><strong>{metrics.highRisk}</strong></article>
        <article className="stat-card"><span>Role</span><strong>{data?.role ?? 'analyst'}</strong></article>
      </section>

      {loading && <p>Loading alerts…</p>}
      {error && <p className="error">{error}</p>}
      {!loading && !error && <VirtualizedAlertList alerts={alerts} />}
    </main>
  )
}
