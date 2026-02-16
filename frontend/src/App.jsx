import { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
// index.css is imported in main.jsx by default

function App() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const runAnalysis = async () => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('/api/aep/run', {
        method: 'POST',
      })

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`)
      }

      const data = await response.json()
      setResult(data)

      // Optional: scroll to results
      setTimeout(() => {
        document.getElementById('results-section')?.scrollIntoView({ behavior: 'smooth' })
      }, 100)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  // Format distribution for Recharts
  const chartData = result?.distribution?.map((val, idx) => ({
    name: idx,
    value: val
  })) || []

  // Dynamic iteration count calculation
  const iterationCount = result?.distribution?.length || 0

  return (
    <div className="container">
      <header>
        {result && (
          <div className="badge">Monte Carlo Iterations: {iterationCount} (Optimized for demo stability)</div>
        )}
        {!result && (
          <div className="badge">OpenOA Demo Mode</div>
        )}
        <h1>OpenOA Monte Carlo AEP Demo</h1>
        <p className="subtitle">
          Estimate long-term Annual Energy Production (AEP) using the Monte Carlo method.
          <br />
          Demonstration using the "La Haute Borne" wind plant dataset.
        </p>
      </header>

      <main>
        <div className="action-area">
          <button
            onClick={runAnalysis}
            disabled={loading}
            className="run-btn"
          >
            {loading ? (
              <span className="btn-content">
                <span className="spinner-small"></span> Processing...
              </span>
            ) : 'Run Demo Analysis'}
          </button>
        </div>

        {error && (
          <div className="error-box">
            <strong>Analysis Failed</strong>
            <p>{error}</p>
          </div>
        )}

        {loading && !result && (
          <div className="loading-state">
            <p>Running simulations...</p>
            <p className="loading-hint">Processing ~13 months of SCADA data (Optimized for Demo Stability).</p>
          </div>
        )}

        {result && (
          <div id="results-section" className="fade-in results-container">
            <div className="metrics-grid">
              <div className="card">
                <h3>Mean AEP</h3>
                <div className="value">{result.aep_GWh_mean?.toFixed(2)} <span className="unit">GWh</span></div>
              </div>
              <div className="card">
                <h3>P50 AEP</h3>
                <div className="value">{result.aep_GWh_p50?.toFixed(2)} <span className="unit">GWh</span></div>
              </div>
              <div className="card">
                <h3>P90 AEP</h3>
                <div className="value">{result.aep_GWh_p90?.toFixed(2)} <span className="unit">GWh</span></div>
              </div>
              <div className="card">
                <h3>Uncertainty</h3>
                <div className="value">{result.uncertainty_pct?.toFixed(2)} <span className="unit">%</span></div>
              </div>
            </div>

            <div className="chart-container">
              <h3>AEP Distribution (GWh)</h3>
              <div style={{ width: '100%', height: 350 }}>
                <ResponsiveContainer>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#ffffff20" />
                    <XAxis hide />
                    <YAxis
                      label={{ value: 'Frequency', angle: -90, position: 'insideLeft', fill: '#888' }}
                      tick={{ fill: '#888' }}
                    />
                    <Tooltip
                      cursor={{ fill: '#ffffff10' }}
                      contentStyle={{ backgroundColor: '#333', borderColor: '#444', color: '#fff' }}
                      formatter={(value) => [value.toFixed(0), 'Frequency']}
                    />
                    <Bar dataKey="value" fill="#646cff" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <p className="chart-caption">
                Distribution of AEP values across {iterationCount} Monte Carlo simulations (Demo Mode).
              </p>
            </div>

            <div className="metrics-explanation">
              <h3>Understanding the Metrics</h3>
              <div className="explanation-grid">
                <div className="explanation-item">
                  <h4>Mean AEP (GWh)</h4>
                  <p>Average annual energy production across all Monte Carlo simulations.</p>
                </div>
                <div className="explanation-item">
                  <h4>P50 AEP</h4>
                  <p>Median expected annual production. There is a 50% probability actual production will exceed this value.</p>
                </div>
                <div className="explanation-item">
                  <h4>P90 AEP</h4>
                  <p>Conservative estimate. There is a 90% probability actual production will exceed this value.</p>
                </div>
                <div className="explanation-item">
                  <h4>Uncertainty (%)</h4>
                  <p>Relative variability of results, calculated as (standard deviation / mean × 100).</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      <footer>
        <p>Powered by <strong>OpenOA</strong> (NREL)</p>
        <p className="footer-note">Demo Dataset: La Haute Borne, France (2014-2015)</p>
      </footer>
    </div>
  )
}

export default App
