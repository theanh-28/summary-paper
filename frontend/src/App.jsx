import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, AuthContext } from './context/AuthContext';
import { useContext } from 'react';
import Login from './pages/Login';
import Register from './pages/Register';
import UploadSummary from './pages/UploadSummary';
import History from './pages/History';
import Navbar from './components/Navbar';
import './App.css';

const PrivateRoute = ({ children }) => {
    const { token } = useContext(AuthContext);
    return token ? children : <Navigate to="/login" />;
};

function AppRoutes() {
    return (
        <>
            <Navbar />
            <div className="main-content">
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route 
                        path="/" 
                        element={
                            <PrivateRoute>
                                <UploadSummary />
                            </PrivateRoute>
                        } 
                    />
                    <Route 
                        path="/history" 
                        element={
                            <PrivateRoute>
                                <History />
                            </PrivateRoute>
                        } 
                    />
                </Routes>
            </div>
        </>
    );
}

function App() {
    return (
        <Router>
            <AuthProvider>
                <AppRoutes />
            </AuthProvider>
        </Router>
    );
}

export default App;
