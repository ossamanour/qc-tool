import React, { useEffect } from "react";
import Layout from "../../components/Layout/Layout";
import useStore from "../../components/store/store";
import AuthenticateModule from "./components/AuthenticateModule/AuthenticateModule";
import ServiceModule from "./components/ServiceModule/ServiceModule";
import "./Home.css";

const Home = () => {
    const {isAuthenticated, autoPageDataFetch} = useStore();

    useEffect(() => {
        autoPageDataFetch("home");
    }, []);

    return (
        <Layout>
            <div>
                <section className="logo">
                    <h1>Welcome to AIAEC</h1>
                </section>
                {isAuthenticated ? <></> : <section className="auth-module">
                    <AuthenticateModule></AuthenticateModule></section>}
                <ServiceModule></ServiceModule>
            </div>
        </Layout>
    );
};

export default Home;