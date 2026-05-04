export default function NoticePlaceholder() {
  return (
    <div
      style={{
        marginTop: 12,
        padding: 24,
        background: 'var(--bg-card)',
        border: '1px dashed var(--border-light)',
        borderRadius: 'var(--radius)',
      }}
    >
      <div
        style={{
          textAlign: 'center',
          color: 'var(--text-muted)',
          fontSize: 13,
          marginBottom: 16,
        }}
      >
        🚧 크롤러 미연결 — 추후 Supabase에서 공지사항 데이터를 가져옵니다
      </div>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
          gap: 12,
        }}
      >
        {[0, 1, 2].map(i => (
          <div
            key={i}
            style={{
              padding: 14,
              background: 'var(--bg-hover)',
              borderRadius: 'var(--radius-sm)',
              opacity: 0.55,
            }}
          >
            <div
              style={{
                height: 12,
                width: '60%',
                background: 'var(--border-light)',
                borderRadius: 4,
                marginBottom: 8,
              }}
            />
            <div
              style={{
                height: 10,
                width: '90%',
                background: 'var(--border)',
                borderRadius: 4,
                marginBottom: 6,
              }}
            />
            <div
              style={{
                height: 10,
                width: '40%',
                background: 'var(--border)',
                borderRadius: 4,
              }}
            />
          </div>
        ))}
      </div>
    </div>
  )
}
