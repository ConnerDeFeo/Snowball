import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Company from './pages/Company';
import Rubric from './pages/Rubric';
import CategoryEditor from './features/rubric/CategoryEditor';
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
          <Route path="/rubric" element={<Rubric />}>
            <Route
              index
              element={<EmptyState title="Select a category" description="Choose a rubric category from the list to view or edit it." />}
            />
            <Route path=":category" element={<CategoryEditor />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ToastProvider>
  )
}

export default App
