import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Purchases from './pages/Purchases';
import Transfers from './pages/Transfers';
import Layout from './components/Layout';

function App() {
  const isAuthenticated = () => {
    return !!localStorage.getItem('token');
  };

  const PrivateRoute = ({ children }) => {
    return isAuthenticated() ? children : <Navigate to="/login" />;
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/"
          element={
            <PrivateRoute>
              <Layout />
            </PrivateRoute>
          }
        >
          <Route index element={<Navigate to="/dashboard" />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="purchases" element={<Purchases />} />
          <Route path="transfers" element={<Transfers />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
