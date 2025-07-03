import React from "react";
import Header from "./Header";
import Footer from "./Footer";
import ChatBotEngine from "../ChatBotEngine/ChatBotEngine";
import "./Layout.css";

const Layout = ({ taskName, children }) => {
    return (
        <div className="whole-container">
            <header className="header-container">
                <Header taskName={taskName}></Header>
            </header>
            <main className="body-container">
                {children}
            </main>  
            <footer className="footer-container">
                <Footer></Footer>
            </footer>

            {/* <ChatBotEngine></ChatBotEngine> */}
        </div>
    );
};

export default Layout;