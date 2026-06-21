"use client";

import { useEffect, useState } from "react";
import { api, getCurrentUser } from "@/lib/api";
import type { MarketplaceTheme } from "@/lib/types";
import { Banner, Loading, errMsg } from "@/components/ui";

export default function MarketplacePage() {
  const [themes, setThemes] = useState<MarketplaceTheme[]>([]);
  const [loading, setLoading] = useState(true);
  const [ok, setOk] = useState("");
  const [err, setErr] = useState("");

  useEffect(() => {
    (async () => {
      try {
        setThemes(await api.marketplace());
      } catch (e) {
        setErr(errMsg(e));
      }
      setLoading(false);
    })();
  }, []);

  async function use(id: string) {
    setOk("");
    setErr("");
    try {
      await api.updateUser(getCurrentUser(), { theme: id });
      setOk(`Стиль выпуска: ${id}`);
    } catch (e) {
      setErr(errMsg(e));
    }
  }

  if (loading) return <Loading />;

  const builtin = themes.filter((t) => t.builtin);
  const third = themes.filter((t) => t.third_party);

  return (
    <>
      <h1 className="page-title">Маркетплейс стилей</h1>
      <p className="page-sub">
        Темы — это данные: сторонние стили ставятся без кода. Установка из CLI:
        <code> morning-paper install-theme --path bundle/ </code>.
      </p>
      <Banner kind="ok">{ok}</Banner>
      <Banner kind="err">{err}</Banner>

      {third.length ? (
        <>
          <h3>Сторонние</h3>
          <div className="grid cols-3" style={{ marginBottom: 20 }}>
            {third.map((t) => <ThemeCard key={t.id} t={t} onUse={use} />)}
          </div>
        </>
      ) : null}

      <h3>Встроенные</h3>
      <div className="grid cols-3">
        {builtin.map((t) => <ThemeCard key={t.id} t={t} onUse={use} />)}
      </div>
    </>
  );
}

function ThemeCard({ t, onUse }: { t: MarketplaceTheme; onUse: (id: string) => void }) {
  return (
    <div className="card">
      <div className="row" style={{ justifyContent: "space-between" }}>
        <h3 style={{ margin: 0 }}>{t.display_name}</h3>
        <span className="pill">{t.price_usd ? `$${t.price_usd.toFixed(2)}` : "free"}</span>
      </div>
      <p className="muted" style={{ minHeight: 36 }}>{t.mood}</p>
      <p className="muted">
        {t.builtin ? "встроенный" : `автор: ${t.author || "—"}`}
        {t.license ? ` · ${t.license}` : ""}
      </p>
      <button className="btn small secondary" onClick={() => onUse(t.id)}>Использовать</button>
    </div>
  );
}
