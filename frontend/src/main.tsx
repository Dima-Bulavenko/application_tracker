import { createRoot } from 'react-dom/client';
import { App } from './app';
import './shared/theme/index.css';

createRoot(document.getElementById('root')!).render(<App />);
