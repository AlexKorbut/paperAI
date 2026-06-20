// Wire types mirroring src/morning_paper/api/schemas.py. Kept in sync by hand —
// these are the public API contract, not internal models.

export interface User {
  user_id: string;
  output_lang: string;
  theme: string;
  tz: string;
  deliver_channel: string;
}

export interface UserUpdate {
  output_lang?: string;
  theme?: string;
  tz?: string;
  deliver_channel?: string;
}

export interface Theme {
  id: string;
  display_name: string;
  mood: string;
  page: string;
  columns: number;
  color_mode: string;
  colors: { paper: string; ink: string; accent: string };
}

export interface SourceInfo {
  source_id: string;
  display_name: string;
  requires_auth: boolean;
  config_schema: Record<string, unknown>;
}

export interface SourceAccount {
  source_id: string;
  enabled: boolean;
  status: string;
  options: Record<string, unknown>;
}

export interface Profile {
  user_id: string;
  output_lang: string;
  topics: Record<string, number>;
  entities: Record<string, number>;
  version: number;
  updated_at: string;
}

export interface FeedbackIn {
  vote: 1 | -1;
  issue_id?: string | null;
  story_id?: string | null;
  section?: string | null;
  topics?: string[];
  entities?: string[];
}

export interface FeedbackOut {
  id: string;
  user_id: string;
  vote: number;
  recorded_at: string;
}

export interface Job {
  job_id: string;
  issue_id?: string | null;
  status: string;
}

export interface IssueSummary {
  id: string;
  theme_id?: string | null;
  status: string;
  pdf_url?: string | null;
  created_at?: string | null;
}

export interface Cost {
  cost_usd: number;
  tokens_in: number;
  tokens_out: number;
}

export interface IssueStatus {
  issue_id: string;
  status: string;
  theme_id?: string | null;
  pdf_url?: string | null;
  cost: Cost;
}

export interface IssueCreate {
  theme_id?: string | null;
  output_lang?: string | null;
  feed_urls?: string[];
}
