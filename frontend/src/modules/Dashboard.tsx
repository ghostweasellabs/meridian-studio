import React from "react";
import { useAuth } from "./auth/AuthProvider";
import { Button } from "../components/ui/button";

export function Dashboard(): JSX.Element {
  const { user, signOut } = useAuth();
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold">Dashboard</h2>
      <p className="mt-2 text-neutral-600">Signed in as {user?.email}</p>
      <div className="mt-4">
        <Button onClick={() => void signOut()}>Sign out</Button>
      </div>
    </div>
  );
}
