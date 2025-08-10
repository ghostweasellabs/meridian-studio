import React, { useState } from "react";
import { Input } from "../components/ui/input";
import { Button } from "../components/ui/button";
import { useAuth } from "./auth/AuthProvider";
import { Link, Navigate } from "react-router-dom";

export function SignUpPage(): JSX.Element {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);
  const { user, signUpWithEmailPassword } = useAuth();

  async function onSignUp(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setInfo(null);
    const { error } = await signUpWithEmailPassword(email, password);
    if (error) setError(error);
    else {setInfo(
        "Account created. Check your email to confirm or sign in now.",
      );}
  }

  if (user) return <Navigate to="/dashboard" replace />;

  return (
    <div className="p-6 max-w-sm mx-auto">
      <h2 className="text-xl font-semibold">Create account</h2>
      <form className="mt-4 grid gap-3" onSubmit={onSignUp}>
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
        {info ? <div className="text-green-600 text-sm">{info}</div> : null}
        <Button type="submit">Create account</Button>
      </form>
      <div className="mt-3 text-sm text-neutral-600">
        Already have an account?{" "}
        <Link to="/auth" className="underline">Sign in</Link>
      </div>
    </div>
  );
}
