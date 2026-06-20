"use client";

import { useEffect, useState } from "react";
import { api, ApiError, getCurrentUser } from "@/lib/api";
import type { Profile } from "@/lib/types";
import { Banner, Loading, errMsg } from "@/components/ui";

type Kind = "topic" | "entity";

function sortEntries(obj: Record<string, number>): [string, number][] {
  return Object.entries(obj).sort((a, b) => b[1] - a[1]);
}

export default function ProfilePage() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);
  const [building, setBuilding] = useState(false);
  const [ok, setOk] = useState("");
  const [err, setErr] = useState("");

  async function load() {
    try {
      setProfile(await api.getProfile(getCurrentUser()));
      setErr("");
    } catch (e) {
      if (e instanceof ApiError && e.status === 404) setProfile(null);
      else setErr(errMsg(e));
    }
  }

  useEffect(() => {
    (async () => {
      await load();
      setLoading(false);
    })();
  }, []);

  async function build() {
    setBuilding(true);
    setOk("");
    setErr("");
    try {
      await api.buildProfile(getCurrentUser());
      // The build runs ingest+tag in the background; poll for the persisted result.
      const before = profile?.version ?? -1;
      for (let i = 0; i < 6; i++) {
        await new Promise((r) => setTimeout(r, 1500));
        await load();
        const cur = await api.getProfile(getCurrentUser()).catch(() => null);
        if (cur && cur.version !== before && Object.keys(cur.topics).length) break;
      }
      setOk("Профиль обновлён. Если он пуст — добавьте источники и ключ ANTHROPIC_API_KEY.");
    } catch (e) {
      setErr(errMsg(e));
    }
    setBuilding(false);
  }

  async function vote(kind: Kind, name: string, v: 1 | -1) {
    setOk("");
    setErr("");
    try {
      await api.postFeedback(getCurrentUser(), {
        vote: v,
        topics: kind === "topic" ? [name] : [],
        entities: kind === "entity" ? [name] : [],
      });
      setOk(`${v > 0 ? "👍" : "👎"} учтено для «${name}». Применится при следующем построении профиля.`);
    } catch (e) {
      setErr(errMsg(e));
    }
  }

  if (loading) return <Loading />;

  const topics = profile ? sortEntries(profile.topics) : [];
  const entities = profile ? sortEntries(profile.entities) : [];

  return (
    <>
      <h1 className="page-title">Профиль интересов</h1>
      <p className="page-sub">
        Темы и сущности, по которым отбираются новости. Оценивайте 👍/👎 — профиль дообучается.
      </p>
      <Banner kind="ok">{ok}</Banner>
      <Banner kind="err">{err}</Banner>

      <div className="row" style={{ marginBottom: 18 }}>
        <button className="btn" onClick={build} disabled={building}>
          {building ? "Построение…" : "Построить / обновить профиль"}
        </button>
        {profile ? <span className="muted">версия {profile.version}</span> : null}
      </div>

      {!profile || (!topics.length && !entities.length) ? (
        <p className="empty">Профиль пуст. Добавьте источники на вкладке «Источники» и постройте профиль.</p>
      ) : (
        <div className="grid cols-2">
          <div className="card">
            <h3>Темы</h3>
            {topics.length ? (
              topics.map(([name, w]) => (
                <Bar key={name} name={name} weight={w} cls="" onVote={(v) => vote("topic", name, v)} />
              ))
            ) : (
              <p className="empty">нет тем</p>
            )}
          </div>
          <div className="card">
            <h3>Сущности</h3>
            {entities.length ? (
              entities.map(([name, w]) => (
                <Bar key={name} name={name} weight={w} cls="ent" onVote={(v) => vote("entity", name, v)} />
              ))
            ) : (
              <p className="empty">нет сущностей</p>
            )}
          </div>
        </div>
      )}
    </>
  );
}

function Bar({
  name,
  weight,
  cls,
  onVote,
}: {
  name: string;
  weight: number;
  cls: string;
  onVote: (v: 1 | -1) => void;
}) {
  const pct = Math.max(2, Math.min(100, Math.round(weight * 100)));
  return (
    <div className="bar">
      <div className="bar__label" title={name}>{name}</div>
      <div className="bar__track">
        <div className={`bar__fill ${cls}`} style={{ width: `${pct}%` }} />
      </div>
      <div className="bar__actions">
        <button className="iconbtn" title="больше такого" onClick={() => onVote(1)}>👍</button>
        <button className="iconbtn" title="меньше такого" onClick={() => onVote(-1)}>👎</button>
      </div>
    </div>
  );
}
