import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Company from './pages/Company';
import Checklist from './pages/Checklist';
import ToastProvider from './shared/toast/ToastProvider';

function App() {
  return (
    <ToastProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/company/:tckr" element={<Company />} />
          <Route path="/checklist" element={<Checklist />} />
        </Routes>
      </BrowserRouter>
    </ToastProvider>
  )
}

export default App
