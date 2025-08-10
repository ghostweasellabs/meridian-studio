import React, { useState } from "react";
import { Input } from "../components/ui/input";
import { Button } from "../components/ui/button";

export function AuthPage(): JSX.Element {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function onSignIn(e: React.FormEvent) {
    e.preventDefault();
    // TODO: Wire supabase-js sign in
    alert(`Signing in: ${email}`);
  }

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
        <Button type="submit">Continue</Button>
      </form>
    </div>
  );
}
