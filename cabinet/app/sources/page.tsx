"use client";

import { useEffect, useState } from "react";
import { api, ApiError, getCurrentUser } from "@/lib/api";
import type { SourceAccount, SourceInfo } from "@/lib/types";
import { Banner, Loading, errMsg } from "@/components/ui";

interface RowState {
  enabled: boolean;
  optionsText: string;
  configured: boolean;
  saving: boolean;
  msg: string;
  err: string;
}

function schemaHint(info: SourceInfo): string {
  const props = (info.config_schema?.properties as Record<string, unknown>) || {};
  const keys = Object.keys(props);
  return keys.length ? `опции: ${keys.join(", ")}` : "без опций";
}

export default function SourcesPage() {
  const [catalog, setCatalog] = useState<SourceInfo[]>([]);
  const [rows, setRows] = useState<Record<string, RowState>>({});
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");

  useEffect(() => {
    const uid = getCurrentUser();
    (async () => {
      try {
        const cat = await api.getSources();
        setCatalog(cat);
        const state: Record<string, RowState> = {};
        await Promise.all(
          cat.map(async (s) => {
            let acc: SourceAccount | null = null;
            try {
              acc = await api.getUserSource(uid, s.source_id);
            } catch (e) {
              if (!(e instanceof ApiError && e.status === 404)) throw e;
            }
            state[s.source_id] = {
              enabled: acc?.enabled ?? true,
              optionsText: JSON.stringify(acc?.options ?? {}, null, 2),
              configured: acc !== null,
              saving: false,
              msg: "",
              err: "",
            };
          })
        );
        setRows(state);
      } catch (e) {
        setErr(errMsg(e));
      }
      setLoading(false);
    })();
  }, []);

  function patch(id: string, p: Partial<RowState>) {
    setRows((r) => ({ ...r, [id]: { ...r[id], ...p } }));
  }

  async function save(info: SourceInfo) {
    const id = info.source_id;
    const row = rows[id];
    let options: Record<string, unknown>;
    try {
      options = row.optionsText.trim() ? JSON.parse(row.optionsText) : {};
    } catch {
      patch(id, { err: "Опции должны быть корректным JSON", msg: "" });
      return;
    }
    patch(id, { saving: true, err: "", msg: "" });
    try {
      const acc = await api.putUserSource(getCurrentUser(), id, { enabled: row.enabled, options });
      patch(id, {
        saving: false,
        configured: true,
        msg: "Сохранено",
        optionsText: JSON.stringify(acc.options, null, 2),
      });
    } catch (e) {
      patch(id, { saving: false, err: errMsg(e) });
    }
  }

  if (loading) return <Loading />;

  return (
    <>
      <h1 className="page-title">Источники интересов</h1>
      <p className="page-sub">
        Подключайте независимые источники. Секретные опции (сессии, токены) на чтении
        скрыты — впишите их заново, чтобы обновить.
      </p>
      <Banner kind="err">{err}</Banner>

      <div className="grid cols-2">
        {catalog.map((s) => {
          const row = rows[s.source_id];
          if (!row) return null;
          return (
            <div className="card" key={s.source_id}>
              <div className="row" style={{ justifyContent: "space-between" }}>
                <h3 style={{ margin: 0 }}>{s.display_name}</h3>
                <span className="pill">{s.requires_auth ? "нужен логин" : "без логина"}</span>
              </div>
              <p className="muted" style={{ marginTop: 4 }}>
                <code>{s.source_id}</code> · {schemaHint(s)}
                {row.configured ? " · подключён" : ""}
              </p>

              <label className="row" style={{ gap: 8, marginBottom: 10 }}>
                <input
                  type="checkbox"
                  checked={row.enabled}
                  onChange={(e) => patch(s.source_id, { enabled: e.target.checked })}
                />
                включён
              </label>

              <div className="field">
                <label>опции (JSON)</label>
                <textarea
                  value={row.optionsText}
                  onChange={(e) => patch(s.source_id, { optionsText: e.target.value })}
                  spellCheck={false}
                />
              </div>

              {row.msg ? <Banner kind="ok">{row.msg}</Banner> : null}
              {row.err ? <Banner kind="err">{row.err}</Banner> : null}

              <button className="btn small" onClick={() => save(s)} disabled={row.saving}>
                {row.saving ? "Сохранение…" : "Сохранить"}
              </button>
            </div>
          );
        })}
      </div>
    </>
  );
}
