import { writeFile, mkdir } from 'node:fs/promises'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const outDir = resolve(__dirname, '..', 'public', 'data')

const SOURCES = [
  {
    url: 'https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2018/json/skorea-provinces-2018-topo-simple.json',
    out: 'skorea-provinces-topo.json',
  },
  {
    url: 'https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2018/json/skorea-municipalities-2018-topo-simple.json',
    out: 'skorea-municipalities-topo.json',
  },
]

await mkdir(outDir, { recursive: true })

for (const { url, out } of SOURCES) {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`${url} → ${res.status}`)
  const text = await res.text()
  const path = resolve(outDir, out)
  await writeFile(path, text)
  console.log(`✓ ${out}  ${(text.length / 1024).toFixed(0)} KB`)
}
