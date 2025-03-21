import Register from './components/Register';
import { Layout } from './components/Layout';
import { HomePage } from './components/HomePage';
import { PageNotFound } from './components/PageNotFound';
import { ThemeProvider } from '@mui/material/styles';
import { Route, Routes } from 'react-router-dom';
import { CssBaseline } from '@mui/material';
import { customTheme } from './theme';

export default function App() {
  return (
    <ThemeProvider theme={customTheme}>
      <CssBaseline />
      <Routes>
        <Route path='/' element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path='/register' element={<Register />} />
          <Route path='*' element={<PageNotFound />} />
        </Route>
      </Routes>
    </ThemeProvider>
  );
}
