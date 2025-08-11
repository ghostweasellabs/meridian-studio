import { supabase } from "./supabaseClient";

export async function api<T>(path: string, opts: RequestInit = {}): Promise<T> {
  const { data } = await supabase.auth.getSession();
  const session = data.session;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(opts.headers as Record<string, string> | undefined),
  };
  if (session?.access_token) {
    headers["Authorization"] = `Bearer ${session.access_token}`;
  }

  const res = await fetch(`${import.meta.env.VITE_API_URL}${path}`, {
    ...opts,
    headers,
  });
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json() as Promise<T>;
}

export interface GraphSummary {
  id: string;
  name: string;
  description: string;
  tags: string[];
  created_at: string;
}

export function listMyGraphs(
  params?: { search?: string; limit?: number; offset?: number },
) {
  const q = new URLSearchParams();
  if (params?.search) q.set("search", params.search);
  if (params?.limit) q.set("limit", String(params.limit));
  if (params?.offset) q.set("offset", String(params.offset));
  return api<GraphSummary[]>(`/graphs/?${q.toString()}`);
}

export function listPublicGraphs(
  params?: { search?: string; limit?: number; offset?: number },
) {
  const q = new URLSearchParams();
  if (params?.search) q.set("search", params.search);
  if (params?.limit) q.set("limit", String(params.limit));
  if (params?.offset) q.set("offset", String(params.offset));
  return api<
    Array<
      GraphSummary & { owner_name: string | null; owner_email: string | null }
    >
  >(
    `/sharing/public?${q.toString()}`,
  );
}
