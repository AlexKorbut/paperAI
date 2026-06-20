"use client";

import { useEffect, useState } from "react";
import { api, getCurrentUser } from "@/lib/api";
import type { Theme, User } from "@/lib/types";
import { Banner, Loading, errMsg } from "@/components/ui";

const CHANNELS = ["file", "telegram", "email"];
const LANGS = ["ru", "en", "de", "fr", "es"];

export default function SettingsPage() {
  const [user, setUser] = useState<User | null>(null);
  const [themes, setThemes] = useState<Theme[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [ok, setOk] = useState("");
  const [err, setErr] = useState("");

  useEffect(() => {
    const uid = getCurrentUser();
    (async () => {
      try {
        const [u, t] = await Promise.all([api.getUser(uid), api.getThemes()]);
        setUser(u);
        setThemes(t);
      } catch (e) {
        setErr(errMsg(e));
      }
      setLoading(false);
    })();
  }, []);

  async function save() {
    if (!user) return;
    setSaving(true);
    setOk("");
    setErr("");
    try {
      const updated = await api.updateUser(getCurrentUser(), {
        theme: user.theme,
        output_lang: user.output_lang,
        tz: user.tz,
        deliver_channel: user.deliver_channel,
      });
      setUser(updated);
      setOk("Сохранено");
    } catch (e) {
      setErr(errMsg(e));
    }
    setSaving(false);
  }

  if (loading) return <Loading />;
  if (!user) return <Banner kind="err">{err || "Не удалось загрузить пользователя"}</Banner>;

  return (
    <>
      <h1 className="page-title">Настройки</h1>
      <p className="page-sub">Язык газеты, стиль, таймзона и канал доставки.</p>
      <Banner kind="ok">{ok}</Banner>
      <Banner kind="err">{err}</Banner>

      <div className="card" style={{ maxWidth: 520 }}>
        <div className="field">
          <label>Стиль</label>
          <select value={user.theme} onChange={(e) => setUser({ ...user, theme: e.target.value })}>
            {themes.map((t) => (
              <option key={t.id} value={t.id}>
                {t.display_name}
              </option>
            ))}
          </select>
        </div>

        <div className="field">
          <label>Язык газеты</label>
          <select value={user.output_lang} onChange={(e) => setUser({ ...user, output_lang: e.target.value })}>
            {LANGS.map((l) => (
              <option key={l} value={l}>{l}</option>
            ))}
          </select>
        </div>

        <div className="field">
          <label>Таймзона</label>
          <input value={user.tz} onChange={(e) => setUser({ ...user, tz: e.target.value })} placeholder="Europe/Moscow" />
        </div>

        <div className="field">
          <label>Доставка</label>
          <select value={user.deliver_channel} onChange={(e) => setUser({ ...user, deliver_channel: e.target.value })}>
            {CHANNELS.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>

        <button className="btn" onClick={save} disabled={saving}>
          {saving ? "Сохранение…" : "Сохранить"}
        </button>
      </div>
    </>
  );
}
