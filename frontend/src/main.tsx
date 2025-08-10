import React from 'npm:react'
import { createRoot } from 'npm:react-dom/client'
import { App } from './modules/App'
import './styles/index.css'

const container = document.getElementById('root')!
createRoot(container).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)


