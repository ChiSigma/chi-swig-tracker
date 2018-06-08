import React, {Component} from 'react';
import './App.css';
import Layout from './js/pages/Layout';
import AppProvider from './js/components/AppProvider';
import AppContext from './js/app-context';
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
                    <AppContext.Consumer>
                        {(context) => (
                            <Layout context={ context } />
                        )}
                    </ AppContext.Consumer>
                </div>
                <NotificationContainer />
            </AppProvider>
        );
    }
}

export default App;
