"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { Group, Theme } from "@/lib/types";
import { Banner, Loading, errMsg } from "@/components/ui";

export default function GroupsPage() {
  const [groups, setGroups] = useState<Group[]>([]);
  const [themes, setThemes] = useState<Theme[]>([]);
  const [name, setName] = useState("");
  const [members, setMembers] = useState("");
  const [theme, setTheme] = useState("");
  const [loading, setLoading] = useState(true);
  const [ok, setOk] = useState("");
  const [err, setErr] = useState("");

  async function refresh() {
    try {
      setGroups(await api.listGroups());
    } catch (e) {
      setErr(errMsg(e));
    }
  }

  useEffect(() => {
    (async () => {
      try {
        setThemes(await api.getThemes());
      } catch {
        /* ignore */
      }
      await refresh();
      setLoading(false);
    })();
  }, []);

  async function create() {
    setOk("");
    setErr("");
    try {
      const list = members.split(",").map((s) => s.trim()).filter(Boolean);
      await api.createGroup({ name, members: list, theme: theme || null });
      setName("");
      setMembers("");
      setOk("Группа создана");
      await refresh();
    } catch (e) {
      setErr(errMsg(e));
    }
  }

  async function addMember(gid: string) {
    const uid = window.prompt("ID участника:");
    if (!uid) return;
    try {
      await api.addGroupMember(gid, uid.trim());
      await refresh();
    } catch (e) {
      setErr(errMsg(e));
    }
  }

  async function removeMember(gid: string, uid: string) {
    try {
      await api.removeGroupMember(gid, uid);
      await refresh();
    } catch (e) {
      setErr(errMsg(e));
    }
  }

  async function generate(gid: string) {
    setOk("");
    setErr("");
    try {
      await api.createGroupIssue(gid);
      setOk("Сборка общего выпуска запущена в фоне.");
    } catch (e) {
      setErr(errMsg(e));
    }
  }

  async function remove(gid: string) {
    if (!window.confirm("Удалить группу?")) return;
    try {
      await api.deleteGroup(gid);
      await refresh();
    } catch (e) {
      setErr(errMsg(e));
    }
  }

  if (loading) return <Loading />;

  return (
    <>
      <h1 className="page-title">Семейные / командные группы</h1>
      <p className="page-sub">Одна общая газета на нескольких человек — из объединённого профиля интересов.</p>
      <Banner kind="ok">{ok}</Banner>
      <Banner kind="err">{err}</Banner>

      <div className="card" style={{ marginBottom: 18, maxWidth: 640 }}>
        <h3>Новая группа</h3>
        <div className="field"><label>Название</label><input value={name} onChange={(e) => setName(e.target.value)} placeholder="Семья" /></div>
        <div className="field"><label>Участники (через запятую)</label><input value={members} onChange={(e) => setMembers(e.target.value)} placeholder="partner, kid" /></div>
        <div className="field">
          <label>Стиль</label>
          <select value={theme} onChange={(e) => setTheme(e.target.value)}>
            <option value="">— по умолчанию —</option>
            {themes.map((t) => <option key={t.id} value={t.id}>{t.display_name}</option>)}
          </select>
        </div>
        <button className="btn" onClick={create} disabled={!name}>Создать группу</button>
      </div>

      <div className="grid cols-2">
        {groups.map((g) => (
          <div className="card" key={g.id}>
            <div className="row" style={{ justifyContent: "space-between" }}>
              <h3 style={{ margin: 0 }}>{g.name}</h3>
              <span className="pill">{g.theme ?? "стиль по умолч."}</span>
            </div>
            <p className="muted">владелец: {g.owner}</p>
            <div style={{ margin: "8px 0" }}>
              {g.members.map((m) => (
                <span key={m} className="pill" style={{ marginRight: 6, marginBottom: 6, display: "inline-block" }}>
                  {m}
                  {m !== g.owner ? (
                    <button className="iconbtn" style={{ marginLeft: 6, padding: "0 6px" }} onClick={() => removeMember(g.id, m)} title="убрать">×</button>
                  ) : null}
                </span>
              ))}
            </div>
            <div className="row">
              <button className="btn small secondary" onClick={() => addMember(g.id)}>+ участник</button>
              <button className="btn small" onClick={() => generate(g.id)}>Собрать общий выпуск</button>
              <button className="btn small danger" onClick={() => remove(g.id)}>Удалить</button>
            </div>
          </div>
        ))}
        {!groups.length ? <p className="empty">пока нет групп</p> : null}
      </div>
    </>
  );
}
