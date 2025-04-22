import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './views/home/Home';
import NotFound from './views/componets/NotFound';
import Editor from './views/editor/components/Editor';
import Login from './views/login/Login';

const Router: React.FC = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/editor" element={<Editor />} />
                <Route path="*" element={<NotFound />} />
                <Route path='/login' element={<Login/>} />
            </Routes>
        </BrowserRouter>
    );
};

export default Router;