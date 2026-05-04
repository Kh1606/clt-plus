import { useEffect, useState } from 'react'
import { ExternalLink } from 'lucide-react'
import { supabase } from '../lib/supabase.js'
import NoticePlaceholder from './NoticePlaceholder.jsx'

export default function NoticeList({ region, subEntity }) {
  const [state, setState] = useState({ status: 'loading', items: [], error: null })

  useEffect(() => {
    let cancelled = false
    setState({ status: 'loading', items: [], error: null })

    supabase
      .from('notices')
      .select('notice_id,title,detail_url,posted_at,source_page,scraped_at')
      .eq('region', region)
      .eq('sub_entity', subEntity)
      .order('posted_at', { ascending: false, nullsFirst: false })
      .limit(50)
      .then(({ data, error }) => {
        if (cancelled) return
        if (error) setState({ status: 'error', items: [], error: error.message })
        else setState({ status: 'ok', items: data || [], error: null })
      })

    return () => {
      cancelled = true
    }
  }, [region, subEntity])

  if (state.status === 'loading') {
    return (
      <div style={{ padding: 24, color: 'var(--text-muted)', fontSize: 13 }}>
        불러오는 중…
      </div>
    )
  }

  if (state.status === 'error') {
    return (
      <div
        style={{
          padding: 16,
          background: 'var(--danger-bg, #FEF2F2)',
          color: 'var(--danger)',
          border: '1px solid var(--danger)',
          borderRadius: 'var(--radius)',
          fontSize: 13,
        }}
      >
        Supabase 연결 오류: {state.error}
      </div>
    )
  }

  if (state.items.length === 0) {
    return <NoticePlaceholder />
  }

  return (
    <div
      style={{
        marginTop: 12,
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))',
        gap: 12,
      }}
    >
      {state.items.map(n => (
        <a
          key={n.notice_id}
          href={n.detail_url}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 8,
            padding: 14,
            background: 'var(--bg-card)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius)',
            boxShadow: 'var(--shadow-sm)',
            transition: 'transform 0.15s ease, border-color 0.15s',
          }}
          onMouseEnter={e => {
            e.currentTarget.style.transform = 'translateY(-2px)'
            e.currentTarget.style.borderColor = 'var(--accent)'
          }}
          onMouseLeave={e => {
            e.currentTarget.style.transform = 'translateY(0)'
            e.currentTarget.style.borderColor = 'var(--border)'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', gap: 8 }}>
            <span
              style={{
                fontSize: 11,
                fontWeight: 600,
                color: 'var(--accent)',
                background: 'var(--accent-light)',
                padding: '2px 8px',
                borderRadius: 999,
                whiteSpace: 'nowrap',
              }}
            >
              {n.source_page}
            </span>
            <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>
              {n.posted_at || '날짜 없음'}
            </span>
          </div>
          <div
            className="line-clamp-2"
            style={{
              fontSize: 14,
              fontWeight: 500,
              color: 'var(--text-primary)',
              lineHeight: 1.4,
            }}
          >
            {n.title}
          </div>
          <div
            style={{
              fontSize: 12,
              color: 'var(--accent)',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              gap: 4,
              marginTop: 'auto',
            }}
          >
            원문 보기 <ExternalLink size={12} />
          </div>
        </a>
      ))}
    </div>
  )
}
