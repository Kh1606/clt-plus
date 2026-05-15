import { useEffect, useState } from 'react'
import { animated, useSpring } from '@react-spring/web'
import { X } from 'lucide-react'
import NoticeList from '../NoticeList.jsx'
import InstitutionPicker from './InstitutionPicker.jsx'

export default function RegionPanel({
  open,
  region,
  subEntities,
  municipalityHint,
  onClose,
}) {
  const [selectedSub, setSelectedSub] = useState(null)

  // Reset institution selection whenever the region changes.
  useEffect(() => {
    setSelectedSub(subEntities?.[0]?.name ?? null)
  }, [region, subEntities])

  const spring = useSpring({
    transform: open ? 'translateY(0%)' : 'translateY(100%)',
    opacity: open ? 1 : 0,
    config: { tension: 280, friction: 28 },
  })

  return (
    <animated.div
      style={{
        ...spring,
        position: 'absolute',
        left: 0,
        right: 0,
        bottom: 0,
        height: '45%',
        background: 'var(--bg-card)',
        borderTop: '1px solid var(--border)',
        borderTopLeftRadius: 'var(--radius)',
        borderTopRightRadius: 'var(--radius)',
        boxShadow: '0 -8px 32px rgba(13,27,110,0.15)',
        padding: '16px 20px',
        display: 'flex',
        flexDirection: 'column',
        gap: 12,
        zIndex: 30,
        pointerEvents: open ? 'auto' : 'none',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <div style={{ minWidth: 0, flex: 1 }}>
          <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>
            지역 선택
          </div>
          <div
            style={{
              fontSize: 18,
              fontWeight: 700,
              color: 'var(--text-primary)',
              display: 'flex',
              alignItems: 'baseline',
              gap: 8,
            }}
          >
            {region ?? '—'}
            {municipalityHint && (
              <span
                style={{
                  fontSize: 12,
                  fontWeight: 500,
                  color: 'var(--accent)',
                  background: 'var(--accent-light)',
                  padding: '2px 8px',
                  borderRadius: 999,
                }}
              >
                {municipalityHint} · 행정구별 분류는 곧 지원 예정
              </span>
            )}
          </div>
        </div>
        <button
          onClick={onClose}
          aria-label="닫기"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: 32,
            height: 32,
            borderRadius: 999,
            background: 'var(--bg-hover)',
            color: 'var(--text-secondary)',
          }}
        >
          <X size={16} />
        </button>
      </div>

      <InstitutionPicker
        subEntities={subEntities}
        selectedName={selectedSub}
        onSelect={setSelectedSub}
      />

      <div style={{ flex: 1, minHeight: 0, overflow: 'auto' }}>
        {region && selectedSub && (
          <NoticeList region={region} subEntity={selectedSub} />
        )}
      </div>
    </animated.div>
  )
}
