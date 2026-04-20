import React from 'react';
import './styles/global.css';
import { ChatPage } from './pages/ChatPage';
import styles from './App.module.css';

function App(): React.ReactNode {
  return (
    <div className={styles.app}>
      <ChatPage />
    </div>
  );
}

export default App;
