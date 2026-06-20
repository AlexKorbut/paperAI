"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api, getCurrentUser } from "@/lib/api";
import type { IssueSummary, Profile, User } from "@/lib/types";
import { Banner, Loading, Pill, errMsg } from "@/components/ui";

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [issues, setIssues] = useState<IssueSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");

  useEffect(() => {
    const uid = getCurrentUser();
    (async () => {
      try {
        setUser(await api.getUser(uid));
      } catch (e) {
        setErr(errMsg(e));
      }
      try {
        setProfile(await api.getProfile(uid));
      } catch {
        /* no profile yet */
      }
      try {
        setIssues(await api.listIssues(uid));
      } catch {
        /* no issues / no db */
      }
      setLoading(false);
    })();
  }, []);

  if (loading) return <Loading />;

  const topicCount = profile ? Object.keys(profile.topics).length : 0;
  const entityCount = profile ? Object.keys(profile.entities).length : 0;

  return (
    <>
      <h1 className="page-title">Обзор</h1>
      <p className="page-sub">
        Личный кабинет газеты для <strong>{user?.user_id ?? getCurrentUser()}</strong>.
      </p>
      <Banner kind="err">{err}</Banner>

      <div className="grid cols-3">
        <div className="card">
          <h3>Настройки</h3>
          {user ? (
            <>
              <div className="kv"><span className="k">Стиль</span><span>{user.theme}</span></div>
              <div className="kv"><span className="k">Язык</span><span>{user.output_lang}</span></div>
              <div className="kv"><span className="k">Таймзона</span><span>{user.tz}</span></div>
              <div className="kv"><span className="k">Доставка</span><span>{user.deliver_channel}</span></div>
            </>
          ) : (
            <p className="muted">нет данных</p>
          )}
          <p style={{ marginTop: 12 }}><Link href="/settings">Изменить →</Link></p>
        </div>

        <div className="card">
          <h3>Профиль интересов</h3>
          {profile ? (
            <>
              <div className="kv"><span className="k">Темы</span><span>{topicCount}</span></div>
              <div className="kv"><span className="k">Сущности</span><span>{entityCount}</span></div>
              <div className="kv"><span className="k">Версия</span><span>{profile.version}</span></div>
            </>
          ) : (
            <p className="muted">профиль ещё не построен</p>
          )}
          <p style={{ marginTop: 12 }}><Link href="/profile">Открыть профиль →</Link></p>
        </div>

        <div className="card">
          <h3>Выпуски</h3>
          {issues.length ? (
            <ul style={{ paddingLeft: 18, margin: "4px 0" }}>
              {issues.slice(0, 4).map((i) => (
                <li key={i.id} style={{ marginBottom: 4 }}>
                  <span style={{ fontSize: 13 }}>{i.id.slice(0, 14)}</span> <Pill status={i.status} />
                </li>
              ))}
            </ul>
          ) : (
            <p className="muted">пока нет выпусков</p>
          )}
          <p style={{ marginTop: 12 }}><Link href="/issues">Все выпуски →</Link></p>
        </div>
      </div>
    </>
  );
}
