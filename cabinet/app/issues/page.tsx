"use client";

import { useEffect, useState } from "react";
import { api, getCurrentUser } from "@/lib/api";
import type { IssueSummary, Theme } from "@/lib/types";
import { Banner, Loading, Pill, errMsg } from "@/components/ui";

const TERMINAL = new Set(["rendered", "incomplete", "error", "delivered", "done"]);

export default function IssuesPage() {
  const [issues, setIssues] = useState<IssueSummary[]>([]);
  const [themes, setThemes] = useState<Theme[]>([]);
  const [theme, setTheme] = useState<string>("");
  const [lang, setLang] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [status, setStatus] = useState("");
  const [err, setErr] = useState("");

  async function refresh() {
    try {
      setIssues(await api.listIssues(getCurrentUser()));
    } catch (e) {
      setErr(errMsg(e));
    }
  }

  useEffect(() => {
    (async () => {
      try {
        const t = await api.getThemes();
        setThemes(t);
      } catch {
        /* ignore */
      }
      await refresh();
      setLoading(false);
    })();
  }, []);

  async function generate() {
    setRunning(true);
    setErr("");
    setStatus("Постановка задачи…");
    try {
      const job = await api.createIssue(getCurrentUser(), {
        theme_id: theme || null,
        output_lang: lang || null,
      });
      const id = job.issue_id || job.job_id;
      // Poll until the build reaches a terminal state.
      for (let i = 0; i < 40; i++) {
        const st = await api.getIssue(id);
        setStatus(`Выпуск ${id.slice(0, 14)}: ${st.status}`);
        if (TERMINAL.has(st.status)) break;
        await new Promise((r) => setTimeout(r, 1500));
      }
      await refresh();
    } catch (e) {
      setErr(errMsg(e));
      setStatus("");
    }
    setRunning(false);
  }

  if (loading) return <Loading />;

  return (
    <>
      <h1 className="page-title">Выпуски</h1>
      <p className="page-sub">Соберите выпуск сейчас или посмотрите историю. PDF доступен по ссылке.</p>
      <Banner kind="err">{err}</Banner>

      <div className="card" style={{ marginBottom: 20 }}>
        <h3>Собрать выпуск</h3>
        <div className="row" style={{ alignItems: "flex-end" }}>
          <div className="field" style={{ marginBottom: 0, minWidth: 220 }}>
            <label>Стиль (по умолчанию — из настроек)</label>
            <select value={theme} onChange={(e) => setTheme(e.target.value)}>
              <option value="">— по умолчанию —</option>
              {themes.map((t) => (
                <option key={t.id} value={t.id}>{t.display_name}</option>
              ))}
            </select>
          </div>
          <div className="field" style={{ marginBottom: 0, width: 120 }}>
            <label>Язык</label>
            <input value={lang} onChange={(e) => setLang(e.target.value)} placeholder="ru" />
          </div>
          <button className="btn" onClick={generate} disabled={running}>
            {running ? "Сборка…" : "Собрать"}
          </button>
        </div>
        {status ? <p className="muted" style={{ marginTop: 12 }}>{status}</p> : null}
      </div>

      <div className="card">
        <h3>История</h3>
        {issues.length ? (
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
            <thead>
              <tr style={{ textAlign: "left", color: "var(--muted)" }}>
                <th style={{ padding: "6px 4px" }}>ID</th>
                <th>Стиль</th>
                <th>Статус</th>
                <th>Создан</th>
                <th>PDF</th>
              </tr>
            </thead>
            <tbody>
              {issues.map((i) => (
                <tr key={i.id} style={{ borderTop: "1px solid var(--line)" }}>
                  <td style={{ padding: "8px 4px", fontFamily: "ui-monospace, monospace" }}>{i.id}</td>
                  <td>{i.theme_id ?? "—"}</td>
                  <td><Pill status={i.status} /></td>
                  <td>{i.created_at ? new Date(i.created_at).toLocaleString() : "—"}</td>
                  <td>
                    <a href={`/api/v1/issues/${encodeURIComponent(i.id)}/pdf`} target="_blank" rel="noreferrer">
                      скачать
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="empty">
            Пока нет выпусков. История наполняется при включённом слое БД (init-db).
          </p>
        )}
      </div>
    </>
  );
}
