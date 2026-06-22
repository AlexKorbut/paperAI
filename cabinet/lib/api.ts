// Typed client for the Morning Paper API. The browser calls same-origin `/api/*`
// which Next proxies to the backend (next.config.mjs). Every request carries the
// active user in the `X-MP-User` header (the backend's first-party auth).

import type {
  FeedbackIn,
  FeedbackOut,
  Group,
  IssueCreate,
  IssueStatus,
  IssueSummary,
  Job,
  MarketplaceTheme,
  PrintAddress,
  PrintOrder,
  PrintProvider,
  PrintQuote,
  Profile,
  SourceAccount,
  SourceInfo,
  StyleOverrides,
  Theme,
  User,
  UserUpdate,
} from "./types";

const USER_KEY = "mp_user";

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

export function getCurrentUser(): string {
  if (typeof window === "undefined") return "me";
  return window.localStorage.getItem(USER_KEY) || "me";
}

export function setCurrentUser(user: string): void {
  if (typeof window !== "undefined") {
    window.localStorage.setItem(USER_KEY, user.trim() || "me");
  }
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const res = await fetch(`/api${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      "X-MP-User": getCurrentUser(),
      ...(init.headers || {}),
    },
    cache: "no-store",
  });

  if (!res.ok) {
    let detail: string = res.statusText;
    try {
      const body = await res.json();
      detail = typeof body?.detail === "string" ? body.detail : JSON.stringify(body?.detail ?? body);
    } catch {
      try {
        detail = (await res.text()) || res.statusText;
      } catch {
        /* keep statusText */
      }
    }
    throw new ApiError(res.status, detail);
  }

  if (res.status === 204) return undefined as T;
  const ct = res.headers.get("content-type") || "";
  return ct.includes("application/json") ? ((await res.json()) as T) : (undefined as T);
}

const enc = encodeURIComponent;

export const api = {
  // Users / preferences
  getUser: (id: string) => request<User>(`/v1/users/${enc(id)}`),
  updateUser: (id: string, body: UserUpdate) =>
    request<User>(`/v1/users/${enc(id)}`, { method: "PUT", body: JSON.stringify(body) }),

  // Typography / reading-comfort overrides
  getStyle: (id: string) => request<StyleOverrides>(`/v1/users/${enc(id)}/style`),
  putStyle: (id: string, body: StyleOverrides) =>
    request<StyleOverrides>(`/v1/users/${enc(id)}/style`, { method: "PUT", body: JSON.stringify(body) }),

  // Catalogs
  getThemes: () => request<Theme[]>(`/v1/themes`),
  getSources: () => request<SourceInfo[]>(`/v1/sources`),

  // Per-user sources
  getUserSource: (id: string, sid: string) =>
    request<SourceAccount>(`/v1/users/${enc(id)}/sources/${enc(sid)}`),
  putUserSource: (id: string, sid: string, body: { enabled: boolean; options: Record<string, unknown> }) =>
    request<SourceAccount>(`/v1/users/${enc(id)}/sources/${enc(sid)}`, {
      method: "PUT",
      body: JSON.stringify(body),
    }),

  // Profile + feedback
  getProfile: (id: string) => request<Profile>(`/v1/users/${enc(id)}/profile`),
  buildProfile: (id: string) =>
    request<Job>(`/v1/users/${enc(id)}/profile:build`, { method: "POST" }),
  postFeedback: (id: string, body: FeedbackIn) =>
    request<FeedbackOut>(`/v1/users/${enc(id)}/feedback`, { method: "POST", body: JSON.stringify(body) }),

  // Issues
  listIssues: (id: string) => request<IssueSummary[]>(`/v1/users/${enc(id)}/issues`),
  createIssue: (id: string, body: IssueCreate) =>
    request<Job>(`/v1/users/${enc(id)}/issues`, { method: "POST", body: JSON.stringify(body) }),
  getIssue: (issueId: string) => request<IssueStatus>(`/v1/issues/${enc(issueId)}`),

  // Privacy / data rights
  exportData: (id: string) => request<Record<string, unknown>>(`/v1/users/${enc(id)}/data:export`),
  deleteData: (id: string) =>
    request<Record<string, unknown>>(`/v1/users/${enc(id)}/data`, { method: "DELETE" }),

  // Print on demand
  printProviders: () => request<PrintProvider[]>(`/v1/print/providers`),
  printQuote: (body: { provider: string; format: string; pages: number; copies: number; country: string }) =>
    request<PrintQuote>(`/v1/print/quote`, { method: "POST", body: JSON.stringify(body) }),
  createPrintOrder: (
    id: string,
    body: { provider: string; format: string; copies: number; issue_id?: string | null; pages?: number | null; address: PrintAddress },
  ) => request<PrintOrder>(`/v1/users/${enc(id)}/print-orders`, { method: "POST", body: JSON.stringify(body) }),
  listPrintOrders: (id: string) => request<PrintOrder[]>(`/v1/users/${enc(id)}/print-orders`),

  // Groups
  createGroup: (body: { name: string; members: string[]; theme?: string | null; output_lang?: string | null }) =>
    request<Group>(`/v1/groups`, { method: "POST", body: JSON.stringify(body) }),
  listGroups: () => request<Group[]>(`/v1/groups`),
  addGroupMember: (gid: string, user_id: string) =>
    request<Group>(`/v1/groups/${enc(gid)}/members`, { method: "POST", body: JSON.stringify({ user_id }) }),
  removeGroupMember: (gid: string, uid: string) =>
    request<Group>(`/v1/groups/${enc(gid)}/members/${enc(uid)}`, { method: "DELETE" }),
  deleteGroup: (gid: string) => request<{ deleted: boolean }>(`/v1/groups/${enc(gid)}`, { method: "DELETE" }),
  createGroupIssue: (gid: string) => request<Job>(`/v1/groups/${enc(gid)}/issues`, { method: "POST" }),

  // Marketplace
  marketplace: () => request<MarketplaceTheme[]>(`/v1/marketplace/themes`),
};
