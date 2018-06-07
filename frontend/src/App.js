import React, {Component} from 'react';
import './App.css';
import Layout from './js/pages/Layout';
import AppProvider from './js/components/AppProvider';
import { NotificationContainer, NotificationManager } from 'react-notifications';

class App extends Component {

    componentWillMount() {
        const fetch = window.fetch
        window.fetch = async function() {
            const rawResponse = await fetch.apply(global, arguments)
            const response = await rawResponse.json()

            if(response.error) {
                NotificationManager.error(response.error);
            }
            return Promise.resolve(response);
        }
    }

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
