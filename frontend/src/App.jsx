import { React, useState } from 'react';
import { HashRouter, BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home/Home';
import QualityControlDashboard from './pages/Dashboard/QualityControlDashboard';
import CostEstimateDashboard from './pages/Dashboard/CostEstimateDashboard';
import QualityControlMain from './pages/QualityControl/QualityControlMain';
import CostEstimateMain from './pages/CostEstimate/CostEstimateMain';
import ImageInteract from './pages/ImageInteract/ImageInteract';

function App() {

    return (
        <HashRouter
        future={{
            v7_relativeSplatPath: true,
        }}>
            <Routes>
                <Route path='/' element={<Home />}></Route>
                <Route path='/qualitycontrol/dashboard' element={<QualityControlDashboard />}></Route>
                <Route path='/costestimate/dashboard' element={<CostEstimateDashboard />}></Route>
                <Route path='/qualitycontrol/main' element={<QualityControlMain />}></Route>
                <Route path='/costestimate/main' element={<CostEstimateMain />}></Route>
                <Route path='/imageinteract' element={<ImageInteract />}></Route>
            </Routes>
        </HashRouter>
    );
};

export default App;