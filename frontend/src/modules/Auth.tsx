import React, { useState } from "react";
import { Input } from "../components/ui/input";
import { Button } from "../components/ui/button";
import { useAuth } from "./auth/AuthProvider";
import { Link, Navigate } from "react-router-dom";

export function AuthPage(): JSX.Element {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const { user, signInWithEmailPassword } = useAuth();

  async function onSignIn(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    const { error } = await signInWithEmailPassword(email, password);
    if (error) setError(error);
  }

  if (user) return <Navigate to="/dashboard" replace />;

  return (
    <div className="p-6 max-w-sm mx-auto">
      <h2 className="text-xl font-semibold">Sign in</h2>
      <form className="mt-4 grid gap-3" onSubmit={onSignIn}>
        <Input
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <Input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error ? <div className="text-red-600 text-sm">{error}</div> : null}
        <Button type="submit">Continue</Button>
      </form>
      <div className="mt-3 text-sm text-neutral-600">
        Don’t have an account? <Link to="#" className="underline">Sign up</Link>
      </div>
    </div>
  );
}
