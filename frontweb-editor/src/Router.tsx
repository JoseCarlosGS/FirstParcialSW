import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './views/home/Home';
import NotFound from './views/componets/NotFound';
import Editor from './views/editor/components/Editor';
import Login from './views/login/Login';
import ProtectedRoute from './ProtectedRoute';

const Router: React.FC = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="*" element={<NotFound />} />
                <Route path='/login' element={<Login/>} />
                <Route element={<ProtectedRoute />}>
                    <Route path="/" element={<Home />} />
                    <Route path="/editor" element={<Editor />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
};

export default Router;