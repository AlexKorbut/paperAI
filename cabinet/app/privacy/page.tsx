"use client";

import { useState } from "react";
import { api, getCurrentUser } from "@/lib/api";
import { Banner, errMsg } from "@/components/ui";

export default function PrivacyPage() {
  const [data, setData] = useState<Record<string, unknown> | null>(null);
  const [ok, setOk] = useState("");
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);

  async function doExport() {
    setBusy(true);
    setErr("");
    setOk("");
    try {
      const d = await api.exportData(getCurrentUser());
      setData(d);
      setOk("Данные выгружены ниже.");
    } catch (e) {
      setErr(errMsg(e));
    }
    setBusy(false);
  }

  function download() {
    if (!data) return;
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${getCurrentUser()}-data.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  async function doDelete() {
    if (!window.confirm(`Удалить ВСЕ данные пользователя «${getCurrentUser()}»? Это необратимо.`)) return;
    setBusy(true);
    setErr("");
    setOk("");
    try {
      const res = await api.deleteData(getCurrentUser());
      setData(null);
      setOk(`Удалено: ${JSON.stringify((res as { removed?: unknown }).removed ?? res)}`);
    } catch (e) {
      setErr(errMsg(e));
    }
    setBusy(false);
  }

  return (
    <>
      <h1 className="page-title">Приватность и данные</h1>
      <p className="page-sub">
        Экспорт и удаление по запросу (GDPR/CCPA). Секреты (сессии, токены) в экспорт не попадают.
      </p>
      <Banner kind="ok">{ok}</Banner>
      <Banner kind="err">{err}</Banner>

      <div className="card" style={{ marginBottom: 18 }}>
        <h3>Экспорт данных</h3>
        <p className="muted">Настройки, источники (без секретов), профиль, обратная связь, выпуски.</p>
        <div className="row">
          <button className="btn" onClick={doExport} disabled={busy}>Выгрузить</button>
          {data ? <button className="btn secondary" onClick={download}>Скачать JSON</button> : null}
        </div>
      </div>

      <div className="card" style={{ marginBottom: 18, borderColor: "#f0c9c6" }}>
        <h3>Удаление данных</h3>
        <p className="muted">Стирает аккаунт, источники, профиль, сигналы и обратную связь. Необратимо.</p>
        <button className="btn danger" onClick={doDelete} disabled={busy}>Удалить все данные</button>
      </div>

      {data ? <pre className="json">{JSON.stringify(data, null, 2)}</pre> : null}
    </>
  );
}
