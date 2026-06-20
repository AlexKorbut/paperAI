"use client";

import { useEffect, useState } from "react";
import { api, getCurrentUser } from "@/lib/api";
import type { Theme } from "@/lib/types";
import { Banner, Loading, errMsg } from "@/components/ui";

export default function ThemesPage() {
  const [themes, setThemes] = useState<Theme[]>([]);
  const [current, setCurrent] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState<string>("");
  const [ok, setOk] = useState("");
  const [err, setErr] = useState("");

  useEffect(() => {
    const uid = getCurrentUser();
    (async () => {
      try {
        const [t, u] = await Promise.all([api.getThemes(), api.getUser(uid)]);
        setThemes(t);
        setCurrent(u.theme);
      } catch (e) {
        setErr(errMsg(e));
      }
      setLoading(false);
    })();
  }, []);

  async function choose(id: string) {
    setBusy(id);
    setOk("");
    setErr("");
    try {
      const u = await api.updateUser(getCurrentUser(), { theme: id });
      setCurrent(u.theme);
      setOk(`Стиль выпуска: ${id}`);
    } catch (e) {
      setErr(errMsg(e));
    }
    setBusy("");
  }

  if (loading) return <Loading />;

  return (
    <>
      <h1 className="page-title">Стили газеты</h1>
      <p className="page-sub">Выберите типографский стиль, в котором будет верстаться ваш выпуск.</p>
      <Banner kind="ok">{ok}</Banner>
      <Banner kind="err">{err}</Banner>

      <div className="grid cols-3">
        {themes.map((t) => (
          <div className={`card theme-card ${t.id === current ? "selected" : ""}`} key={t.id}>
            <div className="row" style={{ justifyContent: "space-between" }}>
              <h3 style={{ margin: 0 }}>{t.display_name}</h3>
              {t.id === current ? <span className="pill ok">текущий</span> : null}
            </div>
            <p className="muted" style={{ minHeight: 40 }}>{t.mood}</p>
            <div className="swatches" aria-hidden>
              <span className="swatch" style={{ background: t.colors.paper }} title="paper" />
              <span className="swatch" style={{ background: t.colors.ink }} title="ink" />
              <span className="swatch" style={{ background: t.colors.accent }} title="accent" />
            </div>
            <div className="kv"><span className="k">формат</span><span>{t.page} · {t.columns} колонок · {t.color_mode}</span></div>
            <button
              className="btn small secondary"
              style={{ marginTop: 12 }}
              disabled={busy === t.id || t.id === current}
              onClick={() => choose(t.id)}
            >
              {t.id === current ? "выбран" : busy === t.id ? "…" : "Использовать"}
            </button>
          </div>
        ))}
      </div>
    </>
  );
}
