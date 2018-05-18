import React, {Component} from 'react';
import './App.css';
import Layout from './js/pages/Layout';
import AppProvider from './js/components/AppProvider';

class App extends Component {

    render() {
        return (
            <AppProvider>
                <div className="App">
                    <Layout />
                </div>
            </AppProvider>
        );
    }
}

export default App;
