"use client";

import { useEffect, useMemo, useState } from "react";
import { api, getCurrentUser } from "@/lib/api";
import type { Theme } from "@/lib/types";
import { Banner, Loading, errMsg } from "@/components/ui";

const FONTS = [
  ["", "— шрифт темы —"],
  ["Georgia", "Georgia (serif)"],
  ["Times New Roman", "Times New Roman"],
  ["PT Serif", "PT Serif"],
  ["Vollkorn", "Vollkorn"],
  ["system-ui", "Системный sans"],
] as const;

export default function TypographyPage() {
  const [themes, setThemes] = useState<Theme[]>([]);
  const [theme, setTheme] = useState("");
  const [scale, setScale] = useState(1);
  const [leading, setLeading] = useState(1.45);
  const [accent, setAccent] = useState("#7a1f1f");
  const [dropcap, setDropcap] = useState(true);
  const [bodyFont, setBodyFont] = useState("");
  const [headlineFont, setHeadlineFont] = useState("");
  const [loading, setLoading] = useState(true);
  const [ok, setOk] = useState("");
  const [err, setErr] = useState("");
  const [previewUrl, setPreviewUrl] = useState("");

  useEffect(() => {
    const uid = getCurrentUser();
    (async () => {
      try {
        const [ts, user, style] = await Promise.all([
          api.getThemes(),
          api.getUser(uid),
          api.getStyle(uid),
        ]);
        setThemes(ts);
        setTheme(user.theme);
        const cur = ts.find((t) => t.id === user.theme);
        if (cur?.colors?.accent) setAccent(cur.colors.accent);
        if (style.scale != null) setScale(style.scale);
        if (style.leading != null) setLeading(style.leading);
        if (style.accent) setAccent(style.accent);
        if (style.dropcap != null) setDropcap(style.dropcap);
        if (style.body_font) setBodyFont(style.body_font);
        if (style.headline_font) setHeadlineFont(style.headline_font);
      } catch (e) {
        setErr(errMsg(e));
      }
      setLoading(false);
    })();
  }, []);

  // Debounced live preview (each refresh re-renders server-side).
  const target = useMemo(() => {
    if (!theme) return "";
    const p = new URLSearchParams();
    p.set("scale", String(scale));
    p.set("leading", String(leading));
    if (accent) p.set("accent", accent);
    p.set("dropcap", String(dropcap));
    if (bodyFont) p.set("body_font", bodyFont);
    if (headlineFont) p.set("headline_font", headlineFont);
    return `/api/v1/themes/${encodeURIComponent(theme)}/preview?${p.toString()}`;
  }, [theme, scale, leading, accent, dropcap, bodyFont, headlineFont]);

  useEffect(() => {
    if (!target) return;
    const id = setTimeout(() => setPreviewUrl(target), 600);
    return () => clearTimeout(id);
  }, [target]);

  async function save() {
    setOk("");
    setErr("");
    try {
      await api.putStyle(getCurrentUser(), {
        scale,
        leading,
        accent,
        dropcap,
        body_font: bodyFont || null,
        headline_font: headlineFont || null,
      });
      setOk("Сохранено — применится к новым выпускам.");
    } catch (e) {
      setErr(errMsg(e));
    }
  }

  async function reset() {
    setScale(1);
    setLeading(1.45);
    setDropcap(true);
    setBodyFont("");
    setHeadlineFont("");
    try {
      await api.putStyle(getCurrentUser(), {
        scale: null, leading: null, accent: null,
        body_font: null, headline_font: null, dropcap: null,
      });
      setOk("Сброшено к стилю темы.");
    } catch (e) {
      setErr(errMsg(e));
    }
  }

  if (loading) return <Loading />;

  return (
    <>
      <h1 className="page-title">Типографика</h1>
      <p className="page-sub">Подстройте размер, интерлиньяж, акцент и буквицу под комфортное чтение — превью обновляется вживую.</p>
      <Banner kind="ok">{ok}</Banner>
      <Banner kind="err">{err}</Banner>

      <div className="grid cols-2">
        <div className="card">
          <h3>Настройки чтения</h3>

          <div className="field">
            <label>Тема (превью)</label>
            <select value={theme} onChange={(e) => setTheme(e.target.value)}>
              {themes.map((t) => <option key={t.id} value={t.id}>{t.display_name}</option>)}
            </select>
          </div>

          <div className="field">
            <label>Размер чтения — {scale.toFixed(2)}×</label>
            <input type="range" min={0.85} max={1.35} step={0.05} value={scale}
                   onChange={(e) => setScale(+e.target.value)} style={{ width: "100%" }} />
          </div>

          <div className="field">
            <label>Интерлиньяж — {leading.toFixed(2)}</label>
            <input type="range" min={1.2} max={1.75} step={0.05} value={leading}
                   onChange={(e) => setLeading(+e.target.value)} style={{ width: "100%" }} />
          </div>

          <div className="row" style={{ alignItems: "center", gap: 16 }}>
            <div className="field" style={{ marginBottom: 0 }}>
              <label>Акцент</label>
              <input type="color" value={accent} onChange={(e) => setAccent(e.target.value)}
                     style={{ width: 56, height: 34, padding: 2 }} />
            </div>
            <label className="row" style={{ gap: 8, marginTop: 18 }}>
              <input type="checkbox" checked={dropcap} onChange={(e) => setDropcap(e.target.checked)} />
              Буквица
            </label>
          </div>

          <div className="row" style={{ marginTop: 8 }}>
            <div className="field" style={{ flex: 1 }}>
              <label>Шрифт текста</label>
              <select value={bodyFont} onChange={(e) => setBodyFont(e.target.value)}>
                {FONTS.map(([v, l]) => <option key={v} value={v}>{l}</option>)}
              </select>
            </div>
            <div className="field" style={{ flex: 1 }}>
              <label>Шрифт заголовков</label>
              <select value={headlineFont} onChange={(e) => setHeadlineFont(e.target.value)}>
                {FONTS.map(([v, l]) => <option key={v} value={v}>{l}</option>)}
              </select>
            </div>
          </div>

          <div className="row">
            <button className="btn" onClick={save}>Сохранить</button>
            <button className="btn secondary" onClick={reset}>Сбросить</button>
          </div>
        </div>

        <div className="card">
          <h3>Живое превью</h3>
          {previewUrl ? (
            <iframe
              key={previewUrl}
              src={previewUrl}
              title="theme preview"
              style={{ width: "100%", height: 560, border: "1px solid var(--line)", borderRadius: 8, background: "#fff" }}
            />
          ) : (
            <p className="muted">готовлю превью…</p>
          )}
          <p className="muted" style={{ marginTop: 8 }}>Превью рендерится на сервере той же типографикой, что и газета.</p>
        </div>
      </div>
    </>
  );
}
