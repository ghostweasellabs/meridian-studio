import React from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

function HomePage(): JSX.Element {
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold">Home</h2>
      <p className="mt-2 text-neutral-600">Welcome to Meridian Studio.</p>
    </div>
  )
}

export function App(): JSX.Element {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen">
          <header className="border-b p-4 flex items-center gap-4">
            <Link to="/" className="font-semibold">Meridian Studio</Link>
            <nav className="text-sm text-neutral-600 flex gap-3">
              <Link to="/">Home</Link>
            </nav>
          </header>
          <main>
            <Routes>
              <Route path="/" element={<HomePage />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  )
}


