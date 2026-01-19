// ===============================
// FILE: pages/index.js
// ===============================
import Head from 'next/head'
import { useState } from 'react'

// 🔗 YOUR LIVE FLASK API (VERCEL)
// Example hit: https://akash-vehicle-info-api.vercel.app/?rc=AS01BB1209&key=yourkey
const API_BASE = 'https://akash-vehicle-info-api.vercel.app/'

export default function Home() {
  const [rc, setRc] = useState('')
  const [key, setKey] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [data, setData] = useState(null)

  // 💰 PRICE SYSTEM
  const [days, setDays] = useState(1)
  const prices = { 1: 10, 7: 50, 30: 200 }

  const endpoint = `${API_BASE}?rc=${encodeURIComponent(rc)}&key=${encodeURIComponent(key)}`

  const fetchData = async () => {
    if (!rc || !key) {
      alert('RC Number aur API Key dono daalo!')
      return
    }
    setLoading(true)
    setError('')
    setData(null)
    try {
      const res = await fetch(endpoint)
      const json = await res.json()
      if (!res.ok) throw new Error(json?.error || 'Request Failed')
      setData(json)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={page}>
      <Head>
        <title>AKASHHACKER | VEHICLE RC API</title>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet" />
      </Head>

      <main style={card}>
        <h1 style={title}>🚗 VEHICLE RC INFORMATION SYSTEM</h1>
        <p style={subtitle}>POWERED BY <b>@AKASHHACKER</b></p>

        {/* INPUTS */}
        <div style={inputWrap}>
          <input
            placeholder="ENTER VEHICLE RC NUMBER"
            value={rc}
            onChange={(e) => setRc(e.target.value.toUpperCase())}
            style={input}
          />
          <input
            placeholder="ENTER API KEY"
            value={key}
            onChange={(e) => setKey(e.target.value)}
            style={input}
          />
        </div>

        {/* STATUS */}
        <div style={statusBox}>
          <p>📡 <b>API STATUS:</b> <span style={{ color: '#00ff41' }}>OPERATIONAL</span></p>
          <p>🔗 <b>ENDPOINT:</b></p>
          <code style={code}>{rc && key ? endpoint : `${API_BASE}?rc=AS01BB1209&key=YOURKEY`}</code>
        </div>

        {/* ACTION */}
        <button onClick={fetchData} disabled={!rc || !key || loading} style={button(rc && key)}>
          {loading ? 'FETCHING DATA…' : 'EXECUTE RC QUERY'}
        </button>

        {/* ERROR */}
        {error && <div style={errorBox}>❌ {error}</div>}

        {/* RESULT */}
        {data && (
          <div style={resultBox}>
            <h3>📄 API RESPONSE</h3>
            <pre style={json}>{JSON.stringify(data, null, 2)}</pre>
          </div>
        )}

        {/* PRICING */}
        <div style={pricing}>
          <h2>🔑 GET API ACCESS</h2>
          <select value={days} onChange={(e) => setDays(Number(e.target.value))} style={select}>
            <option value={1}>1 Day Access</option>
            <option value={7}>7 Days Access</option>
            <option value={30}>30 Days Access</option>
          </select>
          <p style={{ marginTop: 10 }}>💰 Price: <b>₹{prices[days]}</b></p>
          <a
            href={`https://t.me/AkashExploits1?text=Hi%20I%20want%20Vehicle%20RC%20API%20Key%20for%20${days}%20days.%20Price:%20₹${prices[days]}`}
            target="_blank"
            rel="noreferrer"
            style={buyBtn}
          >
            🚀 GENERATE API KEY
          </a>
        </div>
      </main>

      <footer style={footer}>© 2026 AKASHHACKER • VEHICLE DATA TERMINAL</footer>
    </div>
  )
}

// ===============================
// STYLES
// ===============================
const page = {
  backgroundColor: '#050505',
  color: '#00d4ff',
  minHeight: '100vh',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  fontFamily: 'Orbitron, sans-serif',
  padding: 20
}

const card = {
  maxWidth: 900,
  width: '100%',
  padding: 40,
  borderRadius: 20,
  border: '1px solid #00d4ff',
  background: 'rgba(0,212,255,.02)',
  boxShadow: '0 0 30px rgba(0,212,255,.3)',
  textAlign: 'center'
}

const title = { fontSize: '2.2rem', letterSpacing: 2 }
const subtitle = { color: '#aaa', marginBottom: 30 }

const inputWrap = { display: 'flex', flexDirection: 'column', gap: 14 }

const input = {
  padding: 12,
  borderRadius: 8,
  border: '1px solid #00d4ff',
  backgroundColor: '#111',
  color: '#00d4ff',
  textAlign: 'center'
}

const statusBox = {
  marginTop: 20,
  padding: 16,
  backgroundColor: '#111',
  borderRadius: 10,
  borderLeft: '4px solid #00d4ff',
  textAlign: 'left'
}

const code = { color: '#00d4ff', wordBreak: 'break-all' }

const button = (active) => ({
  marginTop: 20,
  padding: '12px 30px',
  borderRadius: 50,
  backgroundColor: active ? '#00d4ff' : '#555',
  color: '#000',
  fontWeight: 'bold',
  border: 'none',
  cursor: active ? 'pointer' : 'not-allowed'
})

const errorBox = {
  marginTop: 16,
  padding: 12,
  borderRadius: 10,
  backgroundColor: '#220000',
  color: '#ffb3b3',
  border: '1px solid #ff4d4f'
}

const resultBox = {
  marginTop: 20,
  padding: 20,
  backgroundColor: '#0b0b0b',
  borderRadius: 18,
  border: '1px dashed #00d4ff',
  textAlign: 'left'
}

const json = {
  maxHeight: 380,
  overflow: 'auto',
  background: '#000',
  padding: 16,
  borderRadius: 10,
  color: '#7CFFCB'
}

const pricing = {
  marginTop: 30,
  padding: 24,
  borderRadius: 18,
  border: '1px dashed #00d4ff',
  backgroundColor: '#0b0b0b'
}

const select = {
  width: '100%',
  padding: 12,
  borderRadius: 8,
  backgroundColor: '#111',
  color: '#00d4ff',
  border: '1px solid #00d4ff'
}

const buyBtn = {
  display: 'inline-block',
  marginTop: 16,
  padding: '14px 40px',
  borderRadius: 50,
  backgroundColor: '#00d4ff',
  color: '#000',
  fontWeight: 'bold',
  textDecoration: 'none'
}

const footer = { marginTop: 24, fontSize: '0.7rem', color: '#555' }
