import React from "react";
import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Button } from "../components/ui/button";
import { AuthPage } from "./Auth";
import { AuthProvider } from "./auth/AuthProvider";
import { ProtectedRoute } from "./auth/ProtectedRoute";
import { Dashboard } from "./Dashboard";

const queryClient = new QueryClient();

function HomePage(): JSX.Element {
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold">Home</h2>
      <p className="mt-2 text-neutral-600">Welcome to Meridian Studio.</p>
    </div>
  );
}

export function App(): JSX.Element {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <div className="min-h-screen">
            <header className="border-b p-4 flex items-center gap-4">
              <Link to="/" className="font-semibold">
                Meridian Studio
              </Link>
              <nav className="text-sm text-neutral-600 flex gap-3">
                <Link to="/">Home</Link>
                <Link to="/dashboard">Dashboard</Link>
                <Link to="/auth">Sign in</Link>
              </nav>
              <div className="ml-auto">
                <Button size="sm">Primary</Button>
              </div>
            </header>
            <main>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/auth" element={<AuthPage />} />
                <Route
                  path="/dashboard"
                  element={
                    <ProtectedRoute>
                      <Dashboard />
                    </ProtectedRoute>
                  }
                />
              </Routes>
            </main>
          </div>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}
