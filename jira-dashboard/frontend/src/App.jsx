function App() {
  return (
    <main className="page-shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="Sprintboard home">
          <span className="brand-mark" aria-hidden="true">
            S
          </span>
          <span>Sprintboard</span>
        </a>
        <span className="prototype-label">Prototype</span>
      </header>

      <section className="hero" aria-labelledby="page-title">
        <div className="hero-copy">
          <p className="eyebrow">
            <span className="status-dot" aria-hidden="true" />
            Local preview
          </p>
          <h1 id="page-title">Jira Sprint Dashboard</h1>
          <p className="intro">
            A starting point for a clearer view of sprint work. This prototype
            is not connected to Jira and does not display Jira data.
          </p>
        </div>

        <aside className="notice" role="note" aria-labelledby="notice-title">
          <span className="notice-icon" aria-hidden="true">
            i
          </span>
          <div>
            <h2 id="notice-title">Mock-only preview</h2>
            <p>
              No Jira connection, account access, or sprint data is active.
              Nothing here represents current project information.
            </p>
          </div>
        </aside>
      </section>

      <footer className="page-footer">
        <span>Dashboard prototype</span>
        <span className="footer-divider" aria-hidden="true">
          /
        </span>
        <span>Local preview only</span>
      </footer>
    </main>
  );
}

export default App;