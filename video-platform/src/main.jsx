import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import './styles.css';
import { I18nProvider } from './i18n.jsx';
import { ToastProvider } from './ui.jsx';
import { SessionProvider } from './session.jsx';
import App from './App.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <I18nProvider><ToastProvider><SessionProvider><App /></SessionProvider></ToastProvider></I18nProvider>
    </BrowserRouter>
  </StrictMode>,
);
