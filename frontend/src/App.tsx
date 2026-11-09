import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Company from './pages/Company';
import Checklist from './pages/Checklist';
import CategoryEditor from './features/checklist/CategoryEditor';
import EmptyState from './shared/EmptyState';
import ToastProvider from './shared/toast/ToastProvider';
import Header from './shared/Header';

function App() {
  return (
    <ToastProvider>
      <BrowserRouter>
      <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/company/:tckr" element={<Company />} />
          <Route path="/checklist" element={<Checklist />}>
            <Route
              index
              element={<EmptyState title="Select a category" description="Choose a checklist category from the list, or add a new one." />}
            />
            <Route path=":categoryId" element={<CategoryEditor />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ToastProvider>
  )
}

export default App
