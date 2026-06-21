"use client";

import { useEffect, useMemo, useState } from "react";
import { api, getCurrentUser } from "@/lib/api";
import type { PrintOrder, PrintProvider, PrintQuote } from "@/lib/types";
import { Banner, Loading, Pill, errMsg } from "@/components/ui";

export default function PrintPage() {
  const [providers, setProviders] = useState<PrintProvider[]>([]);
  const [orders, setOrders] = useState<PrintOrder[]>([]);
  const [provider, setProvider] = useState("");
  const [format, setFormat] = useState("");
  const [pages, setPages] = useState(8);
  const [copies, setCopies] = useState(1);
  const [country, setCountry] = useState("US");
  const [issueId, setIssueId] = useState("");
  const [addr, setAddr] = useState({ name: "", line1: "", city: "", postcode: "", country: "US" });
  const [quote, setQuote] = useState<PrintQuote | null>(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [ok, setOk] = useState("");
  const [err, setErr] = useState("");

  const current = useMemo(() => providers.find((p) => p.provider_id === provider), [providers, provider]);

  async function refreshOrders() {
    try {
      setOrders(await api.listPrintOrders(getCurrentUser()));
    } catch {
      /* ignore */
    }
  }

  useEffect(() => {
    (async () => {
      try {
        const provs = await api.printProviders();
        setProviders(provs);
        if (provs[0]) {
          setProvider(provs[0].provider_id);
          setFormat(provs[0].supported_formats[0]);
        }
      } catch (e) {
        setErr(errMsg(e));
      }
      await refreshOrders();
      setLoading(false);
    })();
  }, []);

  function onProvider(id: string) {
    setProvider(id);
    const p = providers.find((x) => x.provider_id === id);
    if (p && !p.supported_formats.includes(format)) setFormat(p.supported_formats[0]);
    setQuote(null);
  }

  async function getQuote() {
    setErr("");
    setOk("");
    try {
      setQuote(await api.printQuote({ provider, format, pages, copies, country }));
    } catch (e) {
      setErr(errMsg(e));
    }
  }

  async function order() {
    setBusy(true);
    setErr("");
    setOk("");
    try {
      const o = await api.createPrintOrder(getCurrentUser(), {
        provider,
        format,
        copies,
        pages,
        issue_id: issueId || null,
        address: { ...addr, country },
      });
      setOk(
        `Заказ ${o.id}: ${o.status}, $${o.quote.total_usd.toFixed(2)}` +
          (o.status === "needs_credentials" ? " — задайте ключ провайдера, чтобы оформить" : "")
      );
      await refreshOrders();
    } catch (e) {
      setErr(errMsg(e));
    }
    setBusy(false);
  }

  if (loading) return <Loading />;

  return (
    <>
      <h1 className="page-title">Печать по требованию</h1>
      <p className="page-sub">Закажите бумажную газету через типографию (Newspaper Club / Mixam). Цена — оценка.</p>
      <Banner kind="ok">{ok}</Banner>
      <Banner kind="err">{err}</Banner>

      <div className="grid cols-2">
        <div className="card">
          <h3>Параметры</h3>
          <div className="field">
            <label>Типография</label>
            <select value={provider} onChange={(e) => onProvider(e.target.value)}>
              {providers.map((p) => (
                <option key={p.provider_id} value={p.provider_id}>{p.display_name}</option>
              ))}
            </select>
          </div>
          <div className="field">
            <label>Формат</label>
            <select value={format} onChange={(e) => { setFormat(e.target.value); setQuote(null); }}>
              {current?.supported_formats.map((f) => (
                <option key={f} value={f}>{f}</option>
              ))}
            </select>
          </div>
          <div className="row">
            <div className="field" style={{ flex: 1 }}>
              <label>Страниц</label>
              <input type="number" min={1} value={pages} onChange={(e) => setPages(+e.target.value)} />
            </div>
            <div className="field" style={{ flex: 1 }}>
              <label>Тираж</label>
              <input type="number" min={1} value={copies} onChange={(e) => setCopies(+e.target.value)} />
            </div>
            <div className="field" style={{ flex: 1 }}>
              <label>Страна</label>
              <input value={country} onChange={(e) => { setCountry(e.target.value.toUpperCase()); setQuote(null); }} />
            </div>
          </div>
          <div className="field">
            <label>ID выпуска (необязательно — подставит PDF и число страниц)</label>
            <input value={issueId} onChange={(e) => setIssueId(e.target.value)} placeholder="20260619-…" />
          </div>
          <button className="btn secondary" onClick={getQuote}>Рассчитать цену</button>
          {quote ? (
            <p style={{ marginTop: 12 }}>
              <strong>${quote.total_usd.toFixed(2)}</strong>{" "}
              <span className="muted">
                (ед. ${quote.unit_price_usd.toFixed(2)} × {quote.copies} + доставка ${quote.shipping_usd.toFixed(2)})
              </span>
            </p>
          ) : null}
        </div>

        <div className="card">
          <h3>Адрес доставки</h3>
          <div className="field"><label>Имя</label><input value={addr.name} onChange={(e) => setAddr({ ...addr, name: e.target.value })} /></div>
          <div className="field"><label>Адрес</label><input value={addr.line1} onChange={(e) => setAddr({ ...addr, line1: e.target.value })} /></div>
          <div className="row">
            <div className="field" style={{ flex: 1 }}><label>Город</label><input value={addr.city} onChange={(e) => setAddr({ ...addr, city: e.target.value })} /></div>
            <div className="field" style={{ flex: 1 }}><label>Индекс</label><input value={addr.postcode} onChange={(e) => setAddr({ ...addr, postcode: e.target.value })} /></div>
          </div>
          <button className="btn" onClick={order} disabled={busy || !addr.name || !addr.line1}>
            {busy ? "Оформление…" : "Заказать печать"}
          </button>
        </div>
      </div>

      <div className="card" style={{ marginTop: 18 }}>
        <h3>Мои заказы</h3>
        {orders.length ? (
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
            <thead>
              <tr style={{ textAlign: "left", color: "var(--muted)" }}>
                <th style={{ padding: "6px 4px" }}>Заказ</th><th>Типография</th><th>Формат</th><th>Тираж</th><th>Сумма</th><th>Статус</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((o) => (
                <tr key={o.id} style={{ borderTop: "1px solid var(--line)" }}>
                  <td style={{ padding: "8px 4px", fontFamily: "ui-monospace, monospace" }}>{o.id}</td>
                  <td>{o.provider}</td>
                  <td>{o.format}</td>
                  <td>{o.copies}</td>
                  <td>${o.quote.total_usd.toFixed(2)}</td>
                  <td><Pill status={o.status} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="empty">пока нет заказов</p>
        )}
      </div>
    </>
  );
}
