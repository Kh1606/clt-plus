import { Building2 } from 'lucide-react'

export default function InstitutionPicker({ subEntities, selectedName, onSelect }) {
  if (!subEntities?.length) {
    return (
      <div style={{ fontSize: 13, color: 'var(--text-muted)' }}>
        등록된 기관이 없습니다
      </div>
    )
  }

  return (
    <div
      style={{
        display: 'flex',
        gap: 8,
        overflowX: 'auto',
        paddingBottom: 4,
      }}
    >
      {subEntities.map(sub => {
        const active = sub.name === selectedName
        return (
          <button
            key={sub.name}
            onClick={() => onSelect(sub.name)}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 6,
              padding: '8px 14px',
              background: active ? 'var(--accent)' : 'var(--bg-card)',
              color: active ? '#fff' : 'var(--text-primary)',
              border: `1px solid ${active ? 'var(--accent)' : 'var(--border)'}`,
              borderRadius: 999,
              fontSize: 13,
              fontWeight: 500,
              whiteSpace: 'nowrap',
              transition: 'background 0.15s ease, border-color 0.15s ease, color 0.15s ease',
              flexShrink: 0,
            }}
          >
            <Building2 size={13} />
            {sub.name}
          </button>
        )
      })}
    </div>
  )
}
