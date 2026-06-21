"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { getCurrentUser, setCurrentUser } from "@/lib/api";

const LINKS: [string, string][] = [
  ["/", "Обзор"],
  ["/settings", "Настройки"],
  ["/sources", "Источники"],
  ["/themes", "Стили"],
  ["/typography", "Типографика"],
  ["/profile", "Профиль"],
  ["/issues", "Выпуски"],
  ["/print", "Печать"],
  ["/groups", "Группы"],
  ["/marketplace", "Маркетплейс"],
  ["/privacy", "Приватность"],
];

export default function Nav() {
  const pathname = usePathname();
  const [user, setUser] = useState("me");
  const [draft, setDraft] = useState("me");

  useEffect(() => {
    const u = getCurrentUser();
    setUser(u);
    setDraft(u);
  }, []);

  function applyUser() {
    const next = draft.trim() || "me";
    if (next !== user) {
      setCurrentUser(next);
      // Hard reload so every page refetches for the new user.
      window.location.reload();
    }
  }

  return (
    <header className="topbar">
      <div className="topbar__inner">
        <div className="brand">
          Morning <span>Paper</span>
        </div>
        <nav className="nav">
          {LINKS.map(([href, label]) => {
            const active = href === "/" ? pathname === "/" : pathname.startsWith(href);
            return (
              <Link key={href} href={href} className={active ? "active" : ""}>
                {label}
              </Link>
            );
          })}
        </nav>
        <div className="userswitch">
          <span>user:</span>
          <input
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") applyUser();
            }}
            onBlur={applyUser}
            aria-label="active user id"
          />
        </div>
      </div>
    </header>
  );
}
