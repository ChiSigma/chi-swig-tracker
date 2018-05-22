import React, {Component} from 'react';
import './App.css';
import Layout from './js/pages/Layout';
import AppProvider from './js/components/AppProvider';
import { NotificationContainer } from 'react-notifications';

class App extends Component {

    render() {
        return (
            <AppProvider>
                <div className="App">
                    <Layout />
                </div>
                <NotificationContainer />
            </AppProvider>
        );
    }
}

export default App;
