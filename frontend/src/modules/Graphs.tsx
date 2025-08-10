import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { listMyGraphs, listPublicGraphs } from "../lib/api";
import { Input } from "../components/ui/input";

export function MyGraphs(): JSX.Element {
  const [search, setSearch] = useState("");
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["my-graphs", search],
    queryFn: () => listMyGraphs({ search }),
  });
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold">My Graphs</h2>
      <div className="mt-3 flex gap-2 items-center">
        <Input
          placeholder="Search"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && refetch()}
          className="max-w-sm"
        />
      </div>
      <div className="mt-4 grid gap-3">
        {isLoading ? "Loading..." : null}
        {error
          ? <div className="text-red-600 text-sm">{String(error)}</div>
          : null}
        {data?.map((g) => (
          <div key={g.id} className="border rounded p-3">
            <div className="font-medium">{g.name}</div>
            <div className="text-sm text-neutral-600">{g.description}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export function PublicGallery(): JSX.Element {
  const [search, setSearch] = useState("");
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["public-graphs", search],
    queryFn: () => listPublicGraphs({ search }),
  });
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold">Public Gallery</h2>
      <div className="mt-3 flex gap-2 items-center">
        <Input
          placeholder="Search"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && refetch()}
          className="max-w-sm"
        />
      </div>
      <div className="mt-4 grid gap-3">
        {isLoading ? "Loading..." : null}
        {error
          ? <div className="text-red-600 text-sm">{String(error)}</div>
          : null}
        {data?.map((g) => (
          <div key={g.id} className="border rounded p-3">
            <div className="font-medium">{g.name}</div>
            <div className="text-sm text-neutral-600">{g.description}</div>
            <div className="text-xs text-neutral-500">
              {g.owner_name ?? g.owner_email ?? "Anonymous"}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
