import { useState } from 'react'
import { ChevronDown, ChevronRight } from 'lucide-react'

export default function RegionSidebar({ regions, selected, onSelect }) {
  const [expanded, setExpanded] = useState(() => new Set([selected?.region]))

  const toggle = region => {
    setExpanded(prev => {
      const next = new Set(prev)
      next.has(region) ? next.delete(region) : next.add(region)
      return next
    })
  }

  return (
    <aside
      style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border)',
        borderRadius: 'var(--radius)',
        boxShadow: 'var(--shadow-sm)',
        padding: 12,
        height: 'fit-content',
        maxHeight: 'calc(100vh - 140px)',
        overflowY: 'auto',
        position: 'sticky',
        top: 24,
      }}
    >
      <div
        style={{
          fontSize: 12,
          fontWeight: 600,
          color: 'var(--text-muted)',
          textTransform: 'uppercase',
          letterSpacing: 0.5,
          padding: '4px 8px 8px',
        }}
      >
        지역 · 기관 ({regions.length})
      </div>
      <ul style={{ listStyle: 'none' }}>
        {regions.map(r => {
          const isOpen = expanded.has(r.region)
          return (
            <li key={r.region}>
              <button
                onClick={() => toggle(r.region)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  width: '100%',
                  padding: '8px 8px',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: 14,
                  fontWeight: 600,
                  color: 'var(--text-primary)',
                  textAlign: 'left',
                }}
                onMouseEnter={e =>
                  (e.currentTarget.style.background = 'var(--bg-hover)')
                }
                onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}
              >
                {isOpen ? (
                  <ChevronDown size={16} style={{ marginRight: 6, flexShrink: 0 }} />
                ) : (
                  <ChevronRight size={16} style={{ marginRight: 6, flexShrink: 0 }} />
                )}
                <span style={{ flex: 1 }}>{r.region}</span>
                <span style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 500 }}>
                  {r.subEntities.length}
                </span>
              </button>
              {isOpen && (
                <ul style={{ listStyle: 'none', paddingLeft: 22, marginTop: 2 }}>
                  {r.subEntities.map(s => {
                    const isActive =
                      selected?.region === r.region && selected?.sub === s.name
                    return (
                      <li key={s.name}>
                        <button
                          onClick={() => onSelect({ region: r.region, sub: s.name })}
                          style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            width: '100%',
                            padding: '6px 10px',
                            borderRadius: 'var(--radius-sm)',
                            fontSize: 13,
                            color: isActive ? 'var(--accent-text)' : 'var(--text-secondary)',
                            background: isActive ? 'var(--accent)' : 'transparent',
                            fontWeight: isActive ? 600 : 400,
                            textAlign: 'left',
                          }}
                          onMouseEnter={e => {
                            if (!isActive)
                              e.currentTarget.style.background = 'var(--bg-hover)'
                          }}
                          onMouseLeave={e => {
                            if (!isActive) e.currentTarget.style.background = 'transparent'
                          }}
                        >
                          <span>{s.name}</span>
                          <span
                            style={{
                              fontSize: 11,
                              opacity: 0.7,
                              fontWeight: 500,
                            }}
                          >
                            {s.sources.length}
                          </span>
                        </button>
                      </li>
                    )
                  })}
                </ul>
              )}
            </li>
          )
        })}
      </ul>
    </aside>
  )
}
