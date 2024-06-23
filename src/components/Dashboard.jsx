import React from 'react';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    // ... (restante do código do componente)

    return (
        <div>
            {/* ... (restante do conteúdo do dashboard) */}
            <button onClick={handleLogout}>Logout</button>
        </div>
    );
};


export default Dashboard;
