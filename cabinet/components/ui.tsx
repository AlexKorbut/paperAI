"use client";

import { ReactNode } from "react";

export function Banner({ kind, children }: { kind: "ok" | "err"; children: ReactNode }) {
  if (!children) return null;
  return <div className={`banner ${kind}`}>{children}</div>;
}

export function Pill({ status }: { status: string }) {
  return <span className={`pill ${status}`}>{status}</span>;
}

export function Loading({ label = "Загрузка…" }: { label?: string }) {
  return <div className="spinner">{label}</div>;
}

export function Card({ title, children }: { title?: string; children: ReactNode }) {
  return (
    <div className="card">
      {title ? <h3>{title}</h3> : null}
      {children}
    </div>
  );
}

export function Field({
  label,
  children,
}: {
  label: string;
  children: ReactNode;
}) {
  return (
    <div className="field">
      <label>{label}</label>
      {children}
    </div>
  );
}

/** Render an API error into a friendly string. */
export function errMsg(e: unknown): string {
  if (e && typeof e === "object" && "message" in e) return String((e as Error).message);
  return String(e);
}
